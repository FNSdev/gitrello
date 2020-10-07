import requests
from django.conf import settings

from authentication.exceptions import GithubException
from gitrello.handlers import safe_http_request


class GithubOauthService:
    ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'

    @classmethod
    def _check_response_for_error(cls, response_data):
        if response_data.get('error'):
            raise GithubException(response_data['error'], response_data['error_description'])

    @classmethod
    @safe_http_request
    def exchange_code_for_token(cls, code: str) -> str:
        response = requests.post(
            url=self.ACCESS_TOKEN_URL,
            data={
                'client_id': settings.GITHUB_CLIENT_ID,
                'client_secret': settings.GITHUB_CLIENT_SECRET,
                'code': code,
            },
            headers={
                'Accept': 'application/json',
            },
        )

        response_data = response.json()
        self._check_response_for_error(response_data)
        return response_data['access_token']
