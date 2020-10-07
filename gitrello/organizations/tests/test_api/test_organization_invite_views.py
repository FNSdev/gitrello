from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from authentication.exceptions import UserNotFoundException
from authentication.services.permissions_service import Permissions, PermissionsService
from authentication.tests.factories import UserFactory
from gitrello.exceptions import APIRequestValidationException, PermissionDeniedException
from organizations.exceptions import (
    OrganizationInviteAlreadyExistsException, OrganizationMembershipAlreadyExistsException
)
from organizations.services import OrganizationInviteService
from organizations.tests.factories import OrganizationInviteFactory


class TestOrganizationInvitesView(TestCase):
    def test_create_invite(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user)
        invite = OrganizationInviteFactory()

        payload = {
            'organization_id': 42,
            'email': invite.user.email,
            'message': 'message',
        }
        with \
                patch.object(
                    PermissionsService,
                    'get_organization_permissions',
                    return_value=Permissions.with_all_permissions(),
                ) as mocked_get_permissions, \
                patch.object(
                    OrganizationInviteService,
                    'create_organization_invite',
                    return_value=invite,
                ) as mocked_send_invite:
            response = api_client.post('/api/v1/organization-invites', data=payload, format='json')

        self.assertEqual(response.status_code, 201)
        mocked_get_permissions.assert_called_with(
            organization_id=payload['organization_id'],
            user_id=user.id,
        )
        mocked_send_invite.assert_called_with(
            organization_id=payload['organization_id'],
            email=payload['email'],
            message=payload['message']
        )
        expected_response = {
            'id': str(invite.id),
            'user_id': str(invite.user_id),
            'organization_id': str(invite.organization_id),
            'message': invite.message,
        }
        self.assertDictEqual(response.data, expected_response)

    def test_create_invite_request_not_valid(self):
        payload = {
            'extra_argument': 42,
            'email': 'not-a-email',
        }

        api_client = APIClient()
        api_client.force_authenticate(user=UserFactory())
        response = api_client.post('/api/v1/organization-invites', data=payload, format='json')

        self.assertEqual(response.status_code, 400)

        expected_response = {
            'error_code': APIRequestValidationException.code,
            'error_message': APIRequestValidationException.message,
            'error_details': {
                "organization_id": [
                    "This field is required."
                ],
                "email": [
                    "Enter a valid email address."
                ],
                "message": [
                    "This field is required."
                ],
            }
        }
        self.assertDictEqual(response.data, expected_response)

    def test_create_invite_not_authenticated(self):
        payload = {
            'organization_id': '1',
            'email': "test@test.com",
            'message': 'message',
        }

        api_client = APIClient()
        with patch.object(OrganizationInviteService, 'create_organization_invite') as mocked_send_invite:
            response = api_client.post('/api/v1/organization-invites', data=payload, format='json')

        self.assertEqual(response.status_code, 401)
        mocked_send_invite.assert_not_called()

    def test_create_invite_permission_denied(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        payload = {
            'organization_id': 1,
            'email': 'test@test.com',
            'message': 'message',
        }
        with \
                patch.object(
                    PermissionsService,
                    'get_organization_permissions',
                    return_value=Permissions.with_no_permissions(),
                ) as mocked_get_permissions, \
                patch.object(OrganizationInviteService, 'create_organization_invite') as mocked_send_invite:
            response = api_client.post('/api/v1/organization-invites', data=payload, format='json')

        self.assertEqual(response.status_code, 403)
        expected_response = {
            'error_code': PermissionDeniedException.code,
            'error_message': PermissionDeniedException.message,
        }
        mocked_get_permissions.assert_called_with(
            user_id=user.id,
            organization_id=payload['organization_id'],
        )
        mocked_send_invite.assert_not_called()
        self.assertDictEqual(response.data, expected_response)

    def test_create_invite_user_not_found(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        payload = {
            'organization_id': 42,
            'email': 'test@test.com',
            'message': 'message',
        }
        with \
                patch.object(
                    PermissionsService,
                    'get_organization_permissions',
                    return_value=Permissions.with_all_permissions(),
                ) as mocked_get_permissions, \
                patch.object(
                    OrganizationInviteService,
                    'create_organization_invite',
                    side_effect=UserNotFoundException,
                ) as mocked_send_invite:
            response = api_client.post('/api/v1/organization-invites', data=payload, format='json')

        self.assertEqual(response.status_code, 400)
        expected_response = {
            'error_code': UserNotFoundException.code,
            'error_message': UserNotFoundException.message,
        }
        mocked_get_permissions.assert_called_with(
            organization_id=payload['organization_id'],
            user_id=user.id,
        )
        mocked_send_invite.assert_called_with(
            organization_id=payload['organization_id'],
            email=payload['email'],
            message=payload['message'],
        )
        self.assertDictEqual(response.data, expected_response)

    def test_create_invite_already_exists(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        payload = {
            'organization_id': 42,
            'email': user.email,
            'message': 'message',
        }
        with \
                patch.object(
                    PermissionsService,
                    'get_organization_permissions',
                    return_value=Permissions.with_all_permissions(),
                ) as mocked_get_permissions, \
                patch.object(
                    OrganizationInviteService,
                    'create_organization_invite',
                    side_effect=OrganizationInviteAlreadyExistsException,
                ) as mocked_send_invite:
            response = api_client.post('/api/v1/organization-invites', data=payload, format='json')

        self.assertEqual(response.status_code, 400)
        expected_response = {
            'error_code': OrganizationInviteAlreadyExistsException.code,
            'error_message': OrganizationInviteAlreadyExistsException.message,
        }
        mocked_get_permissions.assert_called_with(
            organization_id=payload['organization_id'],
            user_id=user.id,
        )
        mocked_send_invite.assert_called_with(
            organization_id=payload['organization_id'],
            email=payload['email'],
            message=payload['message'],
        )
        self.assertDictEqual(response.data, expected_response)


class TestOrganizationInviteView(TestCase):
    def test_accept_or_decline_invite(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        payload = {'accept': True}
        with \
                patch.object(
                    PermissionsService,
                    'get_organization_invite_permissions',
                    return_value=Permissions.with_all_permissions(),
                ) as mocked_get_permissions, \
                patch.object(OrganizationInviteService, 'accept_or_decline_invite') as mocked_accept_or_decline_invite:
            response = api_client.patch(f'/api/v1/organization-invites/42', data=payload, format='json')

        self.assertEqual(response.status_code, 204)
        mocked_get_permissions.assert_called_with(
            organization_invite_id=42,
            user_id=user.id,
        )
        mocked_accept_or_decline_invite.assert_called_with(
            organization_invite_id=42,
            accept=payload['accept'],
        )

    def test_accept_or_decline_invite_request_not_valid(self):
        payload = {
            'extra_argument': 42,
        }

        api_client = APIClient()
        api_client.force_authenticate(user=UserFactory())
        response = api_client.patch('/api/v1/organization-invites/1', data=payload, format='json')

        self.assertEqual(response.status_code, 400)

        expected_response = {
            'error_code': APIRequestValidationException.code,
            'error_message': APIRequestValidationException.message,
            'error_details': {
                "accept": [
                    "This field is required."
                ],
            }
        }
        self.assertDictEqual(response.data, expected_response)

    def test_accept_or_decline_invite_not_authenticated(self):
        payload = {
            'accept': True
        }

        api_client = APIClient()

        with patch.object(OrganizationInviteService, 'accept_or_decline_invite') as mocked_accept_or_decline_invite:
            response = api_client.patch('/api/v1/organization-invites/1', data=payload, format='json')

        self.assertEqual(response.status_code, 401)
        mocked_accept_or_decline_invite.assert_not_called()

    def test_accept_or_decline_invite_permission_denied(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        payload = {'accept': True}
        with \
                patch.object(
                    PermissionsService,
                    'get_organization_invite_permissions',
                    return_value=Permissions.with_no_permissions(),
                ) as mocked_get_permissions, \
                patch.object(
                    OrganizationInviteService,
                    'accept_or_decline_invite',
                ) as mocked_accept_or_decline_invite:
            response = api_client.patch('/api/v1/organization-invites/1', data=payload, format='json')

        self.assertEqual(response.status_code, 403)
        mocked_get_permissions.assert_called_with(
            user_id=user.id,
            organization_invite_id=1,
        )
        mocked_accept_or_decline_invite.assert_not_called()
        expected_response = {
            'error_code': PermissionDeniedException.code,
            'error_message': PermissionDeniedException.message,
        }
        self.assertDictEqual(response.data, expected_response)

    def test_accept_or_decline_invite_already_a_member(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        payload = {'accept': True}
        with \
                patch.object(
                    PermissionsService,
                    'get_organization_invite_permissions',
                    return_value=Permissions.with_all_permissions(),
                ) as mocked_get_permissions, \
                patch.object(
                    OrganizationInviteService,
                    'accept_or_decline_invite',
                    side_effect=OrganizationMembershipAlreadyExistsException
                ) as mocked_accept_or_decline_invite:
            response = api_client.patch(f'/api/v1/organization-invites/42', data=payload, format='json')

        self.assertEqual(response.status_code, 400)
        mocked_get_permissions.assert_called_with(
            organization_invite_id=42,
            user_id=user.id,
        )
        mocked_accept_or_decline_invite.assert_called_with(
            organization_invite_id=42,
            accept=payload['accept'],
        )
        expected_response = {
            'error_code': OrganizationMembershipAlreadyExistsException.code,
            'error_message': OrganizationMembershipAlreadyExistsException.message,
        }
        self.assertDictEqual(response.data, expected_response)
