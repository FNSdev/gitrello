from django.db.models import Case, F, Subquery, When, Value
from django.db.transaction import atomic

from boards.models import BoardMembership
from gitrello.handlers import retry_on_transaction_serialization_error
from tickets.exceptions import CategoryNotFoundException, TicketNotFoundException
from tickets.models import Category, Ticket


class TicketService:
    @retry_on_transaction_serialization_error
    @atomic
    def create_ticket(self, category_id: int) -> Ticket:
        if not Category.objects.filter(id=category_id).exists():
            raise CategoryNotFoundException

        ticket = Ticket.objects.filter(category_id=category_id).order_by('-priority').only('priority').first()

        return Ticket.objects.create(
            category_id=Subquery(Category.objects.filter(id=category_id).values('id')),
            priority=ticket.priority + 1 if ticket else 0,
        )

    @retry_on_transaction_serialization_error
    @atomic
    def update_ticket(self, ticket_id: int, validated_data: dict) -> Ticket:
        ticket = Ticket.objects.filter(id=ticket_id).first()
        if not ticket:
            raise TicketNotFoundException

        if (new_category_id := validated_data.get('category_id')) is not None:
            new_priority = validated_data.get('priority')
            if ticket.category_id == new_category_id:
                if ticket.priority < new_priority:
                    Ticket.objects \
                        .filter(
                            category_id=ticket.category_id,
                            priority__gt=ticket.priority,
                            priority__lte=new_priority,
                        ) \
                        .update(priority=F('priority') - 1)
                else:
                    Ticket.objects \
                        .filter(
                            category_id=ticket.category_id,
                            priority__lt=ticket.priority,
                            priority__gte=new_priority,
                        ) \
                        .update(priority=F('priority') + 1)
            else:
                Ticket.objects \
                    .update(priority=Case(
                        When(category_id=new_category_id, priority__gte=new_priority, then=F('priority') + 1),
                        When(category_id=ticket.category_id, priority__gt=ticket.priority, then=F('priority') - 1),
                        default=F('priority'),
                    ))

            ticket.category_id = validated_data['category_id']
            ticket.priority = validated_data['priority']

        ticket.title = validated_data['title']
        ticket.due_date = validated_data['due_date']
        ticket.body = validated_data['body']

        ticket.save()
        return ticket

    @retry_on_transaction_serialization_error
    @atomic
    def can_create_ticket(self, user_id: int, category_id: int) -> bool:
        category = Category.objects.filter(id=category_id).values('board_id').first()
        if not category:
            return False  # TODO add tests

        return BoardMembership.objects.filter(
            organization_membership__user_id=user_id,
            board_id=category['board_id'],
        ).exists()

    @retry_on_transaction_serialization_error
    @atomic
    def can_update_ticket(self, user_id: int, ticket_id: int) -> bool:
        ticket = Ticket.objects.filter(id=ticket_id).values('category__board_id').first()
        if not ticket:
            return False

        return BoardMembership.objects.filter(
            organization_membership__user_id=user_id,
            board_id=ticket['category__board_id'],
        ).exists()
