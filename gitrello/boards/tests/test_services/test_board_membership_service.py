from django.test import TestCase

from boards.exceptions import (
    BoardNotFoundException, BoardMembershipAlreadyExistsException, BoardMembershipNotFoundException,
    CanNotLeaveBoardException,
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

        board_membership = BoardMembershipService.create_board_membership(
            board_id=board.id,
            organization_membership_id=organization_membership.id,
        )

        self.assertIsNotNone(board_membership)
        self.assertEqual(board_membership.board.id, board.id)
        self.assertEqual(board_membership.organization_membership.id, organization_membership.id)

    def test_add_member_board_not_found(self):
        organization = OrganizationFactory()

        with self.assertRaises(BoardNotFoundException):
            _ = BoardMembershipService.create_board_membership(
                board_id=-1,
                organization_membership_id=organization.id,
            )

    def test_add_member_organization_membership_not_found(self):
        board = BoardFactory()

        with self.assertRaises(OrganizationMembershipNotFoundException):
            _ = BoardMembershipService.create_board_membership(board_id=board.id, organization_membership_id=-1)

    def test_add_member_membership_already_exists(self):
        board_membership = BoardMembershipFactory()

        with self.assertRaises(BoardMembershipAlreadyExistsException):
            _ = BoardMembershipService.create_board_membership(
                board_id=board_membership.board_id,
                organization_membership_id=board_membership.organization_membership_id,
            )

    def test_delete_member(self):
        board_membership = BoardMembershipFactory()
        BoardMembershipService.delete_board_membership(board_membership.id)

        self.assertIsNone(BoardMembership.objects.filter(id=board_membership.id).first())

    def test_delete_member_membership_not_found(self):
        with self.assertRaises(BoardMembershipNotFoundException):
            BoardMembershipService.delete_board_membership(-1)

    def test_delete_member_user_is_organization_owner(self):
        membership = BoardMembershipFactory(
            organization_membership=OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER),
        )

        with self.assertRaises(CanNotLeaveBoardException):
            BoardMembershipService.delete_board_membership(membership.id)
