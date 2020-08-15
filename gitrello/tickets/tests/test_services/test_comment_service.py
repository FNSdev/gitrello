from django.test import TestCase

from authentication.tests.factories import UserFactory
from boards.exceptions import BoardMembershipNotFoundException
from boards.tests.factories import BoardMembershipFactory, BoardFactory
from organizations.choices import OrganizationMemberRole
from organizations.tests.factories import OrganizationMembershipFactory
from tickets.services import CommentService
from tickets.exceptions import TicketNotFoundException
from tickets.tests.factories import CategoryFactory, TicketFactory


class TestCommentService(TestCase):
    def test_create_comment(self):
        ticket = TicketFactory()
        board_membership = BoardMembershipFactory(board_id=ticket.category.board_id)

        comment = CommentService().create_comment(
            ticket_id=ticket.id,
            user_id=board_membership.organization_membership.user_id,
            message='test_message',
        )

        self.assertIsNotNone(ticket)
        self.assertEqual(comment.message, 'test_message')
        self.assertEqual(comment.ticket_id, ticket.id)
        self.assertEqual(comment.author_id, board_membership.id)

    def test_create_comment_ticket_not_found(self):
        board_membership = BoardMembershipFactory()

        with self.assertRaises(TicketNotFoundException):
            _ = CommentService().create_comment(
                ticket_id=-1,
                user_id=board_membership.organization_membership.user_id,
                message='test_message',
            )

    def test_create_comment_board_membership_not_found(self):
        ticket = TicketFactory()

        with self.assertRaises(BoardMembershipNotFoundException):
            _ = CommentService().create_comment(
                ticket_id=ticket.id,
                user_id=-1,
                message='test_message',
            )

    def test_owner_can_create_comment(self):
        owner_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.OWNER)
        board_membership = BoardMembershipFactory(organization_membership_id=owner_membership.id)
        ticket = TicketFactory(category=CategoryFactory(board_id=board_membership.board_id))

        self.assertTrue(
            CommentService().can_create_comment(
                user_id=owner_membership.user_id,
                ticket_id=ticket.id,
            )
        )

    def test_admin_can_create_comment(self):
        admin_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.ADMIN)
        board_membership = BoardMembershipFactory(organization_membership_id=admin_membership.id)
        ticket = TicketFactory(category=CategoryFactory(board_id=board_membership.board_id))

        self.assertTrue(
            CommentService().can_create_comment(
                user_id=admin_membership.user_id,
                ticket_id=ticket.id,
            )
        )

    def test_member_can_create_comment(self):
        member_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.MEMBER)
        board_membership = BoardMembershipFactory(organization_membership_id=member_membership.id)
        ticket = TicketFactory(category=CategoryFactory(board_id=board_membership.board_id))

        self.assertTrue(
            CommentService().can_create_comment(
                user_id=member_membership.user_id,
                ticket_id=ticket.id,
            )
        )

    def test_user_not_on_board_can_not_create_comment(self):
        member_membership = OrganizationMembershipFactory(role=OrganizationMemberRole.MEMBER)
        board = BoardFactory(organization=member_membership.organization)
        ticket = TicketFactory(category=CategoryFactory(board=board))

        self.assertFalse(
            CommentService().can_create_comment(
                user_id=UserFactory().id,
                ticket_id=ticket.id,
            )
        )

    def test_random_user_can_not_create_comment(self):
        ticket = TicketFactory()

        self.assertFalse(
            CommentService().can_create_comment(
                user_id=UserFactory().id,
                ticket_id=ticket.id,
            )
        )
