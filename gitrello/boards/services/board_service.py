from django.db.models import Subquery
from django.db.transaction import atomic

from boards.exceptions import BoardAlreadyExistsException
from boards.models import Board, BoardMembership
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

    def get_board(self, board_id: int) -> Board:
        return Board.objects \
            .filter(id=board_id) \
            .prefetch_related(
                'categories',
                'categories__tickets',
                'categories__tickets__assignees',
                'categories__tickets__assignees__organization_membership',
                'categories__tickets__assignees__organization_membership__user',
            ) \
            .first()

    @retry_on_transaction_serialization_error
    def can_create_board(self, organization_id: int, user_id: int) -> bool:
        return OrganizationMembership.objects.filter(
            organization_id=organization_id,
            user_id=user_id,
            role=OrganizationMemberRole.OWNER,
        ).exists()

    def can_get_board(self, board_id: int, user_id: int) -> bool:
        return BoardMembership.objects \
            .filter(
                board_id=board_id,
                organization_membership__user_id=user_id,
            ) \
            .exists()
