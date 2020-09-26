from django.test import TestCase

from authentication.exceptions import UserAlreadyExistsException
from authentication.services import UserService
from authentication.tests.factories import UserFactory


class TestUserService(TestCase):
    def test_create_user(self):
        user = UserService().create_user(
            username='username',
            first_name='fn',
            last_name='ln',
            email='test@test.com',
            password='password123',
        )

        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'username')
        self.assertEqual(user.first_name, 'fn')
        self.assertEqual(user.last_name, 'ln')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.check_password('password123'))

    def test_create_user_username_not_unique(self):
        UserFactory(username='username')
        with self.assertRaises(UserAlreadyExistsException):
            _, _ = UserService().create_user(
                username='username',
                first_name='fn',
                last_name='ln',
                email='test@test.com',
                password='password123',
            )

    def test_create_user_email_not_unique(self):
        UserFactory(email='test@test.com')
        with self.assertRaises(UserAlreadyExistsException):
            _, _ = UserService().create_user(
                username='username',
                first_name='fn',
                last_name='ln',
                email='test@test.com',
                password='password123',
            )
