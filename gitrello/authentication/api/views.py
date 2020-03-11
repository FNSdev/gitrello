from rest_framework import views
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
                'id': user.id,
                'token': token.key,
            }
        )
