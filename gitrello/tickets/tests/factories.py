import factory

from boards.tests.factories import BoardFactory
from tickets.models import Category


class CategoryFactory(factory.Factory):
    class Meta:
        model = Category

    name = factory.sequence(lambda i: f'category_{i}')
    board = BoardFactory()
