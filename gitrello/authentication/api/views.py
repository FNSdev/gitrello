from rest_framework import views
from rest_framework.response import Response

from authentication.api.serializers import CreateUserSerializer
from authentication.services import UserService
from gitrello.exceptions import APIRequestValidationException
from gitrello.status_codes import StatusCode


class CreateUserView(views.APIView):
    USER_ALREADY_EXISTS = 'User with given username and/or email already exists'

    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        if not serializer.is_valid():
            raise APIRequestValidationException(serializer_errors=serializer.errors)

        user, token = UserService().create_user(**serializer.validated_data)
        if not user:
            return Response(
                status=400,
                data={
                    'error_code': StatusCode.ALREADY_EXISTS.value,
                    'error_message': self.USER_ALREADY_EXISTS,
                }
            )

        return Response(
            status=201,
            data={
                'id': user.id,
                'token': token.key,
            }
        )
