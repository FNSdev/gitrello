from unittest.mock import patch

from django.test import TestCase

from boards.exceptions import BoardAlreadyExistsException
from boards.services import BoardService, BoardMembershipService
from boards.tests.factories import BoardFactory
from organizations.choices import OrganizationMemberRole
from organizations.exceptions import OrganizationNotFoundException
from organizations.tests.factories import OrganizationMembershipFactory


class TestBoardService(TestCase):
    def test_create_board(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)

        with patch.object(BoardMembershipService, 'create_board_membership') as mocked_add_member:
            board = BoardService.create_board(name='board', organization_id=organization_membership.organization_id)

        self.assertIsNotNone(board)
        self.assertEqual(board.name, 'board')
        self.assertEqual(board.organization.id, organization_membership.organization_id)
        mocked_add_member.assert_called_with(
            board_id=board.id,
            organization_membership_id=organization_membership.id,
        )

    def test_create_board_name_not_unique(self):
        organization_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        board = BoardFactory(
            organization_id=organization_membership.organization_id,
        )

        with self.assertRaises(BoardAlreadyExistsException):
            _ = BoardService.create_board(
                name=board.name,
                organization_id=organization_membership.organization_id
            )

    def test_create_board_organization_not_found(self):
        with self.assertRaises(OrganizationNotFoundException):
            _ = BoardService.create_board(name='board', organization_id=-1)
