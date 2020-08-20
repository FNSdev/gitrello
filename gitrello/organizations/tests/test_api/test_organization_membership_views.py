from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from authentication.tests.factories import UserFactory
from gitrello.exceptions import PermissionDeniedException
from organizations.services import OrganizationMembershipService
from organizations.tests.factories import OrganizationMembershipFactory


class TestOrganizationMembershipView(TestCase):
    def test_delete_membership(self):
        membership = OrganizationMembershipFactory()
        client = APIClient()
        client.force_authenticate(user=membership.user)

        with patch.object(OrganizationMembershipService, 'delete_member') as mocked_delete_member:
            response = client.delete(f'/api/v1/organization-memberships/{membership.id}')

        self.assertEqual(response.status_code, 204)
        mocked_delete_member.assert_called_with(organization_membership_id=membership.id)

    def test_delete_membership_not_authenticated(self):
        client = APIClient()

        with patch.object(OrganizationMembershipService, 'can_delete_member') as mocked_can_delete_member:
            response = client.delete('/api/v1/organization-memberships/1')

        self.assertEqual(response.status_code, 401)
        mocked_can_delete_member.assert_not_called()

    def test_delete_membership_permission_denied(self):
        user = UserFactory()
        client = APIClient()
        client.force_authenticate(user=user)

        with patch.object(
                OrganizationMembershipService,
                'can_delete_member',
                return_value=False,
        ) as mocked_can_delete_member:
            response = client.delete('/api/v1/organization-memberships/1')

        self.assertEqual(response.status_code, 403)
        mocked_can_delete_member.assert_called_with(
            user_id=user.id,
            organization_membership_id=1,
        )
        expected_response = {
            'error_code': PermissionDeniedException.code,
            'error_message': PermissionDeniedException.message,
        }
        self.assertDictEqual(response.data, expected_response)
