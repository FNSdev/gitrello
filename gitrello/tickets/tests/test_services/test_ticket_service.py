from datetime import datetime

from django.test import TestCase

from tickets.exceptions import CategoryNotFoundException, TicketNotFoundException
from tickets.services import TicketService
from tickets.tests.factories import CategoryFactory, TicketFactory


class TestTicketService(TestCase):
    def test_create_ticket(self):
        category = CategoryFactory()
        ticket = TicketService.create_ticket(category.id)

        self.assertEqual(ticket.category.id, category.id)
        self.assertIsNone(ticket.title)
        self.assertIsNone(ticket.body)
        self.assertIsNone(ticket.due_date)

    def test_create_ticket_category_not_found(self):
        with self.assertRaises(CategoryNotFoundException):
            _ = TicketService.create_ticket(-1)

    def test_update_ticket(self):
        ticket = TicketFactory()
        data = {
            'title': 'Hey, I`m a Ticket',
            'body': 'Hey, I`m a Ticket`s body',
            'due_date': datetime(2020, 12, 12),
        }

        updated_ticket = TicketService.update_ticket(ticket.id, data)
        self.assertEqual(updated_ticket.id, ticket.id)
        self.assertEqual(updated_ticket.category_id, ticket.category_id)
        self.assertEqual(updated_ticket.title, data['title'])
        self.assertEqual(updated_ticket.body, data['body'])
        self.assertEqual(updated_ticket.due_date, data['due_date'])

    def test_update_ticket_ticket_not_found(self):
        with self.assertRaises(TicketNotFoundException):
            _ = TicketService.update_ticket(-1, {})
