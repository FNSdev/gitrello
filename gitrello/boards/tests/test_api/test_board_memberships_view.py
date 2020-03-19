from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from authentication.tests.factories import UserFactory
from boards.exceptions import BoardMembershipAlreadyExistsException
from boards.services import BoardMembershipService
from boards.tests.factories import BoardFactory, BoardMembershipFactory
from gitrello.exceptions import APIRequestValidationException, PermissionDeniedException
from organizations.choices import OrganizationMemberRole
from organizations.tests.factories import OrganizationMembershipFactory


class TestBoardMembershipsView(TestCase):
    def test_create_board_membership(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        other_organization_membership = OrganizationMembershipFactory(
            organization_id=organization_membership.organization_id,
        )
        board = BoardFactory(organization_id=organization_membership.organization_id)
        _ = BoardMembershipFactory(organization_membership_id=organization_membership.id, board_id=board.id)
        api_client = APIClient()
        api_client.force_authenticate(user=organization_membership.user)
        board_membership = BoardMembershipFactory()

        payload = {
            'board_id': board.id,
            'organization_id': board.organization_id,
            'organization_membership_id': other_organization_membership.id,
        }

        with patch.object(BoardMembershipService, 'add_member', return_value=board_membership) as mocked_add_member:
            response = api_client.post('/api/v1/board-memberships', data=payload, format='json')

        self.assertEqual(response.status_code, 201)
        mocked_add_member.assert_called_with(
            board_id=payload['board_id'],
            organization_membership_id=payload['organization_membership_id'],
        )
        self.assertDictEqual(response.data, {'id': board_membership.id})

    def test_create_board_membership_not_authenticated(self):
        payload = {
            'board_id': 1,
            'organization_id': 1,
            'organization_membership_id': 1,
        }

        api_client = APIClient()

        with patch.object(BoardMembershipService, 'can_add_member') as mocked_can_add_member:
            response = api_client.post('/api/v1/board-memberships', data=payload, format='json')

        self.assertEqual(response.status_code, 403)
        mocked_can_add_member.assert_not_called()

    def test_create_board_membership_request_not_valid(self):
        payload = {
            'extra_argument': 42,
        }

        api_client = APIClient()
        api_client.force_authenticate(user=UserFactory())
        response = api_client.post('/api/v1/board-memberships', data=payload, format='json')

        self.assertEqual(response.status_code, 400)

        expected_response = {
            'error_code': APIRequestValidationException.code,
            'error_message': APIRequestValidationException.message,
            'error_details': {
                "board_id": [
                    "This field is required."
                ],
                "organization_membership_id": [
                    "This field is required."
                ],
            }
        }
        self.assertDictEqual(response.data, expected_response)

    def test_create_board_membership_already_exists(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        other_organization_membership = OrganizationMembershipFactory(
            organization_id=organization_membership.organization_id,
        )
        board = BoardFactory(organization_id=organization_membership.organization_id)
        _ = BoardMembershipFactory(organization_membership_id=organization_membership.id, board_id=board.id)
        api_client = APIClient()
        api_client.force_authenticate(user=organization_membership.user)

        payload = {
            'board_id': board.id,
            'organization_id': board.organization_id,
            'organization_membership_id': other_organization_membership.id,
        }

        with patch.object(
                BoardMembershipService,
                'add_member',
                side_effect=BoardMembershipAlreadyExistsException) as mocked_add_member:
            response = api_client.post('/api/v1/board-memberships', data=payload, format='json')

        self.assertEqual(response.status_code, 400)
        mocked_add_member.assert_called_with(
            board_id=payload['board_id'],
            organization_membership_id=payload['organization_membership_id'],
        )
        expected_response = {
            'error_code': BoardMembershipAlreadyExistsException.code,
            'error_message': BoardMembershipAlreadyExistsException.message,
        }
        self.assertDictEqual(response.data, expected_response)

    def test_create_board_membership_permission_denied(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)
        payload = {
            'board_id': 1,
            'organization_membership_id': 1,
        }

        with patch.object(
                BoardMembershipService,
                'can_add_member',
                return_value=False) as mocked_can_add_member:
            response = api_client.post('/api/v1/board-memberships', data=payload, format='json')

        self.assertEqual(response.status_code, 403)
        mocked_can_add_member.assert_called_with(
            user_id=user.id,
            board_id=payload['board_id'],
            organization_membership_id=payload['organization_membership_id'],
        )
        expected_response = {
            'error_code': PermissionDeniedException.code,
            'error_message': PermissionDeniedException.message,
        }
        self.assertDictEqual(response.data, expected_response)


class TestBoardMembershipView(TestCase):
    def test_delete_board_membership(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        other_organization_membership = OrganizationMembershipFactory(
            organization_id=organization_membership.organization_id,
        )
        board = BoardFactory(organization_id=organization_membership.organization_id)
        _ = BoardMembershipFactory(organization_membership_id=organization_membership.id, board_id=board.id)
        board_membership = BoardMembershipFactory(
            organization_membership_id=other_organization_membership.id,
            board_id=board.id,
        )
        api_client = APIClient()
        api_client.force_authenticate(user=organization_membership.user)

        with patch.object(BoardMembershipService, 'delete_member') as mocked_delete_member:
            response = api_client.delete(f'/api/v1/board-membership/{board_membership.id}')

        self.assertEqual(response.status_code, 204)
        mocked_delete_member.assert_called_with(board_membership_id=board_membership.id)

    def test_create_board_membership_not_authenticated(self):
        api_client = APIClient()

        with patch.object(BoardMembershipService, 'can_delete_member') as mocked_can_delete_member:
            response = api_client.delete(f'/api/v1/board-membership/1')

        self.assertEqual(response.status_code, 403)
        mocked_can_delete_member.assert_not_called()

    def test_create_board_membership_permission_denied(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        with patch.object(
                BoardMembershipService,
                'can_delete_member',
                return_value=False) as mocked_can_delete_member:
            response = api_client.delete('/api/v1/board-membership/1')

        self.assertEqual(response.status_code, 403)
        mocked_can_delete_member.assert_called_with(
            user_id=user.id,
            board_membership_id=1,
        )
        expected_response = {
            'error_code': PermissionDeniedException.code,
            'error_message': PermissionDeniedException.message,
        }
        self.assertDictEqual(response.data, expected_response)
