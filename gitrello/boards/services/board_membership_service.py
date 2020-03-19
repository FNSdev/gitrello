import logging

from django.db import IntegrityError
from django.db.models import Subquery, Q, Case, When

from boards.exceptions import (
    GITrelloBoardsException, BoardNotFoundException, BoardMembershipAlreadyExistsException,
    BoardMembershipNotFoundException, CanNotLeaveBoardException,
)
from boards.models import BoardMembership, Board
from organizations.choices import OrganizationMemberRole
from organizations.exceptions import OrganizationMembershipNotFoundException
from organizations.models import OrganizationMembership

logger = logging.getLogger(__name__)


class BoardMembershipService:
    _board_not_found_pattern = r'null value in column "board_id"'
    _organization_membership_not_found_pattern = r'null value in column "organization_membership_id"'
    _already_exists_pattern = r'duplicate key'

    def add_member(self, board_id: int, organization_membership_id: int) -> BoardMembership:
        try:
            return BoardMembership.objects.create(
                board_id=Subquery(Board.objects.filter(id=board_id).values('id')),
                organization_membership_id=Subquery(
                    OrganizationMembership.objects.filter(id=organization_membership_id).values('id')
                ),
            )
        except IntegrityError as e:
            logger.warning(
                'Could not add organization_membership_id %s to board %s',
                organization_membership_id,
                board_id
            )
            self._process_add_member_exception(e)

    def delete_member(self, board_membership_id: int):
        membership = BoardMembership.objects.filter(id=board_membership_id).first()
        if not membership:
            raise BoardMembershipNotFoundException

        membership.delete()

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

    def _process_add_member_exception(self, e: IntegrityError):
        if e.args[0].find(self._board_not_found_pattern) != -1:
            raise BoardNotFoundException

        if e.args[0].find(self._organization_membership_not_found_pattern) != -1:
            raise OrganizationMembershipNotFoundException

        if e.args[0].find(self._already_exists_pattern) != -1:
            raise BoardMembershipAlreadyExistsException

        raise GITrelloBoardsException
