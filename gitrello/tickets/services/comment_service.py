from django.db.transaction import atomic

from boards.exceptions import BoardMembershipNotFoundException
from boards.models import BoardMembership
from gitrello.handlers import retry_on_transaction_serialization_error
from tickets.exceptions import TicketNotFoundException
from tickets.models import Comment, Ticket


class CommentService:
    @retry_on_transaction_serialization_error
    @atomic
    def create_comment(self, ticket_id: int, user_id: int, message: str) -> Comment:
        ticket = Ticket.objects \
            .filter(id=ticket_id) \
            .values('category__board_id') \
            .first()

        if not ticket:
            raise TicketNotFoundException

        board_membership = BoardMembership.objects \
            .filter(organization_membership__user_id=user_id, board_id=ticket['category__board_id']) \
            .first()

        if not board_membership:
            raise BoardMembershipNotFoundException

        comment = Comment.objects.create(
            ticket_id=ticket_id,
            author_id=board_membership.id,
            message=message,
        )

        return comment

    @retry_on_transaction_serialization_error
    @atomic
    def can_create_comment(self, ticket_id: int, user_id: int) -> bool:
        return Ticket.objects \
            .filter(
                id=ticket_id,
                category__board__members__user_id=user_id,
            ) \
            .exists()
