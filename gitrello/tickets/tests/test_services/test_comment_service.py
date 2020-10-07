from django.test import TestCase

from boards.exceptions import BoardMembershipNotFoundException
from boards.tests.factories import BoardMembershipFactory
from tickets.services import CommentService
from tickets.exceptions import TicketNotFoundException
from tickets.tests.factories import TicketFactory


class TestCommentService(TestCase):
    def test_create_comment(self):
        ticket = TicketFactory()
        board_membership = BoardMembershipFactory(board_id=ticket.category.board_id)

        comment = CommentService.create_comment(
            ticket_id=ticket.id,
            user_id=board_membership.organization_membership.user_id,
            message='test_message',
        )

        self.assertIsNotNone(comment)
        self.assertEqual(comment.message, 'test_message')
        self.assertEqual(comment.ticket_id, ticket.id)
        self.assertEqual(comment.author_id, board_membership.id)

    def test_create_comment_ticket_not_found(self):
        board_membership = BoardMembershipFactory()

        with self.assertRaises(TicketNotFoundException):
            _ = CommentService.create_comment(
                ticket_id=-1,
                user_id=board_membership.organization_membership.user_id,
                message='test_message',
            )

    def test_create_comment_board_membership_not_found(self):
        ticket = TicketFactory()

        with self.assertRaises(BoardMembershipNotFoundException):
            _ = CommentService.create_comment(
                ticket_id=ticket.id,
                user_id=-1,
                message='test_message',
            )
