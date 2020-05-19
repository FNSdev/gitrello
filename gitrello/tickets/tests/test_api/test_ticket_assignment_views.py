from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from authentication.tests.factories import UserFactory
from boards.exceptions import BoardMembershipNotFoundException
from gitrello.exceptions import APIRequestValidationException, PermissionDeniedException
from tickets.exceptions import TicketNotFoundException, TicketAssignmentAlreadyExistsException, \
    TicketAssignmentNotFoundException
from tickets.services import TicketAssignmentService
from tickets.tests.factories import TicketAssignmentFactory


class TestTicketAssignmentsView(TestCase):
    def test_create_ticket_assignment(self):
        api_client = APIClient()
        user = UserFactory()
        payload = {
            'ticket_id': 1,
            'board_membership_id': 1,
        }
        api_client.force_authenticate(user=user)

        ticket_assignment = TicketAssignmentFactory()
        with \
                patch.object(TicketAssignmentService, 'can_assign_member', return_value=True) \
                as mocked_can_assign_member, \
                patch.object(TicketAssignmentService, 'assign_member', return_value=ticket_assignment) \
                as mocked_assign_member:
            response = api_client.post('/api/v1/ticket-assignments', data=payload, format='json')

        self.assertEqual(response.status_code, 201)
        mocked_can_assign_member.assert_called_with(
            user_id=user.id,
            ticket_id=payload['ticket_id'],
            board_membership_id=payload['board_membership_id'],
        )
        mocked_assign_member.assert_called_with(
            ticket_id=payload['ticket_id'],
            board_membership_id=payload['board_membership_id'],
        )
        expected_response = {
            'id': str(ticket_assignment.id),
            'ticket_id': str(ticket_assignment.ticket_id),
            'assignee_id': str(ticket_assignment.assignee_id),
        }
        self.assertDictEqual(response.data, expected_response)

    def test_create_ticket_assignment_request_not_valid(self):
        payload = {
            'extra_argument': 42,
            'ticket_id': 'not-an-integer',
        }

        api_client = APIClient()
        api_client.force_authenticate(user=UserFactory())
        response = api_client.post('/api/v1/ticket-assignments', data=payload, format='json')

        self.assertEqual(response.status_code, 400)

        expected_response = {
            'error_code': APIRequestValidationException.code,
            'error_message': APIRequestValidationException.message,
            'error_details': {
                "ticket_id": [
                    "A valid integer is required."
                ],
                "board_membership_id": [
                    "This field is required."
                ],
            }
        }
        self.assertDictEqual(response.data, expected_response)

    def test_create_ticket_assignment_not_authenticated(self):
        payload = {
            'ticket_id': 1,
            'board_membership_id': 1,
        }

        api_client = APIClient()
        with patch.object(TicketAssignmentService, 'can_assign_member') as mocked_can_assign_member:
            response = api_client.post('/api/v1/ticket-assignments', data=payload, format='json')

        self.assertEqual(response.status_code, 403)
        mocked_can_assign_member.assert_not_called()

    def test_create_ticket_assignment_permission_denied(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        payload = {
            'ticket_id': 1,
            'board_membership_id': 1,
        }
        with patch.object(TicketAssignmentService, 'can_assign_member', return_value=False) as mocked_can_assign_member:
            response = api_client.post('/api/v1/ticket-assignments', data=payload, format='json')

        self.assertEqual(response.status_code, 403)
        expected_response = {
            'error_code': PermissionDeniedException.code,
            'error_message': PermissionDeniedException.message,
        }
        mocked_can_assign_member.assert_called_with(
            user_id=user.id,
            ticket_id=payload['ticket_id'],
            board_membership_id=payload['board_membership_id'],
        )
        self.assertDictEqual(response.data, expected_response)

    def test_create_ticket_assignment_ticket_not_found(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        payload = {
            'ticket_id': 1,
            'board_membership_id': 1,
        }
        with patch.object(TicketAssignmentService, 'can_assign_member', return_value=True), \
                patch.object(TicketAssignmentService, 'assign_member', side_effect=TicketNotFoundException) \
                as mocked_create_ticket:
            response = api_client.post('/api/v1/ticket-assignments', data=payload, format='json')

        self.assertEqual(response.status_code, 400)
        expected_response = {
            'error_code': TicketNotFoundException.code,
            'error_message': TicketNotFoundException.message,
        }
        mocked_create_ticket.assert_called_with(
            ticket_id=payload['ticket_id'],
            board_membership_id=payload['board_membership_id'],
        )
        self.assertDictEqual(response.data, expected_response)

    def test_create_ticket_assignment_board_membership_not_found(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        payload = {
            'ticket_id': 1,
            'board_membership_id': 1,
        }
        with patch.object(TicketAssignmentService, 'can_assign_member', return_value=True), \
                patch.object(TicketAssignmentService, 'assign_member', side_effect=BoardMembershipNotFoundException) \
                as mocked_create_ticket:
            response = api_client.post('/api/v1/ticket-assignments', data=payload, format='json')

        self.assertEqual(response.status_code, 400)
        expected_response = {
            'error_code': BoardMembershipNotFoundException.code,
            'error_message': BoardMembershipNotFoundException.message,
        }
        mocked_create_ticket.assert_called_with(
            ticket_id=payload['ticket_id'],
            board_membership_id=payload['board_membership_id'],
        )
        self.assertDictEqual(response.data, expected_response)

    def test_create_ticket_assignment_already_assigned(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        payload = {
            'ticket_id': 1,
            'board_membership_id': 1,
        }
        with patch.object(TicketAssignmentService, 'can_assign_member', return_value=True), \
                patch.object(
                    TicketAssignmentService,
                    'assign_member',
                    side_effect=TicketAssignmentAlreadyExistsException
                ) \
                as mocked_create_ticket:
            response = api_client.post('/api/v1/ticket-assignments', data=payload, format='json')

        self.assertEqual(response.status_code, 400)
        expected_response = {
            'error_code': TicketAssignmentAlreadyExistsException.code,
            'error_message': TicketAssignmentAlreadyExistsException.message,
        }
        mocked_create_ticket.assert_called_with(
            ticket_id=payload['ticket_id'],
            board_membership_id=payload['board_membership_id'],
        )
        self.assertDictEqual(response.data, expected_response)


class TestTicketAssignmentView(TestCase):
    def test_delete_ticket_assignment(self):
        api_client = APIClient()
        user = UserFactory()
        api_client.force_authenticate(user=user)

        ticket_assignment = TicketAssignmentFactory()
        with \
                patch.object(TicketAssignmentService, 'can_unassign_member', return_value=True) \
                as mocked_can_unassign_member, \
                patch.object(TicketAssignmentService, 'unassign_member', return_value=ticket_assignment) \
                as mocked_unassign_member:
            response = api_client.delete('/api/v1/ticket-assignments/1',)

        self.assertEqual(response.status_code, 204)
        mocked_can_unassign_member.assert_called_with(
            user_id=user.id,
            ticket_assignment_id=1,
        )
        mocked_unassign_member.assert_called_with(
            ticket_assignment_id=1,
        )

    def test_delete_ticket_assignment_not_authenticated(self):
        api_client = APIClient()
        with patch.object(TicketAssignmentService, 'can_unassign_member') as mocked_can_unassign_member:
            response = api_client.delete('/api/v1/ticket-assignments/1')

        self.assertEqual(response.status_code, 403)
        mocked_can_unassign_member.assert_not_called()

    def test_delete_ticket_assignment_permission_denied(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        with patch.object(TicketAssignmentService, 'can_unassign_member', return_value=False) \
                as mocked_can_unassign_member:
            response = api_client.delete('/api/v1/ticket-assignments/1')

        self.assertEqual(response.status_code, 403)
        expected_response = {
            'error_code': PermissionDeniedException.code,
            'error_message': PermissionDeniedException.message,
        }
        mocked_can_unassign_member.assert_called_with(
            user_id=user.id,
            ticket_assignment_id=1,
        )
        self.assertDictEqual(response.data, expected_response)

    def test_delete_ticket_assignment_ticket_assignment_not_found(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        with patch.object(TicketAssignmentService, 'can_unassign_member', return_value=True), \
                patch.object(
                    TicketAssignmentService,
                    'unassign_member',
                    side_effect=TicketAssignmentNotFoundException
                ) \
                as mocked_create_ticket:
            response = api_client.delete('/api/v1/ticket-assignments/1')

        self.assertEqual(response.status_code, 400)
        expected_response = {
            'error_code': TicketAssignmentNotFoundException.code,
            'error_message': TicketAssignmentNotFoundException.message,
        }
        mocked_create_ticket.assert_called_with(
            ticket_assignment_id=1,
        )
        self.assertDictEqual(response.data, expected_response)
