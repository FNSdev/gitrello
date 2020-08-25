import jwt
import requests
from django.conf import settings

from gitrello.exceptions import HttpRequestException
from gitrello.handlers import safe_http_request


class GithubIntegrationServiceAPIClient:
    CREATE_GITHUB_PROFILE_URL = '/api/v1/github-profiles'

    def __init__(self, user_id):
        token = jwt.encode(
            payload={
                'user_id': user_id,
            },
            key=settings.SECRET_KEY,
            algorithm='HS256',
        )

        self.headers = {
            'Authorization': f'Bearer {token.decode("utf")}',
        }

    @safe_http_request
    def create_github_profile(self, access_token: str):
        response = requests.post(
            url=f'{settings.GITHUB_INTEGRATION_SERVICE_URL}{self.CREATE_GITHUB_PROFILE_URL}',
            json={
                'access_token': access_token,
            },
            headers=self.headers,
        )

        if not response.status_code == 201:
            raise HttpRequestException
