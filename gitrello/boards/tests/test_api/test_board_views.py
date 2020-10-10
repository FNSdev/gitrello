from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from authentication.services.permissions_service import Permissions, PermissionsService
from authentication.tests.factories import UserFactory
from boards.exceptions import BoardAlreadyExistsException
from boards.services import BoardService
from boards.tests.factories import BoardFactory
from gitrello.exceptions import APIRequestValidationException, PermissionDeniedException
from tickets.services import CategoryService


class TestBoardsView(TestCase):
    def test_create_board(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        board = BoardFactory()
        payload = {
            'name': 'Main Board',
            'organization_id': board.organization_id,
        }
        with  \
                patch.object(
                    PermissionsService,
                    'get_organization_permissions',
                    return_value=Permissions.with_all_permissions()
                ) as mocked_get_permissions, \
                patch.object(BoardService, 'create_board', return_value=board) as mocked_create_board, \
                patch.object(CategoryService, 'create_category') as mocked_create_category:
            response = api_client.post('/api/v1/boards', data=payload, format='json')

        self.assertEqual(response.status_code, 201)
        mocked_get_permissions.assert_called_with(
            organization_id=board.organization_id,
            user_id=user.id,
        )
        mocked_create_board.assert_called_with(
            name=payload['name'],
            organization_id=payload['organization_id'],
        )
        mocked_create_category.assert_called_with(
            name=CategoryService.NOT_SORTED,
            board_id=board.id,
        )
        self.assertDictEqual(
            response.data,
            {'id': str(board.id), 'name': board.name, 'organization_id': str(board.organization_id)},
        )

    def test_create_board_not_authenticated(self):
        payload = {
            'name': 'Main Board',
            'organization_id': 1,
        }

        api_client = APIClient()
        response = api_client.post('/api/v1/boards', data=payload, format='json')

        self.assertEqual(response.status_code, 401)

    def test_create_board_request_not_valid(self):
        payload = {
            'extra_argument': 42,
        }

        api_client = APIClient()
        api_client.force_authenticate(user=UserFactory())
        response = api_client.post('/api/v1/boards', data=payload, format='json')

        self.assertEqual(response.status_code, 400)
        expected_response = {
            'error_code': APIRequestValidationException.code,
            'error_message': APIRequestValidationException.message,
            'error_details': {
                "name": [
                    "This field is required."
                ],
                "organization_id": [
                    "This field is required."
                ],
            }
        }
        self.assertDictEqual(response.data, expected_response)

    def test_create_board_already_exists(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)
        payload = {
            'name': 'Main Board',
            'organization_id': 42,
        }

        with \
                patch.object(
                    PermissionsService,
                    'get_organization_permissions',
                    return_value=Permissions.with_all_permissions(),
                ) as mocked_get_permissions, \
                patch.object(
                    BoardService,
                    'create_board',
                    side_effect=BoardAlreadyExistsException,
                ) as mocked_create_board:
            response = api_client.post('/api/v1/boards', data=payload, format='json')

        self.assertEqual(response.status_code, 400)
        mocked_create_board.assert_called_with(
            name=payload['name'],
            organization_id=payload['organization_id']
        )
        mocked_get_permissions.assert_called_with(
            organization_id=payload['organization_id'],
            user_id=user.id,
        )
        expected_response = {
            'error_code': BoardAlreadyExistsException.code,
            'error_message': BoardAlreadyExistsException.message,
        }
        self.assertDictEqual(response.data, expected_response)

    def test_create_board_permission_denied(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)
        payload = {
            'name': 'Main Board',
            'organization_id': 1,
        }

        with \
                patch.object(
                    PermissionsService,
                    'get_organization_permissions',
                    return_value=Permissions.with_no_permissions(),
                ) as mocked_get_permissions, \
                patch.object(BoardService, 'create_board') as mocked_create_board:
            response = api_client.post('/api/v1/boards', data=payload, format='json')

        self.assertEqual(response.status_code, 403)
        mocked_create_board.assert_not_called()
        mocked_get_permissions.assert_called_with(
            user_id=user.id,
            organization_id=payload['organization_id']
        )
        expected_response = {
            'error_code': PermissionDeniedException.code,
            'error_message': PermissionDeniedException.message,
        }
        self.assertDictEqual(response.data, expected_response)
