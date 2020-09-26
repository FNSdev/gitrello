from unittest.mock import patch

from django.test import TestCase

from authentication.exceptions import UserNotFoundException
from authentication.tests.factories import UserFactory
from organizations.choices import OrganizationMemberRole
from organizations.exceptions import (
    OrganizationInviteAlreadyExistsException, OrganizationMembershipAlreadyExistsException,
    OrganizationNotFoundException, OrganizationInviteNotFoundException,
)
from organizations.models import OrganizationInvite
from organizations.services import OrganizationInviteService, OrganizationMembershipService
from organizations.tests.factories import OrganizationFactory, OrganizationMembershipFactory, OrganizationInviteFactory


class TestOrganizationInviteService(TestCase):
    def test_send_invite(self):
        organization = OrganizationFactory()
        user = UserFactory()

        invite = OrganizationInviteService().send_invite(
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
            _ = OrganizationInviteService().send_invite(
                organization_id=-1,
                email=user.email,
                message='message',
            )

    def test_send_invite_user_not_found(self):
        organization = OrganizationFactory()
        with self.assertRaises(UserNotFoundException):
            _ = OrganizationInviteService().send_invite(
                organization_id=organization.id,
                email='does_not_exist@test.com',
                message='message',
            )

    def test_send_invite_already_invited(self):
        member = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        invite = OrganizationInviteFactory(organization_id=member.organization_id)

        with self.assertRaises(OrganizationInviteAlreadyExistsException):
            _ = OrganizationInviteService().send_invite(
                organization_id=member.organization_id,
                email=invite.user.email,
                message='message',
            )

    def test_send_invite_already_a_member(self):
        owner = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        existing_member = OrganizationMembershipFactory(organization=owner.organization)

        with self.assertRaises(OrganizationMembershipAlreadyExistsException):
            _ = OrganizationInviteService().send_invite(
                organization_id=owner.organization_id,
                email=existing_member.user.email,
                message='message',
            )

    def test_can_send_invite(self):
        members = (
            OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER),
            OrganizationMembershipFactory(role=OrganizationMemberRole.ADMIN),
        )

        for member in members:
            self.assertTrue(
                OrganizationInviteService().can_send_invite(
                    user_id=member.user_id,
                    organization_id=member.organization_id,
                )
            )

    def test_can_send_invite_permission_denied(self):
        member = OrganizationMembershipFactory()

        self.assertFalse(
            OrganizationInviteService().can_send_invite(
                user_id=member.user_id,
                organization_id=member.organization_id,
            )
        )

    def test_accept_or_decline_invite_accept(self):
        user = UserFactory()
        invite = OrganizationInviteFactory(user_id=user.id)

        with patch.object(OrganizationMembershipService, 'add_member') as mocked_add_member:
            OrganizationInviteService().accept_or_decline_invite(organization_invite_id=invite.id, accept=True)

        self.assertIsNone(OrganizationInvite.objects.first())
        mocked_add_member.assert_called_with(
            organization_id=invite.organization_id,
            user_id=user.id,
        )

    def test_accept_or_decline_invite_decline(self):
        user = UserFactory()
        invite = OrganizationInviteFactory(user_id=user.id)

        with patch.object(OrganizationMembershipService, 'add_member') as mocked_add_member:
            OrganizationInviteService().accept_or_decline_invite(
                organization_invite_id=invite.id,
                accept=False,
            )

        self.assertIsNone(OrganizationInvite.objects.first())
        mocked_add_member.assert_not_called()

    def test_accept_or_decline_invite_invite_not_found(self):
        with self.assertRaises(OrganizationInviteNotFoundException):
            OrganizationInviteService().accept_or_decline_invite(organization_invite_id=-1, accept=True)

    def test_can_accept_or_decline_invite(self):
        invite = OrganizationInviteFactory()

        self.assertTrue(
            OrganizationInviteService().can_accept_or_decline_invite(
                user_id=invite.user_id,
                organization_invite_id=invite.id,
            ),
        )

    def test_can_accept_or_decline_invite_permission_denied(self):
        invite = OrganizationInviteFactory()
        user = UserFactory()

        self.assertFalse(
            OrganizationInviteService().can_accept_or_decline_invite(user_id=user.id, organization_invite_id=invite.id),
        )
        self.assertFalse(
            OrganizationInviteService().can_accept_or_decline_invite(user_id=user.id, organization_invite_id=-1),
        )
