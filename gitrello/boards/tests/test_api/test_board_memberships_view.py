from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from authentication.services.permissions_service import Permissions, PermissionsService
from authentication.tests.factories import UserFactory
from boards.exceptions import BoardMembershipAlreadyExistsException
from boards.services import BoardMembershipService
from boards.tests.factories import BoardMembershipFactory
from gitrello.exceptions import APIRequestValidationException, PermissionDeniedException


class TestBoardMembershipsView(TestCase):
    def test_create_board_membership(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)
        board_membership = BoardMembershipFactory()

        payload = {
            'board_id': board_membership.board_id,
            'organization_id': 56,
            'organization_membership_id': 42,
        }

        with \
                patch.object(
                    PermissionsService,
                    'get_board_permissions',
                    return_value=Permissions.with_mutate_permissions(),
                ) as mocked_get_permissions, \
                patch.object(
                    BoardMembershipService,
                    'create_board_membership',
                    return_value=board_membership,
                ) as mocked_add_member:
            response = api_client.post('/api/v1/board-memberships', data=payload, format='json')

        self.assertEqual(response.status_code, 201)
        mocked_get_permissions.assert_called_with(
            board_id=payload['board_id'],
            user_id=user.id,
        )
        mocked_add_member.assert_called_with(
            board_id=payload['board_id'],
            organization_membership_id=payload['organization_membership_id'],
        )
        self.assertDictEqual(response.data, {'id': str(board_membership.id)})

    def test_create_board_membership_not_authenticated(self):
        payload = {
            'board_id': 1,
            'organization_id': 1,
            'organization_membership_id': 1,
        }

        api_client = APIClient()
        response = api_client.post('/api/v1/board-memberships', data=payload, format='json')

        self.assertEqual(response.status_code, 401)

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
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        payload = {
            'board_id': 1,
            'organization_id': 2,
            'organization_membership_id': 3,
        }

        with \
                patch.object(
                    PermissionsService,
                    'get_board_permissions',
                    return_value=Permissions.with_mutate_permissions(),
                ) as mocked_get_permissions, \
                patch.object(
                    BoardMembershipService,
                    'create_board_membership',
                    side_effect=BoardMembershipAlreadyExistsException,
                ) as mocked_add_member:
            response = api_client.post('/api/v1/board-memberships', data=payload, format='json')

        self.assertEqual(response.status_code, 400)
        mocked_get_permissions.assert_called_with(
            board_id=payload['board_id'],
            user_id=user.id,
        )
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

        with \
                patch.object(
                    PermissionsService,
                    'get_board_permissions',
                    return_value=Permissions.with_read_permissions(),
                ) as mocked_get_permissions, \
                patch.object(
                    BoardMembershipService,
                    'create_board_membership',
                ) as mocked_add_member:
            response = api_client.post('/api/v1/board-memberships', data=payload, format='json')

        self.assertEqual(response.status_code, 403)
        mocked_get_permissions.assert_called_with(
            board_id=payload['board_id'],
            user_id=user.id,
        )
        mocked_add_member.assert_not_called()
        expected_response = {
            'error_code': PermissionDeniedException.code,
            'error_message': PermissionDeniedException.message,
        }
        self.assertDictEqual(response.data, expected_response)


class TestBoardMembershipView(TestCase):
    def test_delete_board_membership(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        with \
                patch.object(
                    PermissionsService,
                    'get_board_membership_permissions',
                    return_value=Permissions.with_all_permissions(),
                ) as mocked_get_permissions, \
                patch.object(BoardMembershipService, 'delete_board_membership') as mocked_delete_member:
            response = api_client.delete('/api/v1/board-memberships/42')

        self.assertEqual(response.status_code, 204)
        mocked_get_permissions.assert_called_with(
            board_membership_id=42,
            user_id=user.id,
        )
        mocked_delete_member.assert_called_with(board_membership_id=42)

    def test_create_board_membership_not_authenticated(self):
        api_client = APIClient()

        response = api_client.delete(f'/api/v1/board-memberships/1')
        self.assertEqual(response.status_code, 401)

    def test_create_board_membership_permission_denied(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        with \
                patch.object(
                    PermissionsService,
                    'get_board_membership_permissions',
                    return_value=Permissions.with_mutate_permissions(),
                ) as mocked_get_permissions, \
                patch.object(BoardMembershipService, 'delete_board_membership') as mocked_delete_member:
            response = api_client.delete('/api/v1/board-memberships/1')

        self.assertEqual(response.status_code, 403)
        mocked_get_permissions.assert_called_with(
            user_id=user.id,
            board_membership_id=1,
        )
        mocked_delete_member.assert_not_called()
        expected_response = {
            'error_code': PermissionDeniedException.code,
            'error_message': PermissionDeniedException.message,
        }
        self.assertDictEqual(response.data, expected_response)
