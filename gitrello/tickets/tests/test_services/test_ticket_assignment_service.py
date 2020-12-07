from django.test import TestCase

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

        ticket_assignment = TicketAssignmentService.create_ticket_assignment(
            ticket_id=ticket.id,
            board_membership_id=board_membership.id,
        )

        self.assertIsNotNone(ticket_assignment)
        self.assertEqual(ticket_assignment.ticket_id, ticket.id)
        self.assertEqual(ticket_assignment.assignee_id, board_membership.id)

    def test_assign_member_board_membership_not_found(self):
        ticket = TicketFactory()

        with self.assertRaises(BoardMembershipNotFoundException):
            _ = TicketAssignmentService.create_ticket_assignment(ticket_id=ticket.id, board_membership_id=-1)

    def test_assign_member_ticket_not_found(self):
        board_membership = BoardMembershipFactory()

        with self.assertRaises(TicketNotFoundException):
            _ = TicketAssignmentService.create_ticket_assignment(ticket_id=-1, board_membership_id=board_membership.id)

    def test_assign_member_already_assigned(self):
        ticket_assignment = TicketAssignmentFactory()

        with self.assertRaises(TicketAssignmentAlreadyExistsException):
            _ = TicketAssignmentService.create_ticket_assignment(
                ticket_id=ticket_assignment.ticket_id,
                board_membership_id=ticket_assignment.assignee_id,
            )

    def test_unassign_member(self):
        ticket_assignment = TicketAssignmentFactory()

        TicketAssignmentService.delete_ticket_assignment(ticket_assignment.id)
        self.assertIsNone(
            TicketAssignment.objects.filter(id=ticket_assignment.id).first()
        )

    def test_unassign_member_ticket_assignment_not_found(self):
        with self.assertRaises(TicketAssignmentNotFoundException):
            TicketAssignmentService.delete_ticket_assignment(-1)
