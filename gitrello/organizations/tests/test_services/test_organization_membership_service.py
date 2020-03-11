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

        membership = OrganizationMembershipService().add_member(
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
            _ = OrganizationMembershipService().add_member(
                organization_id=membership.organization_id,
                user_id=membership.user_id,
            )

    def test_delete_member(self):
        membership = OrganizationMembershipFactory()
        OrganizationMembershipService().delete_member(membership.id)

        self.assertIsNone(OrganizationMembership.objects.filter(id=membership.id).first())

    def test_delete_member_membership_does_not_exist(self):
        with self.assertRaises(OrganizationMembershipNotFoundException):
            OrganizationMembershipService().delete_member(-1)

    def test_owner_can_delete_admin(self):
        owner_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        membership = OrganizationMembershipFactory(
            organization_id=owner_membership.organization_id,
            role=OrganizationMemberRole.ADMIN,
        )

        self.assertTrue(
            OrganizationMembershipService().can_delete_member(
                user_id=owner_membership.user_id,
                organization_membership_id=membership.id,
            )
        )

    def test_owner_can_delete_member(self):
        owner_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        membership = OrganizationMembershipFactory(
            organization_id=owner_membership.organization_id,
            role=OrganizationMemberRole.MEMBER,
        )

        self.assertTrue(
            OrganizationMembershipService().can_delete_member(
                user_id=owner_membership.user_id,
                organization_membership_id=membership.id,
            )
        )

    def test_admin_can_delete_member(self):
        owner_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.ADMIN)
        membership = OrganizationMembershipFactory(organization_id=owner_membership.organization_id)

        self.assertTrue(
            OrganizationMembershipService().can_delete_member(
                user_id=owner_membership.user_id,
                organization_membership_id=membership.id,
            )
        )

    def test_delete_owner_by_owner_not_possible(self):
        owner_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)

        with self.assertRaises(CanNotLeaveOrganizationException):
            OrganizationMembershipService().can_delete_member(
                user_id=owner_membership.user_id,
                organization_membership_id=owner_membership.id,
            )

    def test_delete_admin_by_other_admin_not_possible(self):
        admin_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.ADMIN)
        other_admin_membership = OrganizationMembershipFactory(
            organization_id=admin_membership.organization_id,
            role=OrganizationMemberRole.ADMIN,
        )

        self.assertFalse(
            OrganizationMembershipService().can_delete_member(
                user_id=admin_membership.user_id,
                organization_membership_id=other_admin_membership.id,
            )
        )

    def test_member_can_not_delete_anyone(self):
        member_membership = OrganizationMembershipFactory()

        memberships = (
            OrganizationMembershipFactory(
                role=OrganizationMemberRole.ADMIN,
                organization_id=member_membership.organization_id,
            ),
            OrganizationMembershipFactory(
                role=OrganizationMemberRole.MEMBER,
                organization_id=member_membership.organization_id,
            ),
        )

        for membership in memberships:
            self.assertFalse(
                OrganizationMembershipService().can_delete_member(
                    user_id=member_membership.user_id,
                    organization_membership_id=membership.id,
                )
            )
