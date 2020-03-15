from django.test import TestCase

from boards.exceptions import BoardNotFoundException
from boards.tests.factories import BoardFactory, BoardMembershipFactory
from organizations.choices import OrganizationMemberRole
from organizations.tests.factories import OrganizationMembershipFactory
from tickets.services import CategoryService


class TestCategoryService(TestCase):
    def test_create_category(self):
        board = BoardFactory()

        category = CategoryService().create_category(
            name='category',
            board_id=board.id,
        )

        self.assertIsNotNone(category)
        self.assertEqual(category.name, 'category')
        self.assertEqual(category.board.id, board.id)

    def test_create_category_board_not_found(self):
        with self.assertRaises(BoardNotFoundException):
            _ = CategoryService().create_category(
                name='category',
                board_id=-1,
            )

    def test_owner_can_create_category(self):
        owner_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        board_membership = BoardMembershipFactory(organization_membership_id=owner_membership.id)

        self.assertTrue(
            CategoryService().can_create_category(
                user_id=owner_membership.user_id,
                board_id=board_membership.board_id,
            )
        )

    def test_admin_can_create_category(self):
        admin_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.ADMIN)
        board_membership = BoardMembershipFactory(organization_membership_id=admin_membership.id)

        self.assertTrue(
            CategoryService().can_create_category(
                user_id=admin_membership.user_id,
                board_id=board_membership.board_id,
            )
        )

    def test_member_can_create_category(self):
        member_membership = OrganizationMembershipFactory()
        board_membership = BoardMembershipFactory(organization_membership_id=member_membership.id)

        self.assertTrue(
            CategoryService().can_create_category(
                user_id=member_membership.user_id,
                board_id=board_membership.board_id,
            )
        )

    def test_user_not_on_board_can_not_create_category(self):
        pass
