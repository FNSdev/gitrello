from django.db.transaction import atomic

from authentication.exceptions import OauthStateNotFoundException
from authentication.models import OauthState
from gitrello.handlers import retry_on_transaction_serialization_error


class OauthStateService:
    @retry_on_transaction_serialization_error
    @atomic
    def get_or_create(self, user_id: int, provider: str) -> OauthState:
        oauth_state, _ = OauthState.objects \
            .get_or_create(
                user_id=user_id,
                provider=provider,
            )

        return oauth_state

    @retry_on_transaction_serialization_error
    @atomic
    def get_by_state(self, state: str) -> OauthState:
        oauth_state = OauthState.objects.filter(state=state).first()
        if not oauth_state:
            raise OauthStateNotFoundException

        return oauth_state

    def delete(self, oauth_state_id: int):
        OauthState.objects.filter(id=oauth_state_id).delete()
