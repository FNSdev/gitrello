from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from authentication.exceptions import UserAlreadyExistsException
from authentication.services import UserService
from authentication.tests.factories import UserFactory
from gitrello.exceptions import APIRequestValidationException


class TestUsersView(TestCase):
    def test_create_user(self):
        payload = {
            'username': 'username',
            'first_name': 'fn',
            'last_name': 'ln',
            'email': 'test@test.com',
            'password': 'fsD43AasdSAFfV',
        }
        user = UserFactory()

        with patch.object(UserService, 'create_user', return_value=user) as mocked_create_user:
            response = APIClient().post('/api/v1/users', data=payload, format='json')

        self.assertEqual(response.status_code, 201)
        mocked_create_user.assert_called_with(
            username=payload['username'],
            first_name=payload['first_name'],
            last_name=payload['last_name'],
            email=payload['email'],
            password=payload['password'],
        )
        self.assertDictEqual(
            response.data,
            {
                'id': str(user.id),
                'token': UserService().get_jwt_token(user.id),
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            },
        )

    def test_create_user_request_not_valid(self):
        payload = {
            'extra_argument': 42
        }
        response = APIClient().post('/api/v1/users', data=payload, format='json')
        self.assertEqual(response.status_code, 400)

        expected_response = {
            'error_code': APIRequestValidationException.code,
            'error_message': APIRequestValidationException.message,
            'error_details':  {
                "username": [
                    "This field is required."
                ],
                "email": [
                    "This field is required."
                ],
                "first_name": [
                    "This field is required."
                ],
                "last_name": [
                    "This field is required."
                ],
                "password": [
                    "This field is required."
                ]
            }
        }
        self.assertDictEqual(response.data, expected_response)

    def test_create_user_password_validation_failed(self):
        payload = {
            'username': 'username',
            'first_name': 'fn',
            'last_name': 'ln',
            'email': 'test@test.com',
            'password': 'password123',
        }
        response = APIClient().post('/api/v1/users', data=payload, format='json')
        self.assertEqual(response.status_code, 400)

        expected_response = {
            'error_code': APIRequestValidationException.code,
            'error_message': APIRequestValidationException.message,
            'error_details':  {
                "non_field_errors": [
                    "This password is too common."
                ]
            }
        }
        self.assertDictEqual(response.data, expected_response)

    def test_create_user_already_exists(self):
        payload = {
            'username': 'username',
            'first_name': 'fn',
            'last_name': 'ln',
            'email': 'test@test.com',
            'password': 'fsD43AasdSAFfV',
        }
        with patch.object(UserService, 'create_user', side_effect=UserAlreadyExistsException) as mocked_create_user:
            response = APIClient().post('/api/v1/users', data=payload, format='json')

        self.assertEqual(response.status_code, 400)
        mocked_create_user.assert_called_with(
            username=payload['username'],
            first_name=payload['first_name'],
            last_name=payload['last_name'],
            email=payload['email'],
            password=payload['password'],
        )
        expected_response = {
            'error_code': UserAlreadyExistsException.code,
            'error_message': UserAlreadyExistsException.message,
        }
        self.assertEqual(response.data, expected_response)
