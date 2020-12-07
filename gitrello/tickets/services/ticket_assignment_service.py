from boards.exceptions import BoardMembershipNotFoundException
from boards.models import BoardMembership
from tickets.exceptions import (
    TicketNotFoundException, TicketAssignmentNotFoundException, TicketAssignmentAlreadyExistsException,
)
from tickets.models import Ticket, TicketAssignment


class TicketAssignmentService:
    @classmethod
    def create_ticket_assignment(cls, ticket_id: int, board_membership_id: int) -> TicketAssignment:
        ticket = Ticket.objects \
            .filter(id=ticket_id) \
            .values('category__board_id') \
            .first()

        if not ticket:
            raise TicketNotFoundException

        exists = BoardMembership.objects \
            .filter(id=board_membership_id, board_id=ticket['category__board_id']) \
            .exists()

        if not exists:
            raise BoardMembershipNotFoundException

        if TicketAssignment.objects.filter(ticket_id=ticket_id, assignee_id=board_membership_id).exists():
            raise TicketAssignmentAlreadyExistsException

        return TicketAssignment.objects.create(
            ticket_id=ticket_id,
            assignee_id=board_membership_id,
        )

    @classmethod
    def delete_ticket_assignment(cls, ticket_assignment_id: int):
        ticket_assignment = TicketAssignment.objects.filter(id=ticket_assignment_id).first()
        if not ticket_assignment:
            raise TicketAssignmentNotFoundException

        ticket_assignment.delete()
