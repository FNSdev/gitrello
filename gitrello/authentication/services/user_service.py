from typing import Optional, Tuple

from django.db import IntegrityError
from rest_framework.authtoken.models import Token

from authentication.models import User


class UserService:
    def create_user(
        self,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        password: str
    ) -> Tuple[Optional[User], Optional[Token]]:
        try:
            user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            user.set_password(password)
            user.save()
        except IntegrityError as e:
            # TODO logging
            return None, None

        token = Token.objects.create(user=user)
        return user, token
