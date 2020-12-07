from typing import Optional

from django.db.models import F

from boards.exceptions import BoardNotFoundException
from boards.models import Board
from tickets.exceptions import CategoryNotFoundException
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

    # TODO add tests
    @classmethod
    def move_category(cls, category_id: int, insert_after_category_id: Optional[int]) -> Category:
        category = Category.objects.filter(id=category_id).first()
        if not category:
            raise CategoryNotFoundException

        if not insert_after_category_id:
            new_priority = 0
        else:
            previous_category = Category.objects.filter(id=insert_after_category_id).first()
            if not previous_category:
                raise CategoryNotFoundException

            if category.priority > previous_category.priority:
                new_priority = previous_category.priority + 1
            else:
                new_priority = previous_category.priority

        if category.priority < new_priority:
            Category.objects \
                .filter(
                    board_id=category.board_id,
                    priority__gt=category.priority,
                    priority__lte=new_priority,
                ) \
                .update(priority=F('priority') - 1)
        else:
            Category.objects \
                .filter(
                    board_id=category.board_id,
                    priority__lt=category.priority,
                    priority__gte=new_priority,
                ) \
                .update(priority=F('priority') + 1)

        category.priority = new_priority
        category.save(update_fields=('updated_at', 'priority'))

        return category

    # TODO add tests
    @classmethod
    def update_category_name(cls, category_id: int, name: str) -> Category:
        category = Category.objects.filter(id=category_id).first()
        if not category:
            raise CategoryNotFoundException

        category.name = name
        category.save()

        return category

    # TODO add tests
    @classmethod
    def delete_category(cls, category_id: int):
        category = Category.objects.filter(id=category_id).first()
        if not category:
            raise CategoryNotFoundException

        Category.objects \
            .filter(board_id=category.board_id, priority__gt=category.priority) \
            .update(priority=F('priority') - 1)

        category.delete()
