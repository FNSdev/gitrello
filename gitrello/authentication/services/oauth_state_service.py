from authentication.exceptions import OauthStateNotFoundException
from authentication.models import OauthState


class OauthStateService:
    @classmethod
    def get_or_create(cls, user_id: int, provider: str) -> OauthState:
        oauth_state, _ = OauthState.objects \
            .get_or_create(
                user_id=user_id,
                provider=provider,
            )

        return oauth_state

    @classmethod
    def get_by_state(cls, state: str) -> OauthState:
        oauth_state = OauthState.objects.filter(state=state).first()
        if not oauth_state:
            raise OauthStateNotFoundException

        return oauth_state

    @classmethod
    def delete(cls, oauth_state_id: int):
        OauthState.objects.filter(id=oauth_state_id).delete()
