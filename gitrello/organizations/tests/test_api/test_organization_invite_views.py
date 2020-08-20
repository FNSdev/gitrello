from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from authentication.exceptions import UserNotFoundException
from authentication.tests.factories import UserFactory
from gitrello.exceptions import APIRequestValidationException, PermissionDeniedException
from organizations.choices import OrganizationMemberRole, OrganizationInviteStatus
from organizations.exceptions import (
    OrganizationInviteAlreadyExistsException, OrganizationMembershipAlreadyExistsException
)
from organizations.services import OrganizationInviteService
from organizations.tests.factories import OrganizationMembershipFactory, OrganizationInviteFactory


class TestOrganizationInvitesView(TestCase):
    def test_create_invite(self):
        members = (
            OrganizationMembershipFactory(
                role=OrganizationMemberRole.OWNER,
            ),
            OrganizationMembershipFactory(
                role=OrganizationMemberRole.ADMIN,
            ),
        )
        api_client = APIClient()

        for member in members:
            invite = OrganizationInviteFactory(organization_id=member.organization_id)
            api_client.force_authenticate(member.user)

            payload = {
                'organization_id': member.organization_id,
                'email': invite.user.email,
                'message': 'message',
            }
            with patch.object(OrganizationInviteService, 'send_invite', return_value=invite) as mocked_send_invite:
                response = api_client.post('/api/v1/organization-invites', data=payload, format='json')

            self.assertEqual(response.status_code, 201)
            mocked_send_invite.assert_called_with(
                organization_id=payload['organization_id'],
                email=payload['email'],
                message=payload['message']
            )
            expected_response = {
                'id': str(invite.id),
                'status': invite.get_status_display(),
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
        with patch.object(OrganizationInviteService, 'send_invite') as mocked_send_invite:
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
        with patch.object(
                OrganizationInviteService,
                'can_send_invite',
                return_value=False
        ) as mocked_can_send_invite:
            response = api_client.post('/api/v1/organization-invites', data=payload, format='json')

        self.assertEqual(response.status_code, 403)
        expected_response = {
            'error_code': PermissionDeniedException.code,
            'error_message': PermissionDeniedException.message,
        }
        mocked_can_send_invite.assert_called_with(
            user_id=user.id,
            organization_id=payload['organization_id'],
        )
        self.assertDictEqual(response.data, expected_response)

    def test_create_invite_user_not_found(self):
        member = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        api_client = APIClient()
        api_client.force_authenticate(user=member.user)

        payload = {
            'organization_id': member.organization_id,
            'email': 'test@test.com',
            'message': 'message',
        }
        with patch.object(
                OrganizationInviteService,
                'send_invite',
                side_effect=UserNotFoundException
        ) as mocked_send_invite:
            response = api_client.post('/api/v1/organization-invites', data=payload, format='json')

        self.assertEqual(response.status_code, 400)
        expected_response = {
            'error_code': UserNotFoundException.code,
            'error_message': UserNotFoundException.message,
        }
        mocked_send_invite.assert_called_with(
            organization_id=payload['organization_id'],
            email=payload['email'],
            message=payload['message'],
        )
        self.assertDictEqual(response.data, expected_response)

    def test_create_invite_already_exists(self):
        member = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=member.user)

        payload = {
            'organization_id': member.organization_id,
            'email': user.email,
            'message': 'message',
        }
        with patch.object(
                OrganizationInviteService,
                'send_invite',
                side_effect=OrganizationInviteAlreadyExistsException
        ) as mocked_send_invite:
            response = api_client.post('/api/v1/organization-invites', data=payload, format='json')

        self.assertEqual(response.status_code, 400)
        expected_response = {
            'error_code': OrganizationInviteAlreadyExistsException.code,
            'error_message': OrganizationInviteAlreadyExistsException.message,
        }
        mocked_send_invite.assert_called_with(
            organization_id=payload['organization_id'],
            email=payload['email'],
            message=payload['message'],
        )
        self.assertDictEqual(response.data, expected_response)


class TestOrganizationInviteView(TestCase):
    def test_update_invite(self):
        invite = OrganizationInviteFactory(status=OrganizationInviteStatus.ACCEPTED)
        api_client = APIClient()
        api_client.force_authenticate(user=invite.user)

        payload = {'accept': True}
        with patch.object(OrganizationInviteService, 'update_invite', return_value=invite) as mocked_update_invite:
            response = api_client.patch(f'/api/v1/organization-invites/{invite.id}', data=payload, format='json')

        self.assertEqual(response.status_code, 200)
        mocked_update_invite.assert_called_with(
            organization_invite_id=invite.id,
            accept=payload['accept'],
        )
        self.assertDictEqual(response.data, {'id': str(invite.id), 'status': invite.get_status_display()})

    def test_update_invite_request_not_valid(self):
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

    def test_update_invite_not_authenticated(self):
        payload = {
            'accept': True
        }

        api_client = APIClient()

        with patch.object(OrganizationInviteService, 'update_invite') as mocked_update_invite:
            response = api_client.patch('/api/v1/organization-invites/1', data=payload, format='json')

        self.assertEqual(response.status_code, 401)
        mocked_update_invite.assert_not_called()

    def test_update_invite_permission_denied(self):
        user = UserFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=user)

        payload = {'accept': True}
        with patch.object(
                OrganizationInviteService,
                'can_update_invite',
                return_value=False,
        ) as mocked_can_update_invite:
            response = api_client.patch('/api/v1/organization-invites/1', data=payload, format='json')

        self.assertEqual(response.status_code, 403)
        mocked_can_update_invite.assert_called_with(
            user_id=user.id,
            organization_invite_id=1,
        )
        expected_response = {
            'error_code': PermissionDeniedException.code,
            'error_message': PermissionDeniedException.message,
        }
        self.assertDictEqual(response.data, expected_response)

    def test_update_invite_already_a_member(self):
        invite = OrganizationInviteFactory()
        api_client = APIClient()
        api_client.force_authenticate(user=invite.user)

        payload = {'accept': True}
        with patch.object(
                OrganizationInviteService,
                'update_invite',
                side_effect=OrganizationMembershipAlreadyExistsException
        ) as mocked_update_invite:
            response = api_client.patch(f'/api/v1/organization-invites/{invite.id}', data=payload, format='json')

        self.assertEqual(response.status_code, 400)
        mocked_update_invite.assert_called_with(
            organization_invite_id=invite.id,
            accept=payload['accept'],
        )
        expected_response = {
            'error_code': OrganizationMembershipAlreadyExistsException.code,
            'error_message': OrganizationMembershipAlreadyExistsException.message,
        }
        self.assertDictEqual(response.data, expected_response)
