from django.test import TestCase

from authentication.tests.factories import UserFactory
from boards.exceptions import (
    BoardNotFoundException, BoardMembershipAlreadyExistsException, BoardMembershipNotFoundException,
)
from boards.models import BoardMembership
from boards.services import BoardMembershipService
from boards.tests.factories import BoardFactory, BoardMembershipFactory
from organizations.choices import OrganizationMemberRole
from organizations.exceptions import OrganizationMembershipNotFoundException
from organizations.tests.factories import OrganizationFactory, OrganizationMembershipFactory


class TestBoardMembershipService(TestCase):
    def test_add_member(self):
        organization_membership = OrganizationMembershipFactory()
        board = BoardFactory(
            organization_id=organization_membership.organization_id,
        )

        board_membership = BoardMembershipService().add_member(
            board_id=board.id,
            organization_membership_id=organization_membership.id,
        )

        self.assertIsNotNone(board_membership)
        self.assertEqual(board_membership.board.id, board.id)
        self.assertEqual(board_membership.organization_membership.id, organization_membership.id)

    def test_add_member_board_not_found(self):
        organization = OrganizationFactory()

        with self.assertRaises(BoardNotFoundException):
            _ = BoardMembershipService().add_member(
                board_id=-1,
                organization_membership_id=organization.id,
            )

    def test_add_member_organization_membership_not_found(self):
        board = BoardFactory()

        with self.assertRaises(OrganizationMembershipNotFoundException):
            _ = BoardMembershipService().add_member(
                board_id=board.id,
                organization_membership_id=-1,
            )

    def test_add_member_membership_already_exists(self):
        board_membership = BoardMembershipFactory()

        with self.assertRaises(BoardMembershipAlreadyExistsException):
            _ = BoardMembershipService().add_member(
                board_id=board_membership.board_id,
                organization_membership_id=board_membership.organization_membership_id,
            )

    def test_owner_can_add_member(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        board = BoardFactory(organization_id=organization_membership.organization_id)
        _ = BoardMembershipFactory(organization_membership_id=organization_membership.id, board_id=board.id)
        other_membership = OrganizationMembershipFactory(organization_id=organization_membership.organization_id)

        self.assertTrue(
            BoardMembershipService().can_add_member(
                board_id=board.id,
                organization_membership_id=other_membership.id,
                user_id=organization_membership.user_id,
            )
        )

    def test_admin_can_add_member(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.ADMIN)
        board = BoardFactory(organization_id=organization_membership.organization_id)
        _ = BoardMembershipFactory(organization_membership_id=organization_membership.id, board_id=board.id)
        other_membership = OrganizationMembershipFactory(organization_id=organization_membership.organization_id)

        self.assertTrue(
            BoardMembershipService().can_add_member(
                board_id=board.id,
                organization_membership_id=other_membership.id,
                user_id=organization_membership.user_id,
            )
        )

    def test_member_can_not_add_other_members(self):
        organization_membership = OrganizationMembershipFactory()
        board_membership = BoardMembershipFactory(organization_membership_id=organization_membership.id)
        other_membership = OrganizationMembershipFactory(organization_id=organization_membership.organization_id)

        self.assertFalse(
            BoardMembershipService().can_add_member(
                board_id=board_membership.board_id,
                organization_membership_id=other_membership.id,
                user_id=organization_membership.user_id,
            )
        )

    def test_admin_not_on_board_can_not_add_member(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.ADMIN)
        board = BoardFactory(organization_id=organization_membership.organization_id)
        other_membership = OrganizationMembershipFactory(organization_id=organization_membership.organization_id)

        self.assertFalse(
            BoardMembershipService().can_add_member(
                board_id=board.id,
                organization_membership_id=other_membership.id,
                user_id=organization_membership.user_id,
            )
        )

    def test_owner_can_not_add_user_not_in_organization(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        board_membership = BoardMembershipFactory(organization_membership_id=organization_membership.id)
        other_membership = OrganizationMembershipFactory()

        self.assertFalse(
            BoardMembershipService().can_add_member(
                board_id=board_membership.board_id,
                organization_membership_id=other_membership.id,
                user_id=organization_membership.user_id,
            )
        )

    def test_admin_can_not_add_user_not_in_organization(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.ADMIN)
        board_membership = BoardMembershipFactory(organization_membership_id=organization_membership.id)
        other_membership = OrganizationMembershipFactory()

        self.assertFalse(
            BoardMembershipService().can_add_member(
                board_id=board_membership.board_id,
                organization_membership_id=other_membership.id,
                user_id=organization_membership.user_id,
            )
        )

    def test_random_user_can_not_add_member(self):
        organization_membership = OrganizationMembershipFactory()
        board = BoardFactory()
        user = UserFactory()

        self.assertFalse(
            BoardMembershipService().can_add_member(
                board_id=board.id,
                organization_membership_id=organization_membership.id,
                user_id=user.id,
            )
        )

    def test_random_user_can_not_add_random_user(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        board = BoardFactory(organization_id=organization_membership.organization_id)
        other_organization_membership = OrganizationMembershipFactory()

        self.assertFalse(
            BoardMembershipService().can_add_member(
                board_id=board.id,
                organization_membership_id=other_organization_membership.id,
                user_id=organization_membership.user_id,
            )
        )

    def test_delete_member(self):
        board_membership = BoardMembershipFactory()
        BoardMembershipService().delete_member(board_membership.id)

        self.assertIsNone(BoardMembership.objects.filter(id=board_membership.id).first())

    def test_delete_member_membership_not_found(self):
        with self.assertRaises(BoardMembershipNotFoundException):
            BoardMembershipService().delete_member(-1)

    def test_owner_can_delete_admin(self):
        owner_organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        owner_board_membership = BoardMembershipFactory(organization_membership_id=owner_organization_membership.id)
        admin_organization_membership = OrganizationMembershipFactory(
            organization_id=owner_organization_membership.organization_id,
            role=OrganizationMemberRole.ADMIN
        )
        admin_board_membership = BoardMembershipFactory(
            organization_membership_id=admin_organization_membership.id,
            board_id=owner_board_membership.board_id,
        )

        self.assertTrue(
            BoardMembershipService().can_delete_member(
                user_id=owner_organization_membership.user_id,
                board_membership_id=admin_board_membership.id,
            )
        )

    def test_owner_can_delete_member(self):
        owner_organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        owner_board_membership = BoardMembershipFactory(organization_membership_id=owner_organization_membership.id)
        member_organization_membership = OrganizationMembershipFactory(
            organization_id=owner_organization_membership.organization_id,
        )
        member_board_membership = BoardMembershipFactory(
            organization_membership=member_organization_membership,
            board_id=owner_board_membership.board_id,
        )

        self.assertTrue(
            BoardMembershipService().can_delete_member(
                user_id=owner_organization_membership.user_id,
                board_membership_id=member_board_membership.id,
            )
        )

    def test_admin_can_delete_member(self):
        admin_organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.ADMIN)
        admin_board_membership = BoardMembershipFactory(organization_membership_id=admin_organization_membership.id)
        member_organization_membership = OrganizationMembershipFactory(
            organization_id=admin_organization_membership.organization_id,
        )
        member_board_membership = BoardMembershipFactory(
            organization_membership=member_organization_membership,
            board_id=admin_board_membership.board_id,
        )

        self.assertTrue(
            BoardMembershipService().can_delete_member(
                user_id=admin_organization_membership.user_id,
                board_membership_id=member_board_membership.id,
            )
        )

    def test_admin_can_not_delete_admin(self):
        admin_organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.ADMIN)
        admin_board_membership = BoardMembershipFactory(organization_membership_id=admin_organization_membership.id)
        other_admin_organization_membership = OrganizationMembershipFactory(
            organization_id=admin_organization_membership.organization_id,
            role=OrganizationMemberRole.ADMIN,
        )
        other_admin_board_membership = BoardMembershipFactory(
            organization_membership=other_admin_organization_membership,
            board_id=admin_board_membership.board_id,
        )

        self.assertFalse(
            BoardMembershipService().can_delete_member(
                user_id=admin_organization_membership.user_id,
                board_membership_id=other_admin_board_membership.id,
            )
        )

    def test_member_can_not_delete_admin(self):
        member_organization_membership = OrganizationMembershipFactory()
        member_board_membership = BoardMembershipFactory(organization_membership_id=member_organization_membership.id)
        admin_organization_membership = OrganizationMembershipFactory(
            organization_id=member_organization_membership.organization_id,
            role=OrganizationMemberRole.ADMIN,
        )
        admin_board_membership = BoardMembershipFactory(
            organization_membership_id=admin_organization_membership.id,
            board_id=member_board_membership.board_id,
        )

        self.assertFalse(
            BoardMembershipService().can_delete_member(
                user_id=member_organization_membership.user_id,
                board_membership_id=admin_board_membership.id,
            )
        )

    def test_member_can_not_delete_member(self):
        member_organization_membership = OrganizationMembershipFactory()
        member_board_membership = BoardMembershipFactory(organization_membership_id=member_organization_membership.id)
        other_member_organization_membership = OrganizationMembershipFactory(
            organization_id=member_organization_membership.organization_id,
        )
        other_member_board_membership = BoardMembershipFactory(
            organization_membership_id=other_member_organization_membership.id,
            board_id=member_board_membership.board_id,
        )

        self.assertFalse(
            BoardMembershipService().can_delete_member(
                user_id=member_organization_membership.user_id,
                board_membership_id=other_member_board_membership.id,
            )
        )

    def test_admin_not_on_board_can_not_delete_member(self):
        admin_organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.ADMIN)
        member_organization_membership = OrganizationMembershipFactory(
            organization_id=admin_organization_membership.organization_id,
        )
        member_board_membership = BoardMembershipFactory(organization_membership_id=member_organization_membership.id)

        self.assertFalse(
            BoardMembershipService().can_delete_member(
                user_id=admin_organization_membership.user_id,
                board_membership_id=member_board_membership.id,
            )
        )

    def test_member_not_on_board_can_not_delete_member(self):
        member_organization_membership = OrganizationMembershipFactory()
        other_member_organization_membership = OrganizationMembershipFactory(
            organization_id=member_organization_membership.organization_id,
        )
        other_member_board_membership = BoardMembershipFactory(
            organization_membership_id=other_member_organization_membership.id,
        )

        self.assertFalse(
            BoardMembershipService().can_delete_member(
                user_id=member_organization_membership.user_id,
                board_membership_id=other_member_board_membership.id,
            )
        )

    def test_random_user_can_not_delete_member(self):
        user = UserFactory()
        organization_membership = OrganizationMembershipFactory()
        board_membership = BoardMembershipFactory(organization_membership=organization_membership)

        self.assertFalse(
            BoardMembershipService().can_delete_member(
                user_id=user.id,
                board_membership_id=board_membership.id,
            )
        )
