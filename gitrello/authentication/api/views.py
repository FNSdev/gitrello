import logging

from django.db.transaction import atomic
from django.views.generic import RedirectView
from rest_framework import views
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.api.serializers import (
    AuthTokenOwnerResponseSerializer, CreateOauthStateResponseSerializer, CreateOauthStateSerializer,
    CreateUserResponseSerializer, CreateUserSerializer, LoginResponseSerializer,
)
from authentication.services import GithubOauthService, OauthStateService, UserService
from github_integration import GithubIntegrationServiceAPIClient
from gitrello.exceptions import HttpRequestException
from gitrello.handlers import retry_on_transaction_serialization_error
from gitrello.schema import gitrello_schema

logger = logging.getLogger(__name__)


class UsersView(views.APIView):
    @retry_on_transaction_serialization_error
    @atomic
    @gitrello_schema(query_serializer=CreateUserSerializer, responses={201: CreateUserResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserService.create_user(**serializer.validated_data)
        response_serializer = CreateUserResponseSerializer(
            instance={
                'id': str(user.id),
                'token': UserService.get_jwt_token(user.id),
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'username': user.username,
            },
        )
        return Response(
            status=201,
            data=response_serializer.data,
        )


class LoginView(views.APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (BasicAuthentication, )

    @gitrello_schema(operation_id='login', responses={200: LoginResponseSerializer, 400: None, 403: None})
    def get(self, request, *args, **kwargs):
        response_serializer = LoginResponseSerializer(
            instance={
                'id': str(request.user.id),
                'token': UserService.get_jwt_token(request.user.id),
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'username': request.user.username,
            },
        )
        return Response(
            status=200,
            data=response_serializer.data,
        )


class AuthTokenOwnerView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @gitrello_schema(
        operation_id='user_details', responses={200: AuthTokenOwnerResponseSerializer, 400: None, 403: None},
    )
    def get(self, request, *args, **kwargs):
        response_serializer = AuthTokenOwnerResponseSerializer(
            instance={
                'id': str(request.user.id),
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'username': request.user.username,
            },
        )
        return Response(
            status=200,
            data=response_serializer.data,
        )


class GithubOauthView(RedirectView):
    url = '/profile'

    # TODO add tests
    @retry_on_transaction_serialization_error
    @atomic
    def get(self, request, *args, **kwargs):
        error = request.GET.get('error')
        if error:
            # TODO show error message to user somehow
            return super().get(request, *args, **kwargs)

        code = request.GET.get('code')
        state = request.GET.get('state')

        if not code or not state:
            # TODO show error message to user somehow
            return super().get(request, *args, **kwargs)

        token = GithubOauthService.exchange_code_for_token(code)

        oauth_state = OauthStateService.get_by_state(state)
        user_id = oauth_state.user_id

        OauthStateService.delete(oauth_state.id)

        # TODO show error message to user somehow
        try:
            github_integration_service_api_client = GithubIntegrationServiceAPIClient(user_id)
            github_integration_service_api_client.create_github_profile(token)
        except HttpRequestException as e:
            logger.exception(e)

        return super().get(request, *args, **kwargs)


class OauthStatesView(views.APIView):
    permission_classes = (IsAuthenticated, )

    # TODO add tests
    @retry_on_transaction_serialization_error
    @atomic
    @gitrello_schema(query_serializer=CreateOauthStateSerializer, responses={201: CreateOauthStateResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = CreateOauthStateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        oauth_state = OauthStateService.get_or_create(user_id=request.user.id, **serializer.validated_data)
        response_serializer = CreateOauthStateResponseSerializer(instance=oauth_state)
        return Response(
            status=201,
            data=response_serializer.data,
        )
