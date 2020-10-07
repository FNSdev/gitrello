from django.test import TestCase

from boards.exceptions import BoardNotFoundException
from boards.tests.factories import BoardFactory
from tickets.services import CategoryService


class TestCategoryService(TestCase):
    def test_create_category(self):
        board = BoardFactory()

        category = CategoryService.create_category(
            name='category',
            board_id=board.id,
        )

        self.assertIsNotNone(category)
        self.assertEqual(category.name, 'category')
        self.assertEqual(category.board.id, board.id)

    def test_create_category_board_not_found(self):
        with self.assertRaises(BoardNotFoundException):
            _ = CategoryService.create_category(
                name='category',
                board_id=-1,
            )
