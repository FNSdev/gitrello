import logging

from django.db import IntegrityError
from django.db.models import Subquery

from boards.exceptions import BoardNotFoundException
from boards.models import Board, BoardMembership
from organizations.models import OrganizationMembership
from tickets.models import Category

logger = logging.getLogger(__name__)


class CategoryService:
    def create_category(self, name: str, board_id: int) -> Category:
        try:
            return Category.objects.create(
                name=name,
                board_id=Subquery(Board.objects.filter(id=board_id).values('id')),
            )
        except IntegrityError:
            logger.warning('Could not create category %s on board %s', name, board_id)
            raise BoardNotFoundException

    def can_create_category(self, user_id: int, board_id: int):
        return BoardMembership.objects.filter(
            board_id=board_id,
            organization_membership_id=Subquery(
                OrganizationMembership.objects.filter(
                    user_id=user_id,
                    boards=board_id,
                ).values('id'),
            ),
        ).exists()
