from django.db.models import Subquery

from boards.exceptions import BoardAlreadyExistsException
from boards.models import Board
from boards.services import BoardMembershipService
from organizations.choices import OrganizationMemberRole
from organizations.exceptions import OrganizationNotFoundException
from organizations.models import Organization, OrganizationMembership


class BoardService:
    @classmethod
    def create_board(cls, name: str, organization_id: int) -> Board:
        if not Organization.objects.filter(id=organization_id).exists():
            raise OrganizationNotFoundException

        if Board.objects.filter(name=name, organization_id=organization_id).exists():
            raise BoardAlreadyExistsException

        board = Board.objects.create(
            name=name,
            organization_id=Subquery(Organization.objects.filter(id=organization_id).values('id')),
        )

        owner_organization_membership = OrganizationMembership.objects \
            .filter(
                organization_id=organization_id,
                role=OrganizationMemberRole.OWNER,
            ) \
            .values('id') \
            .first()

        BoardMembershipService.create_board_membership(
            board_id=board.id,
            organization_membership_id=owner_organization_membership['id'],
        )

        return board
