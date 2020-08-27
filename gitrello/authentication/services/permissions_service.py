from typing import TypedDict

from django.db.transaction import atomic

from boards.models import BoardMembership
from gitrello.handlers import retry_on_transaction_serialization_error
from organizations.choices import OrganizationMemberRole


class BoardPermissions(TypedDict):
    can_read: bool
    can_mutate: bool


class PermissionsService:
    @classmethod
    @retry_on_transaction_serialization_error
    @atomic
    def get_board_permissions(cls, board_id: int, user_id: int) -> BoardPermissions:
        board_membership = BoardMembership.objects \
            .filter(board_id=board_id, organization_membership__user_id=user_id) \
            .select_related('organization_membership') \
            .first()

        if not board_membership:
            return BoardPermissions(can_read=False, can_mutate=False)

        if board_membership.organization_membership.role == OrganizationMemberRole.OWNER:
            return BoardPermissions(can_read=True, can_mutate=True)

        return BoardPermissions(can_read=True, can_mutate=False)
