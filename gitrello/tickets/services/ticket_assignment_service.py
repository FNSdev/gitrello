from django.db.transaction import atomic

from boards.exceptions import BoardMembershipNotFoundException
from boards.models import BoardMembership
from gitrello.handlers import retry_on_transaction_serialization_error
from tickets.exceptions import (
    TicketNotFoundException, TicketAssignmentNotFoundException, TicketAssignmentAlreadyExistsException,
)
from tickets.models import Ticket, TicketAssignment


class TicketAssignmentService:
    @retry_on_transaction_serialization_error
    @atomic
    def assign_member(self, ticket_id: int, board_membership_id: int) -> TicketAssignment:
        if not BoardMembership.objects.filter(id=board_membership_id).exists():
            raise BoardMembershipNotFoundException

        if not Ticket.objects.filter(id=ticket_id).exists():
            raise TicketNotFoundException

        if TicketAssignment.objects.filter(ticket_id=ticket_id, assignee_id=board_membership_id).exists():
            raise TicketAssignmentAlreadyExistsException

        return TicketAssignment.objects.create(
            ticket_id=ticket_id,
            assignee_id=board_membership_id,
        )

    @retry_on_transaction_serialization_error
    @atomic
    def unassign_member(self, ticket_assignment_id):
        ticket_assignment = TicketAssignment.objects.filter(id=ticket_assignment_id).first()
        if not ticket_assignment:
            raise TicketAssignmentNotFoundException

        ticket_assignment.delete()

    @retry_on_transaction_serialization_error
    def can_assign_member(self, user_id, ticket_id, board_membership_id):
        ticket = Ticket.objects.filter(id=ticket_id).values('category__board_id').first()
        if not ticket:
            return False

        # BoardMembership and Ticket belong to different boards
        if not BoardMembership.objects.filter(id=board_membership_id, board_id=ticket['category__board_id']).exists():
            return False

        # Check if user belongs to the same board as ticket & board_membership
        return BoardMembership.objects.filter(
            board_id=ticket['category__board_id'],
            organization_membership__user_id=user_id,
        ).exists()

    @retry_on_transaction_serialization_error
    @atomic
    def can_unassign_member(self, user_id, ticket_assignment_id):
        ticket_assignment = TicketAssignment.objects.filter(
            id=ticket_assignment_id,
        ).values(
            'ticket__category__board_id',
        ).first()

        if not ticket_assignment:
            return False

        return BoardMembership.objects.filter(
            board_id=ticket_assignment['ticket__category__board_id'],
            organization_membership__user_id=user_id,
        ).exists()
