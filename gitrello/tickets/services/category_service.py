from boards.exceptions import BoardNotFoundException
from boards.models import Board
from tickets.models import Category


class CategoryService:
    NOT_SORTED = 'Not Sorted'

    @classmethod
    def create_category(cls, name: str, board_id: int) -> Category:
        if not Board.objects.filter(id=board_id).exists():
            raise BoardNotFoundException

        return Category.objects.create(
            name=name,
            board_id=board_id,
        )
