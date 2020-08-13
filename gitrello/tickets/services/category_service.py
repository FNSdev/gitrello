from django.db.models import Subquery
from django.db.transaction import atomic

from boards.exceptions import BoardNotFoundException
from boards.models import Board, BoardMembership
from gitrello.handlers import retry_on_transaction_serialization_error
from organizations.models import OrganizationMembership
from tickets.models import Category


class CategoryService:
    @retry_on_transaction_serialization_error
    @atomic
    def create_category(self, name: str, board_id: int) -> Category:
        if not Board.objects.filter(id=board_id).exists():
            raise BoardNotFoundException

        return Category.objects.create(
            name=name,
            board_id=Subquery(Board.objects.filter(id=board_id).values('id')),
        )

    @retry_on_transaction_serialization_error
    def can_create_category(self, user_id: int, board_id: int):
        return BoardMembership.objects \
            .filter(
                board_id=board_id,
                organization_membership_id=Subquery(
                    OrganizationMembership.objects
                        .filter(
                            user_id=user_id,
                            boards=board_id,
                        )
                        .values('id'),
                ),
            ) \
            .exists()
