from django.test import TestCase

from authentication.tests.factories import UserFactory
from gitrello.exceptions import PermissionDeniedException
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

    def test_delete_member_membership_does_not_exist(self):
        with self.assertRaises(OrganizationMembershipNotFoundException):
            OrganizationMembershipService().delete_member(
                auth_user_id=1,
                organization_membership_id=1
            )

    def test_delete_owner_not_possible(self):
        membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        with self.assertRaises(CanNotLeaveOrganizationException):
            OrganizationMembershipService().delete_member(
                auth_user_id=membership.user_id,
                organization_membership_id=membership.id,
            )

    def test_delete_member_by_owner(self):
        owner_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        memberships = (
            OrganizationMembershipFactory(
                organization_id=owner_membership.organization_id,
                role=OrganizationMemberRole.ADMIN,
            ),
            OrganizationMembershipFactory(
                organization_id=owner_membership.organization_id,
                role=OrganizationMemberRole.MEMBER,
            ),
        )

        for membership in memberships:
            OrganizationMembershipService().delete_member(
                auth_user_id=owner_membership.user_id,
                organization_membership_id=membership.id,
            )

            self.assertIsNone(
                OrganizationMembership.objects.filter(
                    organization_id=membership.organization_id,
                    user_id=membership.user_id,
                ).first()
            )

    def test_delete_member_by_admin(self):
        admin_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.ADMIN)
        membership = OrganizationMembershipFactory(
            organization_id=admin_membership.organization_id,
            role=OrganizationMemberRole.MEMBER,
        )

        OrganizationMembershipService().delete_member(
            auth_user_id=admin_membership.user_id,
            organization_membership_id=membership.id,
        )

        self.assertIsNone(
            OrganizationMembership.objects.filter(
                organization_id=membership.organization_id,
                user_id=membership.user_id,
            ).first()
        )

    def test_delete_admin_by_admin_not_possible(self):
        admin_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.ADMIN)
        other_admin_membership = OrganizationMembershipFactory(
            organization_id=admin_membership.organization_id,
            role=OrganizationMemberRole.ADMIN,
        )

        with self.assertRaises(PermissionDeniedException):
            OrganizationMembershipService().delete_member(
                auth_user_id=admin_membership.user_id,
                organization_membership_id=other_admin_membership.id,
            )
