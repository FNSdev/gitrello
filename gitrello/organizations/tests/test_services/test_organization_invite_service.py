from unittest.mock import patch

from django.test import TestCase

from authentication.exceptions import UserNotFoundException
from authentication.tests.factories import UserFactory
from gitrello.exceptions import PermissionDeniedException
from organizations.choices import OrganizationMemberRole, OrganizationInviteStatus
from organizations.exceptions import (
    OrganizationInviteAlreadyExistsException, OrganizationMembershipAlreadyExistsException,
)
from organizations.services import OrganizationInviteService, OrganizationMembershipService
from organizations.tests.factories import OrganizationMembershipFactory, OrganizationInviteFactory


class TestOrganizationInviteService(TestCase):
    def test_send_invite(self):
        members = (
            OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER),
            OrganizationMembershipFactory(role=OrganizationMemberRole.ADMIN),
        )
        user = UserFactory()

        for member in members:
            invite = OrganizationInviteService().send_invite(
                auth_user_id=member.user_id,
                organization_id=member.organization_id,
                email=user.email,
                message='message',
            )

            self.assertIsNotNone(invite)
            self.assertEqual(invite.organization_id, member.organization_id)
            self.assertEqual(invite.user.id, user.id)
            self.assertEqual(invite.message, 'message')
            self.assertEqual(invite.status, OrganizationInviteStatus.PENDING)

    def test_send_invite_permission_denied(self):
        member = OrganizationMembershipFactory()
        with self.assertRaises(PermissionDeniedException):
            _ = OrganizationInviteService().send_invite(
                auth_user_id=member.user_id,
                organization_id=member.organization_id,
                email='does_not_matter@test.com',
                message='message',
            )

    def test_send_invite_organization_not_found(self):
        member = OrganizationMembershipFactory()
        with self.assertRaises(PermissionDeniedException):
            _ = OrganizationInviteService().send_invite(
                auth_user_id=member.user_id,
                organization_id=-1,
                email='does_not_matter@test.com',
                message='message',
            )

    def test_send_invite_user_not_found(self):
        member = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        with self.assertRaises(UserNotFoundException):
            _ = OrganizationInviteService().send_invite(
                auth_user_id=member.user_id,
                organization_id=member.organization_id,
                email='does_not_exist@test.com',
                message='message',
            )

    def test_send_invite_already_invited(self):
        member = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        user = UserFactory()
        _ = OrganizationInviteFactory(
            organization_id=member.organization_id,
            user_id=user.id,
        )

        with self.assertRaises(OrganizationInviteAlreadyExistsException):
            _ = OrganizationInviteService().send_invite(
                auth_user_id=member.user_id,
                organization_id=member.organization_id,
                email=user.email,
                message='message',
            )

    def test_update_invite_accept(self):
        user = UserFactory()
        invite = OrganizationInviteFactory(user_id=user.id)

        with patch.object(OrganizationMembershipService, 'add_member') as mocked_add_member:
            invite = OrganizationInviteService().update_invite(
                auth_user_id=user.id,
                organization_invite_id=invite.id,
                accept=True,
            )

        self.assertIsNotNone(invite)
        self.assertEqual(invite.status, OrganizationInviteStatus.ACCEPTED)
        mocked_add_member.assert_called_with(
            organization_id=invite.organization_id,
            user_id=user.id,
        )

    def test_update_invite_decline(self):
        user = UserFactory()
        invite = OrganizationInviteFactory(user_id=user.id)

        with patch.object(OrganizationMembershipService, 'add_member') as mocked_add_member:
            invite = OrganizationInviteService().update_invite(
                auth_user_id=user.id,
                organization_invite_id=invite.id,
                accept=False,
            )

        self.assertIsNotNone(invite)
        self.assertEqual(invite.status, OrganizationInviteStatus.DECLINED)
        mocked_add_member.assert_not_called()

    def test_update_invite_permission_denied(self):
        user = UserFactory()
        invite = OrganizationInviteFactory(user_id=user.id)

        with self.assertRaises(PermissionDeniedException):
            _ = OrganizationInviteService().update_invite(
                auth_user_id=-1,
                organization_invite_id=invite.id,
                accept=False,
            )

    def test_update_invite_already_a_member(self):
        membership = OrganizationMembershipFactory()
        invite = OrganizationInviteFactory(
            user_id=membership.user_id,
            organization_id=membership.organization_id,
            status=OrganizationInviteStatus.ACCEPTED,
        )

        with self.assertRaises(OrganizationMembershipAlreadyExistsException):
            _ = OrganizationInviteService().update_invite(
                auth_user_id=membership.user_id,
                organization_invite_id=invite.id,
                accept=True,
            )
