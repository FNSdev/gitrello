from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from authentication.services.permissions_service import Permissions, PermissionsService
from authentication.tests.factories import UserFactory
from boards.exceptions import BoardNotFoundException
from gitrello.exceptions import APIRequestValidationException, PermissionDeniedException
from tickets.services import CategoryService
from tickets.tests.factories import CategoryFactory


class TestCategoriesView(TestCase):
    def test_create_category(self):
        api_client = APIClient()
        user = UserFactory()
        payload = {
            'board_id': 1,
            'name': 'category',
        }
        api_client.force_authenticate(user=user)

        category = CategoryFactory()
        with \
                patch.object(
                    PermissionsService,
                    'get_board_permissions',
                    return_value=Permissions.with_read_permissions(),
                ) as mocked_get_permissions, \
                patch.object(CategoryService, 'create_category', return_value=category) as mocked_create_category:
            response = api_client.post('/api/v1/categories', data=payload, format='json')

        self.assertEqual(response.status_code, 201)
        mocked_get_permissions.assert_called_with(
            user_id=user.id,
            board_id=payload['board_id'],
        )
        mocked_create_category.assert_called_with(
            board_id=payload['board_id'],
            name=payload['name'],
        )
        expected_response = {
            'id': str(category.id),
            'name': category.name,
            'board_id': str(category.board_id),
            'priority': category.priority,
        }
        self.assertDictEqual(response.data, expected_response)

    def test_create_category_request_not_valid(self):
        payload = {
            'extra_argument': 42,
            'board_id': 'not-an-integer',
        }

        api_client = APIClient()
        api_client.force_authenticate(user=UserFactory())
        response = api_client.post('/api/v1/categories', data=payload, format='json')

        self.assertEqual(response.status_code, 400)

        expected_response = {
            'error_code': APIRequestValidationException.code,
            'error_message': APIRequestValidationException.message,
            'error_details': {
                "name": [
                    "This field is required."
                ],
                "board_id": [
                    "A valid integer is required."
                ],
            }
        }
        self.assertDictEqual(response.data, expected_response)

    def test_create_category_not_authenticated(self):
        payload = {
            'board_id': 1,
            'name': 'category',
        }

        api_client = APIClient()
        response = api_client.post('/api/v1/categories', data=payload, format='json')

        self.assertEqual(response.status_code, 401)

    def test_create_category_permission_denied(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        payload = {
            'board_id': 1,
            'name': 'category',
        }
        with \
                patch.object(
                    PermissionsService,
                    'get_board_permissions',
                    return_value=Permissions.with_no_permissions(),
                ) as mocked_get_permissions, \
                patch.object(CategoryService, 'create_category') as mocked_create_category:
            response = api_client.post('/api/v1/categories', data=payload, format='json')

        self.assertEqual(response.status_code, 403)
        expected_response = {
            'error_code': PermissionDeniedException.code,
            'error_message': PermissionDeniedException.message,
        }
        mocked_get_permissions.assert_called_with(
            user_id=user.id,
            board_id=payload['board_id'],
        )
        mocked_create_category.assert_not_called()
        self.assertDictEqual(response.data, expected_response)

    def test_create_category_board_not_found(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        payload = {
            'board_id': 1,
            'name': 'category',
        }
        with \
                patch.object(
                    PermissionsService,
                    'get_board_permissions',
                    return_value=Permissions.with_read_permissions(),
                ) as mocked_get_permissions, \
                patch.object(
                    CategoryService,
                    'create_category',
                    side_effect=BoardNotFoundException,
                ) as mocked_create_category:
            response = api_client.post('/api/v1/categories', data=payload, format='json')

        self.assertEqual(response.status_code, 400)
        expected_response = {
            'error_code': BoardNotFoundException.code,
            'error_message': BoardNotFoundException.message,
        }
        mocked_get_permissions.assert_called_with(
            board_id=payload['board_id'],
            user_id=user.id,
        )
        mocked_create_category.assert_called_with(
            board_id=payload['board_id'],
            name=payload['name'],
        )
        self.assertDictEqual(response.data, expected_response)
