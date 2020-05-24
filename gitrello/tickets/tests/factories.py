from datetime import datetime

import factory

from boards.tests.factories import BoardFactory, BoardMembershipFactory
from tickets.models import Category, Ticket, TicketAssignment


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.sequence(lambda i: f'category_{i}')
    board = factory.SubFactory(BoardFactory)


class TicketFactory(factory.DjangoModelFactory):
    class Meta:
        model = Ticket

    priority = factory.sequence(lambda i: i)
    title = factory.sequence(lambda i: f'ticket_{i}')
    body = factory.sequence(lambda i: f'ticket_body_{i}')
    due_date = factory.sequence(lambda i: datetime(2000 + i, 1, 1))
    category = factory.SubFactory(CategoryFactory)


class TicketAssignmentFactory(factory.DjangoModelFactory):
    class Meta:
        model = TicketAssignment

    ticket = factory.SubFactory(TicketFactory)
    assignee = factory.SubFactory(
        BoardMembershipFactory,
        board_id=factory.SelfAttribute('..ticket.category.board_id'),
    )
