from django.test import TestCase

from authentication.services.permissions_service import Permissions, PermissionsService
from authentication.tests.factories import UserFactory
from boards.tests.factories import BoardMembershipFactory
from organizations.tests.factories import OrganizationMembershipFactory
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
