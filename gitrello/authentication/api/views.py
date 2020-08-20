from rest_framework import views
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.api.serializers import CreateUserSerializer
from authentication.services import UserService
from gitrello.exceptions import APIRequestValidationException


class UsersView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        if not serializer.is_valid():
            raise APIRequestValidationException(serializer_errors=serializer.errors)

        user, token = UserService().create_user(**serializer.validated_data)
        return Response(
            status=201,
            data={
                'id': str(user.id),
                'token': token.key,
            },
        )


class AuthTokenView(views.APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (BasicAuthentication, )

    def get(self, request, *args, **kwargs):
        return Response(
            status=200,
            data={
                'token': request.user.auth_token.key,
                'user': {
                    'id': str(request.user.id),
                    'username': request.user.username,
                    'email': request.user.email,
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                },
            },
        )


class AuthTokenOwnerView(views.APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get(self, request, *args, **kwargs):
        return Response(
            status=200,
            data={
                'id': str(request.user.id),
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'username': request.user.username,
            },
        )
