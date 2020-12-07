from boards.exceptions import BoardMembershipNotFoundException
from boards.models import BoardMembership
from tickets.exceptions import TicketNotFoundException
from tickets.models import Comment, Ticket


class CommentService:
    @classmethod
    def create_comment(cls, ticket_id: int, user_id: int, message: str) -> Comment:
        ticket = Ticket.objects \
            .filter(id=ticket_id) \
            .values('category__board_id') \
            .first()

        if not ticket:
            raise TicketNotFoundException

        board_membership = BoardMembership.objects \
            .filter(organization_membership__user_id=user_id, board_id=ticket['category__board_id']) \
            .values('id') \
            .first()

        if not board_membership:
            raise BoardMembershipNotFoundException

        comment = Comment.objects.create(
            ticket_id=ticket_id,
            author_id=board_membership['id'],
            message=message,
        )

        return comment
