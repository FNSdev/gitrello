from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from authentication.services.permissions_service import Permissions, PermissionsService
from authentication.tests.factories import UserFactory
from gitrello.exceptions import PermissionDeniedException
from organizations.services import OrganizationMembershipService


class TestOrganizationMembershipView(TestCase):
    def test_delete_membership(self):
        user = UserFactory()
        client = APIClient()
        client.force_authenticate(user=user)

        with \
                patch.object(
                    PermissionsService,
                    'get_organization_membership_permissions',
                    return_value=Permissions.with_all_permissions(),
                ) as mocked_get_permissions, \
                patch.object(OrganizationMembershipService, 'delete_organization_membership') as mocked_delete_member:
            response = client.delete('/api/v1/organization-memberships/42')

        self.assertEqual(response.status_code, 204)
        mocked_get_permissions.assert_called_with(
            organization_membership_id=42,
            user_id=user.id,
        )
        mocked_delete_member.assert_called_with(organization_membership_id=42)

    def test_delete_membership_not_authenticated(self):
        client = APIClient()
        response = client.delete('/api/v1/organization-memberships/1')
        self.assertEqual(response.status_code, 401)

    def test_delete_membership_permission_denied(self):
        user = UserFactory()
        client = APIClient()
        client.force_authenticate(user=user)

        with \
                patch.object(
                    PermissionsService,
                    'get_organization_membership_permissions',
                    return_value=Permissions.with_no_permissions(),
                ) as mocked_get_permissions, \
                patch.object(OrganizationMembershipService, 'delete_organization_membership') as mocked_delete_member:
            response = client.delete('/api/v1/organization-memberships/1')

        self.assertEqual(response.status_code, 403)
        mocked_get_permissions.assert_called_with(
            user_id=user.id,
            organization_membership_id=1,
        )
        mocked_delete_member.assert_not_called()
        expected_response = {
            'error_code': PermissionDeniedException.code,
            'error_message': PermissionDeniedException.message,
        }
        self.assertDictEqual(response.data, expected_response)
