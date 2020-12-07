import logging

from django.contrib import messages
from django.db.transaction import atomic
from django.views.generic import RedirectView

from authentication.services import OauthStateService
from github_integration.services import GithubIntegrationServiceAPIClient, GithubOauthService
from gitrello.exceptions import GITrelloException
from gitrello.handlers import retry_on_transaction_serialization_error

logger = logging.getLogger(__name__)


class GithubOauthView(RedirectView):
    url = '/profile'

    # TODO add tests
    @retry_on_transaction_serialization_error
    @atomic
    def get(self, request, *args, **kwargs):
        error = request.GET.get('error')
        if error:
            messages.add_message(request, messages.ERROR, error)
            return super().get(request, *args, **kwargs)

        code = request.GET.get('code')
        state = request.GET.get('state')

        if not code or not state:
            messages.add_message(request, messages.ERROR, "Something went wrong. Please, try again")
            return super().get(request, *args, **kwargs)

        try:
            token = GithubOauthService.exchange_code_for_token(code)

            oauth_state = OauthStateService.get_by_state(state)
            user_id = oauth_state.user_id

            OauthStateService.delete(oauth_state.id)

            github_integration_service_api_client = GithubIntegrationServiceAPIClient(user_id)
            github_integration_service_api_client.create_github_profile(token)
        except GITrelloException as e:
            messages.add_message(request, messages.ERROR, e.message)

        return super().get(request, *args, **kwargs)
