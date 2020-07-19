from django.db.models import Subquery
from django.db.transaction import atomic

from boards.exceptions import BoardAlreadyExistsException
from boards.models import Board
from boards.services import BoardMembershipService
from gitrello.handlers import retry_on_transaction_serialization_error
from organizations.choices import OrganizationMemberRole
from organizations.exceptions import OrganizationNotFoundException
from organizations.models import Organization, OrganizationMembership


class BoardService:
    @retry_on_transaction_serialization_error
    @atomic
    def create_board(self, name: str, organization_id: int) -> Board:
        if not Organization.objects.filter(id=organization_id).exists():
            raise OrganizationNotFoundException

        if Board.objects.filter(name=name, organization_id=organization_id).exists():
            raise BoardAlreadyExistsException

        board = Board.objects.create(
            name=name,
            organization_id=Subquery(Organization.objects.filter(id=organization_id).values('id')),
        )

        owner_organization_membership = OrganizationMembership.objects.filter(
            organization_id=organization_id,
            role=OrganizationMemberRole.OWNER,
        ).values('id').first()

        BoardMembershipService().add_member_inside_transaction(
            board_id=board.id,
            organization_membership_id=owner_organization_membership['id'],
        )

        return board

    @retry_on_transaction_serialization_error
    def can_create_board(self, organization_id: int, user_id: int) -> bool:
        return OrganizationMembership.objects.filter(
            organization_id=organization_id,
            user_id=user_id,
            role=OrganizationMemberRole.OWNER,
        ).exists()
