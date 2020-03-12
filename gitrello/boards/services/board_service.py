import logging

from django.db import IntegrityError
from django.db.models import Subquery
from django.db.transaction import atomic

from boards.models import Board
from boards.services import BoardMembershipService
from organizations.choices import OrganizationMemberRole
from organizations.exceptions import OrganizationNotFoundException
from organizations.models import Organization, OrganizationMembership

logger = logging.getLogger(__name__)


class BoardService:
    @atomic
    def create_board(self, name: str, organization_id: int) -> Board:
        try:
            board = Board.objects.create(
                name=name,
                organization_id=Subquery(Organization.objects.filter(id=organization_id).values('id')),
            )
        except IntegrityError:
            logger.warning(
                'Could not create board % for organization %s. Organization not found',
                name,
                organization_id,
            )
            raise OrganizationNotFoundException

        owner_organization_membership = OrganizationMembership.objects.filter(
            organization_id=organization_id,
            role=OrganizationMemberRole.OWNER,
        ).values('id').first()

        BoardMembershipService().add_member(
            board_id=board.id,
            organization_membership_id=owner_organization_membership['id'],
        )

        return board

    def can_create_board(self, organization_id: int, user_id: int) -> bool:
        return OrganizationMembership.objects.filter(
            organization_id=organization_id,
            user_id=user_id,
            role=OrganizationMemberRole.OWNER,
        ).exists()
