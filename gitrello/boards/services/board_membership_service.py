from django.db.models import Subquery

from boards.exceptions import (
    BoardNotFoundException, BoardMembershipAlreadyExistsException, BoardMembershipNotFoundException,
    CanNotLeaveBoardException,
)
from boards.models import BoardMembership, Board
from organizations.choices import OrganizationMemberRole
from organizations.exceptions import OrganizationMembershipNotFoundException
from organizations.models import OrganizationMembership


class BoardMembershipService:
    @classmethod
    def create_board_membership(cls, board_id: int, organization_membership_id: int) -> BoardMembership:
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
                OrganizationMembership.objects.filter(id=organization_membership_id).values('id'),
            ),
        )

    @classmethod
    def delete_board_membership(cls, board_membership_id: int):
        membership = BoardMembership.objects \
            .filter(id=board_membership_id) \
            .select_related('organization_membership') \
            .first()

        if not membership:
            raise BoardMembershipNotFoundException

        if membership.organization_membership.role == OrganizationMemberRole.OWNER:
            raise CanNotLeaveBoardException

        membership.delete()
