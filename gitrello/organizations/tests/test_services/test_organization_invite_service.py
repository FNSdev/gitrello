from unittest.mock import patch

from django.test import TestCase

from authentication.exceptions import UserNotFoundException
from authentication.tests.factories import UserFactory
from organizations.choices import OrganizationMemberRole
from organizations.exceptions import (
    OrganizationInviteAlreadyExistsException, OrganizationMembershipAlreadyExistsException,
    OrganizationNotFoundException,
)
from organizations.services import OrganizationInviteService
from organizations.tests.factories import OrganizationFactory, OrganizationMembershipFactory, OrganizationInviteFactory


class TestOrganizationInviteService(TestCase):
    def test_send_invite(self):
        organization = OrganizationFactory()
        user = UserFactory()

        invite = OrganizationInviteService.create_organization_invite(
            organization_id=organization.id,
            email=user.email,
            message='message',
        )

        self.assertIsNotNone(invite)
        self.assertEqual(invite.organization.id, organization.id)
        self.assertEqual(invite.user.id, user.id)
        self.assertEqual(invite.message, 'message')

    def test_send_invite_organization_not_found(self):
        user = UserFactory()
        with self.assertRaises(OrganizationNotFoundException):
            _ = OrganizationInviteService.create_organization_invite(
                organization_id=-1,
                email=user.email,
                message='message',
            )

    def test_send_invite_user_not_found(self):
        organization = OrganizationFactory()
        with self.assertRaises(UserNotFoundException):
            _ = OrganizationInviteService.create_organization_invite(
                organization_id=organization.id,
                email='does_not_exist@test.com',
                message='message',
            )

    def test_send_invite_already_invited(self):
        member = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        invite = OrganizationInviteFactory(organization_id=member.organization_id)

        with self.assertRaises(OrganizationInviteAlreadyExistsException):
            _ = OrganizationInviteService.create_organization_invite(
                organization_id=member.organization_id,
                email=invite.user.email,
                message='message',
            )

    def test_send_invite_already_a_member(self):
        owner = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        existing_member = OrganizationMembershipFactory(organization=owner.organization)

        with self.assertRaises(OrganizationMembershipAlreadyExistsException):
            _ = OrganizationInviteService.create_organization_invite(
                organization_id=owner.organization_id,
                email=existing_member.user.email,
                message='message',
            )
