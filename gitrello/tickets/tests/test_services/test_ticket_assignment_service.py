from django.test import TestCase

from authentication.tests.factories import UserFactory
from boards.exceptions import BoardMembershipNotFoundException
from boards.tests.factories import BoardMembershipFactory
from tickets.exceptions import (
    TicketNotFoundException, TicketAssignmentAlreadyExistsException, TicketAssignmentNotFoundException,
)
from tickets.models import TicketAssignment
from tickets.services import TicketAssignmentService
from tickets.tests.factories import TicketAssignmentFactory, TicketFactory


class TestTicketAssignmentService(TestCase):
    def test_assign_member(self):
        board_membership = BoardMembershipFactory()
        ticket = TicketFactory(category__board_id=board_membership.board_id)

        ticket_assignment = TicketAssignmentService().assign_member(
            ticket_id=ticket.id,
            board_membership_id=board_membership.id,
        )

        self.assertIsNotNone(ticket_assignment)
        self.assertEqual(ticket_assignment.ticket_id, ticket.id)
        self.assertEqual(ticket_assignment.assignee_id, board_membership.id)

    def test_assign_member_board_membership_not_found(self):
        ticket = TicketFactory()

        with self.assertRaises(BoardMembershipNotFoundException):
            _ = TicketAssignmentService().assign_member(ticket_id=ticket.id, board_membership_id=-1)

    def test_assign_member_ticket_not_found(self):
        board_membership = BoardMembershipFactory()

        with self.assertRaises(TicketNotFoundException):
            _ = TicketAssignmentService().assign_member(ticket_id=-1, board_membership_id=board_membership.id)

    def test_assign_member_already_assigned(self):
        ticket_assignment = TicketAssignmentFactory()

        with self.assertRaises(TicketAssignmentAlreadyExistsException):
            _ = TicketAssignmentService().assign_member(
                ticket_id=ticket_assignment.ticket_id,
                board_membership_id=ticket_assignment.assignee_id,
            )

    def test_unassign_member(self):
        ticket_assignment = TicketAssignmentFactory()

        TicketAssignmentService().unassign_member(ticket_assignment.id)
        self.assertIsNone(
            TicketAssignment.objects.filter(id=ticket_assignment.id).first()
        )

    def test_unassign_member_ticket_assignment_not_found(self):
        with self.assertRaises(TicketAssignmentNotFoundException):
            TicketAssignmentService().unassign_member(-1)

    def test_board_member_can_assign_himself(self):
        board_membership = BoardMembershipFactory()
        ticket = TicketFactory(category__board_id=board_membership.board_id)

        self.assertTrue(
            TicketAssignmentService().can_assign_member(
                user_id=board_membership.organization_membership.user_id,
                ticket_id=ticket.id,
                board_membership_id=board_membership.id,
            )
        )

    def test_board_member_can_assign_other_board_member(self):
        board_membership = BoardMembershipFactory()
        other_board_membership = BoardMembershipFactory(board_id=board_membership.board_id)
        ticket = TicketFactory(category__board_id=board_membership.board_id)

        self.assertTrue(
            TicketAssignmentService().can_assign_member(
                user_id=board_membership.organization_membership.user_id,
                ticket_id=ticket.id,
                board_membership_id=other_board_membership.id,
            )
        )

    def test_can_not_assign_not_a_board_member(self):
        board_membership = BoardMembershipFactory()
        other_board_membership = BoardMembershipFactory(board__organization_id=board_membership.board.organization_id)
        ticket = TicketFactory(category__board_id=board_membership.board_id)

        self.assertFalse(
            TicketAssignmentService().can_assign_member(
                user_id=board_membership.organization_membership.user_id,
                ticket_id=ticket.id,
                board_membership_id=other_board_membership.id,
            )
        )

    def test_not_a_board_member_can_not_assign_board_member(self):
        board_membership = BoardMembershipFactory()
        other_board_membership = BoardMembershipFactory(board__organization_id=board_membership.board.organization_id)
        ticket = TicketFactory(category__board_id=other_board_membership.board_id)

        self.assertFalse(
            TicketAssignmentService().can_assign_member(
                user_id=board_membership.organization_membership.user_id,
                ticket_id=ticket.id,
                board_membership_id=other_board_membership.id,
            )
        )

    def test_random_user_can_not_assign_board_member(self):
        board_membership = BoardMembershipFactory()
        ticket = TicketFactory(category__board_id=board_membership.board_id)

        self.assertFalse(
            TicketAssignmentService().can_assign_member(
                user_id=UserFactory().id,
                ticket_id=ticket.id,
                board_membership_id=board_membership.id,
            )
        )

    def test_can_assign_member_ticket_not_found(self):
        self.assertFalse(
            TicketAssignmentService().can_assign_member(
                ticket_id=-1,
                user_id=UserFactory().id,
                board_membership_id=BoardMembershipFactory(),
            )
        )

    def test_can_assign_member_board_membership_not_found(self):
        self.assertFalse(
            TicketAssignmentService().can_assign_member(
                ticket_id=TicketFactory().id,
                user_id=UserFactory().id,
                board_membership_id=-1,
            )
        )

    def test_board_member_can_unassign_himself(self):
        ticket_assignment = TicketAssignmentFactory()

        self.assertTrue(
            TicketAssignmentService().can_unassign_member(
                user_id=ticket_assignment.assignee.organization_membership.user_id,
                ticket_assignment_id=ticket_assignment.id,
            )
        )

    def test_board_member_can_unassign_other_board_member(self):
        ticket_assignment = TicketAssignmentFactory()
        other_board_membership = BoardMembershipFactory(board_id=ticket_assignment.assignee.board_id)

        self.assertTrue(
            TicketAssignmentService().can_unassign_member(
                user_id=other_board_membership.organization_membership.user_id,
                ticket_assignment_id=ticket_assignment.id,
            )
        )

    def test_not_a_board_member_can_not_unassign_board_member(self):
        ticket_assignment = TicketAssignmentFactory()
        other_board_membership = BoardMembershipFactory(
            board__organization_id=ticket_assignment.assignee.board.organization_id,
        )

        self.assertFalse(
            TicketAssignmentService().can_unassign_member(
                user_id=other_board_membership.organization_membership.user_id,
                ticket_assignment_id=ticket_assignment.id,
            )
        )

    def test_random_user_can_not_unassign_board_member(self):
        self.assertFalse(
            TicketAssignmentService().can_unassign_member(
                user_id=UserFactory().id,
                ticket_assignment_id=TicketAssignmentFactory().id,
            )
        )

    def test_can_unassign_member_ticket_assignment_not_found(self):
        self.assertFalse(
            TicketAssignmentService().can_unassign_member(
                user_id=UserFactory().id,
                ticket_assignment_id=-1,
            )
        )
