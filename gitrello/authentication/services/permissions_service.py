from django.db.transaction import atomic

from boards.models import BoardMembership
from gitrello.handlers import retry_on_transaction_serialization_error
from organizations.choices import OrganizationMemberRole


class Permissions:
    def __init__(self, can_read: bool, can_mutate: bool, can_delete: bool):
        self.can_read = can_read
        self.can_mutate = can_mutate
        self.can_delete = can_delete

    @classmethod
    def with_no_permissions(cls):
        return cls(can_read=False, can_mutate=False, can_delete=False)

    @classmethod
    def with_read_permissions(cls):
        return cls(can_read=True, can_mutate=False, can_delete=False)

    @classmethod
    def with_mutate_permissions(cls):
        return cls(can_read=True, can_mutate=True, can_delete=False)

    @classmethod
    def with_all_permissions(cls):
        return cls(can_read=True, can_mutate=True, can_delete=True)

    def to_json(self):
        return {
            'can_read': self.can_read,
            'can_mutate': self.can_mutate,
            'can_delete': self.can_delete,
        }


class PermissionsService:
    @classmethod
    @retry_on_transaction_serialization_error
    @atomic
    def get_board_permissions(cls, board_id: int, user_id: int) -> Permissions:
        board_membership = BoardMembership.objects \
            .filter(board_id=board_id, organization_membership__user_id=user_id) \
            .select_related('organization_membership') \
            .first()

        if not board_membership:
            return Permissions.with_no_permissions()

        if board_membership.organization_membership.role == OrganizationMemberRole.OWNER:
            return Permissions.with_all_permissions()

        return Permissions.with_read_permissions()
