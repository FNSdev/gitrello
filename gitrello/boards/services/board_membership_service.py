from django.db.models import Subquery, Q
from django.db.transaction import atomic

from boards.exceptions import (
    BoardNotFoundException, BoardMembershipAlreadyExistsException, BoardMembershipNotFoundException,
    CanNotLeaveBoardException,
)
from boards.models import BoardMembership, Board
from gitrello.handlers import retry_on_transaction_serialization_error
from organizations.choices import OrganizationMemberRole
from organizations.exceptions import OrganizationMembershipNotFoundException
from organizations.models import OrganizationMembership


class BoardMembershipService:
    @retry_on_transaction_serialization_error
    @atomic
    def add_member(self, board_id: int, organization_membership_id: int) -> BoardMembership:
        return self._add_member(board_id, organization_membership_id)

    def add_member_inside_transaction(self, board_id: int, organization_membership_id: int):
        """Should be called to create BoardMembership inside another transaction"""

        return self._add_member(board_id, organization_membership_id)

    @retry_on_transaction_serialization_error
    @atomic
    def delete_member(self, board_membership_id: int):
        membership = BoardMembership.objects.filter(id=board_membership_id).first()
        if not membership:
            raise BoardMembershipNotFoundException

        membership.delete()

    @retry_on_transaction_serialization_error
    def can_add_member(self, board_id: int, user_id: int, organization_membership_id: int) -> bool:
        return BoardMembership.objects.filter(
            Q(board_id=board_id),
            Q(organization_membership__user_id=user_id),
            Q(organization_membership__role=OrganizationMemberRole.OWNER) |
            Q(organization_membership__role=OrganizationMemberRole.ADMIN),
            Q(
                board__organization_id=Subquery(
                    OrganizationMembership.objects.filter(id=organization_membership_id).values('organization_id')
                )
            )
        ).exists()

    @retry_on_transaction_serialization_error
    @atomic
    def can_delete_member(self, user_id: int, board_membership_id: int) -> bool:
        membership_to_delete = BoardMembership.objects.filter(
            id=board_membership_id,
        ).prefetch_related('organization_membership').first()
        if not membership_to_delete:
            return False

        if membership_to_delete.organization_membership.role == OrganizationMemberRole.OWNER:
            raise CanNotLeaveBoardException

        # User wants to leave board
        if membership_to_delete.organization_membership.user_id == user_id:
            return True

        membership = BoardMembership.objects.filter(
            organization_membership__organization_id=membership_to_delete.organization_membership.organization_id,
            organization_membership__user_id=user_id,
        ).values('organization_membership__role').first()

        if not membership:
            return False

        # ADMIN users can be deleted from board only by it's owner
        if membership_to_delete.organization_membership.role == OrganizationMemberRole.ADMIN:
            return membership['organization_membership__role'] == OrganizationMemberRole.OWNER

        # MEMBER users can be deleted from board by owner and admins
        return \
            membership['organization_membership__role'] == OrganizationMemberRole.OWNER \
            or membership['organization_membership__role'] == OrganizationMemberRole.ADMIN

    def _add_member(self, board_id: int, organization_membership_id: int) -> BoardMembership:
        if not Board.objects.filter(id=board_id).exists():
            raise BoardNotFoundException

        if not OrganizationMembership.objects.filter(id=organization_membership_id).exists():
            raise OrganizationMembershipNotFoundException

        if BoardMembership.objects.filter(
                board_id=board_id, organization_membership_id=organization_membership_id).exists():
            raise BoardMembershipAlreadyExistsException

        return BoardMembership.objects.create(
            board_id=Subquery(Board.objects.filter(id=board_id).values('id')),
            organization_membership_id=Subquery(
                OrganizationMembership.objects.filter(id=organization_membership_id).values('id')
            ),
        )
