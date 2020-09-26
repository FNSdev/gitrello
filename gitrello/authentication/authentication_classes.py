import jwt
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from authentication.models import User


class JWTAuthentication(TokenAuthentication):
    keyword = 'Bearer'

    def authenticate_credentials(self, key):
        try:
            payload = jwt.decode(jwt=key, key=settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.PyJWTError:
            raise AuthenticationFailed('Invalid token')

        user = User.objects.filter(id=payload['user_id'], is_active=True).first()
        if not user:
            raise AuthenticationFailed('User does not exist or is inactive')

        return user, None
