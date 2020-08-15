from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from authentication.tests.factories import UserFactory
from boards.exceptions import BoardMembershipNotFoundException
from gitrello.exceptions import APIRequestValidationException, PermissionDeniedException
from tickets.exceptions import TicketNotFoundException
from tickets.services import CommentService
from tickets.tests.factories import CommentFactory


class TestCategoriesView(TestCase):
    def test_create_comment(self):
        api_client = APIClient()
        user = UserFactory()
        payload = {
            'ticket_id': 1,
            'message': 'test_message',
        }
        api_client.force_authenticate(user=user)

        comment = CommentFactory()
        with patch.object(CommentService, 'can_create_comment', return_value=True) as mocked_can_create_comment, \
                patch.object(CommentService, 'create_comment', return_value=comment) as mocked_create_comment:
            response = api_client.post(reverse('tickets:comments'), data=payload, format='json')

        self.assertEqual(response.status_code, 201)
        mocked_can_create_comment.assert_called_with(
            user_id=user.id,
            ticket_id=payload['ticket_id'],
        )
        mocked_create_comment.assert_called_with(
            user_id=user.id,
            ticket_id=payload['ticket_id'],
            message=payload['message'],
        )
        expected_response = {
            'id': str(comment.id),
            'ticket_id': str(comment.ticket_id),
            'author_id': str(comment.author_id),
            'message': str(comment.message),
        }
        self.assertDictEqual(response.data, expected_response)

    def test_create_comment_request_not_valid(self):
        payload = {
            'extra_argument': 42,
            'ticket_id': 'not-an-integer',
        }

        api_client = APIClient()
        api_client.force_authenticate(user=UserFactory())
        response = api_client.post(reverse('tickets:comments'), data=payload, format='json')

        self.assertEqual(response.status_code, 400)

        expected_response = {
            'error_code': APIRequestValidationException.code,
            'error_message': APIRequestValidationException.message,
            'error_details': {
                "message": [
                    "This field is required."
                ],
                "ticket_id": [
                    "A valid integer is required."
                ],
            }
        }
        self.assertDictEqual(response.data, expected_response)

    def test_create_comment_not_authenticated(self):
        payload = {
            'ticket_id': 1,
            'message': 'test_message',
        }

        api_client = APIClient()
        with patch.object(CommentService, 'can_create_comment') as mocked_can_create_comment:
            response = api_client.post(reverse('tickets:comments'), data=payload, format='json')

        self.assertEqual(response.status_code, 403)
        mocked_can_create_comment.assert_not_called()

    def test_create_comment_permission_denied(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        payload = {
            'ticket_id': 1,
            'message': 'test_message',
        }
        with patch.object(
                CommentService,
                'can_create_comment',
                return_value=False,
        ) as mocked_can_create_comment:
            response = api_client.post(reverse('tickets:comments'), data=payload, format='json')

        self.assertEqual(response.status_code, 403)
        expected_response = {
            'error_code': PermissionDeniedException.code,
            'error_message': PermissionDeniedException.message,
        }
        mocked_can_create_comment.assert_called_with(
            user_id=user.id,
            ticket_id=payload['ticket_id'],
        )
        self.assertDictEqual(response.data, expected_response)

    def test_create_comment_ticket_not_found(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        payload = {
            'ticket_id': 1,
            'message': 'test_message',
        }
        with \
                patch.object(CommentService, 'can_create_comment', return_value=True), \
                patch.object(
                    CommentService,
                    'create_comment',
                    side_effect=TicketNotFoundException,
                ) as mocked_create_comment:
            response = api_client.post(reverse('tickets:comments'), data=payload, format='json')

        self.assertEqual(response.status_code, 400)
        expected_response = {
            'error_code': TicketNotFoundException.code,
            'error_message': TicketNotFoundException.message,
        }
        mocked_create_comment.assert_called_with(
            ticket_id=payload['ticket_id'],
            user_id=user.id,
            message=payload['message'],
        )
        self.assertDictEqual(response.data, expected_response)

    def test_create_comment_board_membership_not_found(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        payload = {
            'ticket_id': 1,
            'message': 'test_message',
        }
        with \
                patch.object(CommentService, 'can_create_comment', return_value=True), \
                patch.object(
                    CommentService,
                    'create_comment',
                    side_effect=BoardMembershipNotFoundException,
                ) as mocked_create_comment:
            response = api_client.post(reverse('tickets:comments'), data=payload, format='json')

        self.assertEqual(response.status_code, 400)
        expected_response = {
            'error_code': BoardMembershipNotFoundException.code,
            'error_message': BoardMembershipNotFoundException.message,
        }
        mocked_create_comment.assert_called_with(
            ticket_id=payload['ticket_id'],
            user_id=user.id,
            message=payload['message'],
        )
        self.assertDictEqual(response.data, expected_response)
