from rest_framework import views
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BaseAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.api.serializers import CreateUserSerializer
from authentication.models import User
from authentication.services import UserService
from gitrello.exceptions import APIRequestValidationException, PermissionDeniedException


class UsersView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        if not serializer.is_valid():
            raise APIRequestValidationException(serializer_errors=serializer.errors)

        user, token = UserService().create_user(**serializer.validated_data)
        return Response(
            status=201,
            data={
                'id': user.id,
                'token': token.key,
            }
        )


class UserView(views.APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def get(self, request, *args, **kwargs):
        if request.user.id != kwargs['id']:
            raise PermissionDeniedException

        user = User.objects.filter(id=kwargs['id']).select_related('auth_token').first()
        if not user:
            return Response(status=404)

        return Response(
            status=200,
            data={
                'id': str(user.id),
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'token': user.auth_token.key,
            }
        )


class AuthTokenView(views.APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, BaseAuthentication)

    def get(self, request, *args, **kwargs):
        return Response(
            status=200,
            data={
                'token': request.user.auth_token.key,
            }
        )
