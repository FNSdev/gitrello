from typing import Tuple

from django.db.models import Q
from django.db.transaction import atomic
from django.views.decorators.debug import sensitive_variables

from rest_framework.authtoken.models import Token

from authentication.exceptions import UserAlreadyExistsException
from authentication.models import User
from gitrello.handlers import retry_on_transaction_serialization_error


class UserService:
    @retry_on_transaction_serialization_error
    @sensitive_variables('password')
    @atomic
    def create_user(
        self,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        password: str
    ) -> Tuple[User, Token]:
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

        token = Token.objects.create(user=user)
        return user, token
