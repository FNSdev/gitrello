from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from authentication.tests.factories import UserFactory
from gitrello.exceptions import APIRequestValidationException, PermissionDeniedException
from tickets.exceptions import CategoryNotFoundException
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
            'id': ticket.id,
            'category_id': ticket.category_id,
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

        self.assertEqual(response.status_code, 403)
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
