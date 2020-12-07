import requests
from django.conf import settings

from authentication.services import UserService
from github_integration.exceptions import GithubAccountUsedByAnotherUserException
from gitrello.exceptions import HttpRequestException
from gitrello.handlers import safe_http_request


class GithubIntegrationServiceAPIClient:
    CREATE_GITHUB_PROFILE_URL = '/api/v1/github-profiles'

    # Error codes
    ALREADY_EXISTS = 106

    def __init__(self, user_id):
        self.headers = {
            'Authorization': f'Bearer {UserService.get_jwt_token(user_id)}',
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

        if response.status_code == 201:
            return

        if response.status_code == 400:
            data = response.json()
            if data['error_code'] == self.ALREADY_EXISTS:
                raise GithubAccountUsedByAnotherUserException

        raise HttpRequestException
