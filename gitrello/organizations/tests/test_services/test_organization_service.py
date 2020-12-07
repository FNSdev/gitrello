from unittest.mock import patch

from django.test import TestCase

from authentication.tests.factories import UserFactory
from organizations.choices import OrganizationMemberRole
from organizations.exceptions import OrganizationAlreadyExistsException
from organizations.services import OrganizationService, OrganizationMembershipService
from organizations.tests.factories import OrganizationFactory


class TestOrganizationService(TestCase):
    def test_create_organization(self):
        user = UserFactory()

        with patch.object(OrganizationMembershipService, 'create_organization_membership') as mocked_add_member:
            organization = OrganizationService().create_organization(
                owner_id=user.id,
                name='organization',
            )

        self.assertIsNotNone(organization)
        self.assertEqual(organization.name, 'organization')
        mocked_add_member.assert_called_with(
            organization_id=organization.id,
            user_id=user.id,
            role=OrganizationMemberRole.OWNER,
        )

    def test_create_organization_name_not_unique(self):
        organization = OrganizationFactory()
        user = UserFactory()

        with self.assertRaises(OrganizationAlreadyExistsException):
            _ = OrganizationService().create_organization(
                owner_id=user.id,
                name=organization.name,
            )
