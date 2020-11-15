from boards.exceptions import BoardNotFoundException
from boards.models import Board
from tickets.models import Category


class CategoryService:
    NOT_SORTED = 'Not Sorted'

    @classmethod
    def create_category(cls, name: str, board_id: int) -> Category:
        if not Board.objects.filter(id=board_id).exists():
            raise BoardNotFoundException

        last_category = Category.objects \
            .filter(board_id=board_id) \
            .order_by('-priority') \
            .only('priority') \
            .first()

        return Category.objects.create(
            name=name,
            board_id=board_id,
            priority=last_category.priority + 1 if last_category else 0,
        )
