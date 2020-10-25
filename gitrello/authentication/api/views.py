import logging

from django.db.transaction import atomic
from rest_framework import views
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.api.serializers import (
    AuthTokenOwnerResponseSerializer, CreateOauthStateResponseSerializer, CreateOauthStateSerializer,
    CreateUserResponseSerializer, CreateUserSerializer, LoginResponseSerializer,
)
from authentication.services import OauthStateService, UserService
from gitrello.handlers import retry_on_transaction_serialization_error
from gitrello.schema import gitrello_schema

logger = logging.getLogger(__name__)


class UsersView(views.APIView):
    @retry_on_transaction_serialization_error
    @atomic
    @gitrello_schema(
        query_serializer=CreateUserSerializer,
        responses={201: CreateUserResponseSerializer},
        security=[],
    )
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

    @gitrello_schema(
        operation_id='login',
        responses={200: LoginResponseSerializer, 400: None, 403: None},
        security=[{'Basic': []}],
    )
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
