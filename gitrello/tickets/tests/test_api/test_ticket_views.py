from datetime import date
from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from authentication.tests.factories import UserFactory
from gitrello.exceptions import APIRequestValidationException, PermissionDeniedException
from tickets.exceptions import CategoryNotFoundException, TicketNotFoundException
from tickets.services import TicketService
from tickets.tests.factories import TicketFactory


class TestTicketsView(TestCase):
    def test_create_ticket(self):
        api_client = APIClient()
        user = UserFactory()
        payload = {
            'category_id': 1,
        }
        api_client.force_authenticate(user=user)

        ticket = TicketFactory()
        with patch.object(TicketService, 'can_create_ticket', return_value=True) as mocked_can_create_ticket, \
                patch.object(TicketService, 'create_ticket', return_value=ticket) as mocked_create_ticket:
            response = api_client.post('/api/v1/tickets', data=payload, format='json')

        self.assertEqual(response.status_code, 201)
        mocked_can_create_ticket.assert_called_with(
            user_id=user.id,
            category_id=payload['category_id'],
        )
        mocked_create_ticket.assert_called_with(
            category_id=payload['category_id'],
        )
        expected_response = {
            'id': str(ticket.id),
            'category_id': str(ticket.category_id),
            'priority': ticket.priority,
        }
        self.assertDictEqual(response.data, expected_response)

    def test_create_ticket_request_not_valid(self):
        payload = {
            'extra_argument': 42,
            'category_id': 'not-an-integer',
        }

        api_client = APIClient()
        api_client.force_authenticate(user=UserFactory())
        response = api_client.post('/api/v1/tickets', data=payload, format='json')

        self.assertEqual(response.status_code, 400)

        expected_response = {
            'error_code': APIRequestValidationException.code,
            'error_message': APIRequestValidationException.message,
            'error_details': {
                "category_id": [
                    "A valid integer is required."
                ],
            }
        }
        self.assertDictEqual(response.data, expected_response)

    def test_create_ticket_not_authenticated(self):
        payload = {
            'category_id': 1,
        }

        api_client = APIClient()
        with patch.object(TicketService, 'can_create_ticket') as mocked_can_create_ticket:
            response = api_client.post('/api/v1/tickets', data=payload, format='json')

        self.assertEqual(response.status_code, 401)
        mocked_can_create_ticket.assert_not_called()

    def test_create_ticket_permission_denied(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        payload = {
            'category_id': 1,
        }
        with patch.object(TicketService, 'can_create_ticket', return_value=False) as mocked_can_create_ticket:
            response = api_client.post('/api/v1/tickets', data=payload, format='json')

        self.assertEqual(response.status_code, 403)
        expected_response = {
            'error_code': PermissionDeniedException.code,
            'error_message': PermissionDeniedException.message,
        }
        mocked_can_create_ticket.assert_called_with(
            user_id=user.id,
            category_id=payload['category_id'],
        )
        self.assertDictEqual(response.data, expected_response)

    def test_create_ticket_category_not_found(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        payload = {
            'category_id': 1,
        }
        with patch.object(TicketService, 'can_create_ticket', return_value=True), \
                patch.object(TicketService, 'create_ticket', side_effect=CategoryNotFoundException) \
                as mocked_create_ticket:
            response = api_client.post('/api/v1/tickets', data=payload, format='json')

        self.assertEqual(response.status_code, 400)
        expected_response = {
            'error_code': CategoryNotFoundException.code,
            'error_message': CategoryNotFoundException.message,
        }
        mocked_create_ticket.assert_called_with(
            category_id=payload['category_id'],
        )
        self.assertDictEqual(response.data, expected_response)


class TestTicketView(TestCase):
    def test_update_ticket(self):
        api_client = APIClient()
        user = UserFactory()
        payload = {
            'title': 'Some Title',
            'body': 'Some Body',
            'due_date': '2021-01-01',
        }
        api_client.force_authenticate(user=user)

        ticket = TicketFactory()
        with patch.object(TicketService, 'can_update_ticket', return_value=True) as mocked_can_update_ticket, \
                patch.object(TicketService, 'update_ticket', return_value=ticket) as mocked_update_ticket:
            response = api_client.patch('/api/v1/tickets/1', data=payload, format='json')

        self.assertEqual(response.status_code, 200)
        mocked_can_update_ticket.assert_called_with(
            user_id=user.id,
            ticket_id=1,
        )
        mocked_update_ticket.assert_called_with(
            ticket_id=1,
            validated_data={
                'title': payload['title'],
                'body': payload['body'],
                'due_date': date.fromisoformat(payload['due_date']),
            }
        )
        expected_response = {
            'id': str(ticket.id),
            'title': ticket.title,
            'body': ticket.body,
            'due_date': ticket.due_date,
            'priority': ticket.priority,
            'category_id': str(ticket.category_id),
        }
        self.assertDictEqual(response.data, expected_response)

    def test_update_ticket_request_not_valid(self):
        payload = {
            'extra_argument': 42,
            'due_date': 'not-a-date',
        }

        api_client = APIClient()
        api_client.force_authenticate(user=UserFactory())
        response = api_client.patch('/api/v1/tickets/1', data=payload, format='json')

        self.assertEqual(response.status_code, 400)

        expected_response = {
            'error_code': APIRequestValidationException.code,
            'error_message': APIRequestValidationException.message,
            'error_details': {
                "due_date": [
                    "Date has wrong format. Use one of these formats instead: YYYY-MM-DD.",
                ],
            }
        }
        self.assertDictEqual(response.data, expected_response)

    def test_update_ticket_not_authenticated(self):
        payload = {
            'title': 'Some Title',
            'body': 'Some Body',
            'due_date': '2021-01-01',
        }

        api_client = APIClient()
        with patch.object(TicketService, 'can_update_ticket') as mocked_can_update_ticket:
            response = api_client.patch('/api/v1/tickets/1', data=payload, format='json')

        self.assertEqual(response.status_code, 401)
        mocked_can_update_ticket.assert_not_called()

    def test_update_ticket_permission_denied(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        payload = {
            'title': 'Some Title',
            'body': 'Some Body',
            'due_date': '2021-01-01',
        }
        with patch.object(TicketService, 'can_update_ticket', return_value=False) as mocked_can_update_ticket:
            response = api_client.patch('/api/v1/tickets/1', data=payload, format='json')

        self.assertEqual(response.status_code, 403)
        expected_response = {
            'error_code': PermissionDeniedException.code,
            'error_message': PermissionDeniedException.message,
        }
        mocked_can_update_ticket.assert_called_with(
            user_id=user.id,
            ticket_id=1,
        )
        self.assertDictEqual(response.data, expected_response)

    def test_update_ticket_ticket_not_found(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        payload = {
            'title': 'Some Title',
            'body': 'Some Body',
            'due_date': '2021-01-01',
        }
        with patch.object(TicketService, 'can_update_ticket', return_value=True), \
                patch.object(TicketService, 'update_ticket', side_effect=TicketNotFoundException) \
                as mocked_update_ticket:
            response = api_client.patch('/api/v1/tickets/1', data=payload, format='json')

        self.assertEqual(response.status_code, 400)
        expected_response = {
            'error_code': TicketNotFoundException.code,
            'error_message': TicketNotFoundException.message,
        }
        mocked_update_ticket.assert_called_with(
            ticket_id=1,
            validated_data={
                'title': payload['title'],
                'body': payload['body'],
                'due_date': date.fromisoformat(payload['due_date']),
            }
        )
        self.assertDictEqual(response.data, expected_response)
