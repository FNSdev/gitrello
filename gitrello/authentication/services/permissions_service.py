from boards.models import BoardMembership
from organizations.choices import OrganizationMemberRole
from organizations.models import OrganizationMembership
from tickets.models import Ticket


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
    def get_organization_permissions(cls, organization_id: int, user_id: int) -> Permissions:
        organization_membership = OrganizationMembership.objects \
            .filter(
                organization_id=organization_id,
                user_id=user_id,
            ) \
            .first()

        if not organization_membership:
            return Permissions.with_no_permissions()

        if organization_membership.role == OrganizationMemberRole.OWNER:
            return Permissions.with_all_permissions()

        return Permissions.with_read_permissions()

    @classmethod
    def get_board_permissions(cls, board_id: int, user_id: int) -> Permissions:
        board_membership = BoardMembership.objects \
            .filter(board_id=board_id, organization_membership__user_id=user_id) \
            .select_related('organization_membership') \
            .first()

        if not board_membership:
            return Permissions.with_no_permissions()

        if board_membership.organization_membership.role == OrganizationMemberRole.OWNER:
            return Permissions.with_all_permissions()

        if board_membership.organization_membership.role == OrganizationMemberRole.ADMIN:
            return Permissions.with_mutate_permissions()

        return Permissions.with_read_permissions()

    @classmethod
    def get_board_membership_permissions(cls, board_membership_id: int, user_id: int) -> Permissions:
        target_board_membership = BoardMembership.objects \
            .filter(id=board_membership_id) \
            .select_related('organization_membership') \
            .first()

        if not target_board_membership:
            return Permissions.with_no_permissions()

        if target_board_membership.organization_membership.user_id == user_id:
            return Permissions.with_all_permissions()

        board_membership = BoardMembership.objects \
            .filter(
                board_id=target_board_membership.board_id,
                organization_membership__user_id=user_id,
            ) \
            .values('organization_membership__role') \
            .first()

        if not board_membership:
            return Permissions.with_no_permissions()

        role = board_membership['organization_membership__role']

        if role == OrganizationMemberRole.MEMBER:
            return Permissions.with_read_permissions()

        if role == OrganizationMemberRole.ADMIN:
            if target_board_membership.organization_membership.role == OrganizationMemberRole.OWNER:
                return Permissions.with_read_permissions()

            return Permissions.with_all_permissions()

        return Permissions.with_all_permissions()

    @classmethod
    def get_ticket_permissions(cls, ticket_id: int, user_id: int) -> Permissions:
        ticket = Ticket.objects.filter(id=ticket_id).values('category__board_id').first()
        if not ticket:
            return Permissions.with_no_permissions()

        is_board_member = BoardMembership.objects \
            .filter(
                organization_membership__user_id=user_id,
                board_id=ticket['category__board_id'],
            ) \
            .exists()

        if not is_board_member:
            return Permissions.with_no_permissions()

        return Permissions.with_all_permissions()
