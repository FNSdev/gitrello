from unittest.mock import patch

from django.test import TestCase

from boards.services import BoardService, BoardMembershipService
from organizations.choices import OrganizationMemberRole
from organizations.exceptions import OrganizationNotFoundException
from organizations.tests.factories import OrganizationMembershipFactory


class TestBoardService(TestCase):
    def test_create_board(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)

        with patch.object(BoardMembershipService, 'add_member') as mocked_add_member:
            board = BoardService().create_board(name='board', organization_id=organization_membership.organization_id)

        self.assertIsNotNone(board)
        self.assertEqual(board.name, 'board')
        self.assertEqual(board.organization.id, organization_membership.organization_id)
        mocked_add_member.assert_called_with(
            board_id=board.id,
            organization_membership_id=organization_membership.id,
        )

    def test_create_board_organization_not_found(self):
        with self.assertRaises(OrganizationNotFoundException):
            _ = BoardService().create_board(name='board', organization_id=-1)

    def test_owner_can_create_board(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)

        self.assertTrue(
            BoardService().can_create_board(
                organization_id=organization_membership.organization_id,
                user_id=organization_membership.user_id,
            )
        )

    def test_admin_can_not_create_board(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.ADMIN)

        self.assertFalse(
            BoardService().can_create_board(
                organization_id=organization_membership.organization_id,
                user_id=organization_membership.user_id,
            )
        )

    def test_member_can_not_create_board(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.MEMBER)

        self.assertFalse(
            BoardService().can_create_board(
                organization_id=organization_membership.organization_id,
                user_id=organization_membership.user_id,
            )
        )
