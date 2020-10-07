from django.test import TestCase

from authentication.tests.factories import UserFactory
from organizations.choices import OrganizationMemberRole
from organizations.exceptions import (
    OrganizationMembershipAlreadyExistsException, OrganizationMembershipNotFoundException,
    CanNotLeaveOrganizationException,
)
from organizations.models import OrganizationMembership
from organizations.services import OrganizationMembershipService
from organizations.tests.factories import OrganizationFactory, OrganizationMembershipFactory


class TestOrganizationMembershipService(TestCase):
    def test_add_member(self):
        organization = OrganizationFactory()
        user = UserFactory()

        membership = OrganizationMembershipService.create_organization_membership(
            organization_id=organization.id,
            user_id=user.id,
            role=OrganizationMemberRole.OWNER,
        )

        self.assertIsNotNone(membership)
        self.assertEqual(membership.organization_id, organization.id)
        self.assertEqual(membership.user_id, user.id)
        self.assertEqual(membership.role, OrganizationMemberRole.OWNER)

    def test_add_member_already_a_member(self):
        membership = OrganizationMembershipFactory()

        with self.assertRaises(OrganizationMembershipAlreadyExistsException):
            _ = OrganizationMembershipService.create_organization_membership(
                organization_id=membership.organization_id,
                user_id=membership.user_id,
            )

    def test_delete_member(self):
        membership = OrganizationMembershipFactory()
        OrganizationMembershipService.delete_organization_membership(membership.id)

        self.assertIsNone(OrganizationMembership.objects.filter(id=membership.id).first())

    def test_delete_member_user_is_organization_owner(self):
        membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        with self.assertRaises(CanNotLeaveOrganizationException):
            OrganizationMembershipService.delete_organization_membership(membership.id)

    def test_delete_member_membership_does_not_exist(self):
        with self.assertRaises(OrganizationMembershipNotFoundException):
            OrganizationMembershipService.delete_organization_membership(-1)
