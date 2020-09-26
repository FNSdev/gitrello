from datetime import datetime

from django.test import TestCase

from authentication.tests.factories import UserFactory
from boards.tests.factories import BoardMembershipFactory
from organizations.tests.factories import OrganizationMembershipFactory
from tickets.exceptions import CategoryNotFoundException, TicketNotFoundException
from tickets.services import TicketService
from tickets.tests.factories import CategoryFactory, TicketFactory


class TestTicketService(TestCase):
    def test_create_ticket(self):
        category = CategoryFactory()
        ticket = TicketService().create_ticket(category.id)

        self.assertEqual(ticket.category.id, category.id)
        self.assertIsNone(ticket.title)
        self.assertIsNone(ticket.body)
        self.assertIsNone(ticket.due_date)

    def test_create_ticket_category_not_found(self):
        with self.assertRaises(CategoryNotFoundException):
            _ = TicketService().create_ticket(-1)

    def test_update_ticket(self):
        ticket = TicketFactory()
        data = {
            'title': 'Hey, I`m a Ticket',
            'body': 'Hey, I`m a Ticket`s body',
            'due_date': datetime(2020, 12, 12),
        }

        updated_ticket = TicketService().update_ticket(ticket.id, data)
        self.assertEqual(updated_ticket.id, ticket.id)
        self.assertEqual(updated_ticket.category_id, ticket.category_id)
        self.assertEqual(updated_ticket.title, data['title'])
        self.assertEqual(updated_ticket.body, data['body'])
        self.assertEqual(updated_ticket.due_date, data['due_date'])

    def test_update_ticket_ticket_not_found(self):
        with self.assertRaises(TicketNotFoundException):
            _ = TicketService().update_ticket(-1, {})

    def test_board_member_can_create_ticket(self):
        board_membership = BoardMembershipFactory()
        category = CategoryFactory(board_id=board_membership.board_id)

        self.assertTrue(
            TicketService().can_create_ticket(
                user_id=board_membership.organization_membership.user_id,
                category_id=category.id,
            )
        )

    def test_not_a_board_member_can_not_create_ticket(self):
        board_membership = BoardMembershipFactory()
        other_organization_membership = OrganizationMembershipFactory(
            organization_id=board_membership.board.organization_id
        )
        category = CategoryFactory(board_id=board_membership.board_id)

        self.assertFalse(
            TicketService().can_create_ticket(
                user_id=other_organization_membership.user_id,
                category_id=category.id,
            )
        )

    def test_random_user_can_not_create_ticket(self):
        board_membership = BoardMembershipFactory()
        category = CategoryFactory(board_id=board_membership.board_id)

        self.assertFalse(
            TicketService().can_create_ticket(
                user_id=UserFactory().id,
                category_id=category.id,
            )
        )

    def test_can_create_ticket_category_not_found(self):
        self.assertFalse(
            TicketService().can_create_ticket(
                user_id=UserFactory().id,
                category_id=-1,
            )
        )
