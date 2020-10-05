from django.test import TestCase

from authentication.services.permissions_service import Permissions, PermissionsService
from authentication.tests.factories import UserFactory
from boards.tests.factories import BoardFactory, BoardMembershipFactory
from organizations.choices import OrganizationMemberRole
from organizations.tests.factories import OrganizationFactory, OrganizationInviteFactory, OrganizationMembershipFactory
from tickets.tests.factories import CategoryFactory, TicketFactory


class TestPermissionsService(TestCase):
    def _assert_has_no_permissions(self, permissions: Permissions):
        self.assertFalse(permissions.can_read)
        self.assertFalse(permissions.can_mutate)
        self.assertFalse(permissions.can_delete)

    def _assert_has_read_permissions(self, permissions: Permissions):
        self.assertTrue(permissions.can_read)
        self.assertFalse(permissions.can_mutate)
        self.assertFalse(permissions.can_delete)

    def _assert_has_mutate_permissions(self, permissions: Permissions):
        self.assertTrue(permissions.can_read)
        self.assertTrue(permissions.can_mutate)
        self.assertFalse(permissions.can_delete)

    def _assert_has_all_permissions(self, permissions: Permissions):
        self.assertTrue(permissions.can_read)
        self.assertTrue(permissions.can_mutate)
        self.assertTrue(permissions.can_delete)

    def test_organization_permissions_for_owner(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)

        permissions = PermissionsService.get_organization_permissions(
            organization_id=organization_membership.organization_id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_all_permissions(permissions)

    def test_organization_permissions_for_organization_member(self):
        organization_membership_1 = OrganizationMembershipFactory(role=OrganizationMemberRole.ADMIN)
        organization_membership_2 = OrganizationMembershipFactory(role=OrganizationMemberRole.MEMBER)

        for member in (organization_membership_1, organization_membership_2):
            permissions = PermissionsService.get_organization_permissions(
                organization_id=member.organization_id,
                user_id=member.user_id,
            )
            self._assert_has_read_permissions(permissions)

    def test_organization_permissions_for_a_random_user(self):
        permissions = PermissionsService.get_organization_permissions(
            organization_id=OrganizationFactory().id,
            user_id=UserFactory().id,
        )
        self._assert_has_no_permissions(permissions)

    def test_organization_permissions_organization_not_found(self):
        permissions = PermissionsService.get_organization_permissions(
            organization_id=-1,
            user_id=UserFactory().id,
        )
        self._assert_has_no_permissions(permissions)

    def test_organization_membership_permissions_for_owner(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        target_organization_membership = OrganizationMembershipFactory(
            organization_id=organization_membership.organization_id,
        )

        permissions = PermissionsService.get_organization_membership_permissions(
            organization_membership_id=target_organization_membership.id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_all_permissions(permissions)

        permissions = PermissionsService.get_organization_membership_permissions(
            organization_membership_id=organization_membership.id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_all_permissions(permissions)

    def test_organization_membership_permissions_for_admin(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.ADMIN)
        target_organization_membership = OrganizationMembershipFactory(
            organization_id=organization_membership.organization_id,
        )
        target_organization_owner_membership = OrganizationMembershipFactory(
            organization_id=organization_membership.organization_id,
            role=OrganizationMemberRole.OWNER,
        )
        target_organization_admin_membership = OrganizationMembershipFactory(
            organization_id=organization_membership.organization_id,
            role=OrganizationMemberRole.ADMIN,
        )

        permissions = PermissionsService.get_organization_membership_permissions(
            organization_membership_id=target_organization_membership.id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_all_permissions(permissions)

        permissions = PermissionsService.get_organization_membership_permissions(
            organization_membership_id=organization_membership.id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_all_permissions(permissions)

        permissions = PermissionsService.get_organization_membership_permissions(
            organization_membership_id=target_organization_owner_membership.id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_read_permissions(permissions)

        permissions = PermissionsService.get_organization_membership_permissions(
            organization_membership_id=target_organization_admin_membership.id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_read_permissions(permissions)

    def test_organization_membership_permissions_for_member(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.MEMBER)
        target_organization_membership = OrganizationMembershipFactory(
            organization_id=organization_membership.organization_id,
        )
        target_organization_owner_membership = OrganizationMembershipFactory(
            organization_id=organization_membership.organization_id,
            role=OrganizationMemberRole.OWNER,
        )
        target_organization_admin_membership = OrganizationMembershipFactory(
            organization_id=organization_membership.organization_id,
            role=OrganizationMemberRole.OWNER,
        )

        permissions = PermissionsService.get_organization_membership_permissions(
            organization_membership_id=target_organization_membership.id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_read_permissions(permissions)

        permissions = PermissionsService.get_organization_membership_permissions(
            organization_membership_id=organization_membership.id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_all_permissions(permissions)

        permissions = PermissionsService.get_organization_membership_permissions(
            organization_membership_id=target_organization_owner_membership.id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_read_permissions(permissions)

        permissions = PermissionsService.get_organization_membership_permissions(
            organization_membership_id=target_organization_admin_membership.id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_read_permissions(permissions)

    def test_organization_membership_permissions_for_not_organization_member(self):
        permissions = PermissionsService.get_organization_membership_permissions(
            organization_membership_id=OrganizationMembershipFactory().id,
            user_id=UserFactory().id,
        )
        self._assert_has_no_permissions(permissions)

    def test_organization_membership_permissions_organization_membership_not_found(self):
        permissions = PermissionsService.get_organization_membership_permissions(
            organization_membership_id=-1,
            user_id=UserFactory().id,
        )
        self._assert_has_no_permissions(permissions)

    def test_organization_invite_permissions_for_recipient(self):
        invite = OrganizationInviteFactory()

        permissions = PermissionsService.get_organization_invite_permissions(
            organization_invite_id=invite.id,
            user_id=invite.user_id,
        )
        self._assert_has_all_permissions(permissions)

    def test_organization_invite_permissions_for_a_random_user(self):
        permissions = PermissionsService.get_organization_invite_permissions(
            organization_invite_id=OrganizationInviteFactory().id,
            user_id=UserFactory().id,
        )
        self._assert_has_no_permissions(permissions)

    def test_organization_invite_permissions_organization_invite_not_found(self):
        permissions = PermissionsService.get_organization_invite_permissions(
            organization_invite_id=-1,
            user_id=UserFactory().id,
        )
        self._assert_has_no_permissions(permissions)

    def test_board_permissions_for_owner(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        board_membership = BoardMembershipFactory(organization_membership=organization_membership)

        permissions = PermissionsService.get_board_permissions(
            board_id=board_membership.board_id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_all_permissions(permissions)

    def test_board_permissions_for_admin(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.ADMIN)
        board_membership = BoardMembershipFactory(organization_membership=organization_membership)

        permissions = PermissionsService.get_board_permissions(
            board_id=board_membership.board_id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_mutate_permissions(permissions)

    def test_board_permissions_for_member(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.MEMBER)
        board_membership = BoardMembershipFactory(organization_membership=organization_membership)

        permissions = PermissionsService.get_board_permissions(
            board_id=board_membership.board_id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_read_permissions(permissions)

    def test_board_permissions_for_not_a_board_member(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.MEMBER)
        board = BoardFactory(organization_id=organization_membership.organization_id)

        permissions = PermissionsService.get_board_permissions(
            board_id=board.id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_no_permissions(permissions)

    def test_board_permissions_for_a_random_user(self):
        permissions = PermissionsService.get_board_permissions(
            board_id=BoardFactory().id,
            user_id=UserFactory().id,
        )
        self._assert_has_no_permissions(permissions)

    def test_board_permissions_board_not_found(self):
        permissions = PermissionsService.get_board_permissions(
            board_id=-1,
            user_id=UserFactory().id,
        )
        self._assert_has_no_permissions(permissions)

    def test_board_membership_permissions_for_owner(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        board_membership = BoardMembershipFactory(organization_membership=organization_membership)
        target_board_membership = BoardMembershipFactory(
            organization_membership=OrganizationMembershipFactory(organization=organization_membership.organization),
            board_id=board_membership.board_id,
        )

        permissions = PermissionsService.get_board_membership_permissions(
            board_membership_id=target_board_membership.id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_all_permissions(permissions)

        permissions = PermissionsService.get_board_membership_permissions(
            board_membership_id=board_membership.id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_all_permissions(permissions)

    def test_board_membership_permissions_for_admin(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.ADMIN)
        board_membership = BoardMembershipFactory(organization_membership=organization_membership)
        target_board_membership = BoardMembershipFactory(
            organization_membership=OrganizationMembershipFactory(organization=organization_membership.organization),
            board_id=board_membership.board_id,
        )
        target_owner_board_membership = BoardMembershipFactory(
            organization_membership=OrganizationMembershipFactory(
                organization=organization_membership.organization,
                role=OrganizationMemberRole.OWNER,
            ),
            board_id=board_membership.board_id,
        )

        permissions = PermissionsService.get_board_membership_permissions(
            board_membership_id=target_board_membership.id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_all_permissions(permissions)

        permissions = PermissionsService.get_board_membership_permissions(
            board_membership_id=target_owner_board_membership.id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_read_permissions(permissions)

        permissions = PermissionsService.get_board_membership_permissions(
            board_membership_id=board_membership.id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_all_permissions(permissions)

    def test_board_membership_permissions_for_member(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.MEMBER)
        board_membership = BoardMembershipFactory(organization_membership=organization_membership)
        target_board_membership = BoardMembershipFactory(
            organization_membership=OrganizationMembershipFactory(organization=organization_membership.organization),
            board_id=board_membership.board_id,
        )

        permissions = PermissionsService.get_board_membership_permissions(
            board_membership_id=target_board_membership.id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_read_permissions(permissions)

        permissions = PermissionsService.get_board_membership_permissions(
            board_membership_id=board_membership.id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_all_permissions(permissions)

    def test_board_membership_permissions_for_not_a_board_member(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.MEMBER)
        target_board_membership = BoardMembershipFactory(
            organization_membership=OrganizationMembershipFactory(organization=organization_membership.organization),
        )

        permissions = PermissionsService.get_board_membership_permissions(
            board_membership_id=target_board_membership.id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_no_permissions(permissions)

    def test_board_membership_permissions_for_a_random_user(self):
        permissions = PermissionsService.get_board_membership_permissions(
            board_membership_id=BoardMembershipFactory().id,
            user_id=UserFactory().id,
        )
        self._assert_has_no_permissions(permissions)

    def test_board_membership_permissions_board_membership_not_found(self):
        permissions = PermissionsService.get_board_membership_permissions(
            board_membership_id=-1,
            user_id=UserFactory().id,
        )
        self._assert_has_no_permissions(permissions)

    def test_ticket_permissions_for_board_member(self):
        board_membership = BoardMembershipFactory()
        ticket = TicketFactory(category=CategoryFactory(board_id=board_membership.board_id))

        permissions = PermissionsService.get_ticket_permissions(
            ticket_id=ticket.id,
            user_id=board_membership.organization_membership.user_id,
        )
        self._assert_has_all_permissions(permissions)

    def test_ticket_permissions_for_not_a_board_member(self):
        ticket = TicketFactory()
        organization_membership = OrganizationMembershipFactory(
            organization_id=ticket.category.board.organization_id,
        )

        permissions = PermissionsService.get_ticket_permissions(
            ticket_id=ticket.id,
            user_id=organization_membership.user_id,
        )
        self._assert_has_no_permissions(permissions)

    def test_ticket_permissions_for_a_random_user(self):
        permissions = PermissionsService.get_ticket_permissions(
            ticket_id=TicketFactory().id,
            user_id=UserFactory().id,
        )
        self._assert_has_no_permissions(permissions)

    def test_ticket_permissions_ticket_not_found(self):
        permissions = PermissionsService.get_ticket_permissions(
            ticket_id=-1,
            user_id=UserFactory().id,
        )
        self._assert_has_no_permissions(permissions)
