import logging
from typing import Tuple

from django.db import IntegrityError
from django.views.decorators.debug import sensitive_variables

from rest_framework.authtoken.models import Token

from authentication.exceptions import UserAlreadyExistsException
from authentication.models import User

logger = logging.getLogger(__name__)


class UserService:
    @sensitive_variables('password')
    def create_user(
        self,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        password: str
    ) -> Tuple[User, Token]:
        try:
            user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            user.set_password(password)
            user.save()
        except IntegrityError:
            logger.warning(f'Could not create user with username {username} and email {email}')
            raise UserAlreadyExistsException

        token = Token.objects.create(user=user)
        return user, token
