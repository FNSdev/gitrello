import jwt
from django.db.models import Q
from django.conf import settings
from django.views.decorators.debug import sensitive_variables

from authentication.exceptions import UserAlreadyExistsException
from authentication.models import User


class UserService:
    @classmethod
    @sensitive_variables('password')
    def create_user(
        cls,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        password: str
    ) -> User:
        if User.objects.filter(Q(username=username) | Q(email=email)).exists():
            raise UserAlreadyExistsException

        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save()

        return user

    @classmethod
    def get_jwt_token(cls, user_id: int) -> str:
        token = jwt.encode(
            payload={
                'user_id': user_id,
            },
            key=settings.SECRET_KEY,
            algorithm='HS256',
        )

        return token.decode('utf-8')
