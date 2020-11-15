from typing import Optional

from django.db.models import Case, F, When

from tickets.exceptions import CategoryNotFoundException, TicketNotFoundException
from tickets.models import Category, Ticket
from tickets.services import CategoryService


class TicketService:
    @classmethod
    def create_ticket(cls, category_id: int) -> Ticket:
        if not Category.objects.filter(id=category_id).exists():
            raise CategoryNotFoundException

        last_ticket = Ticket.objects \
            .filter(category_id=category_id) \
            .order_by('-priority') \
            .only('priority') \
            .first()

        return Ticket.objects.create(
            category_id=category_id,
            priority=last_ticket.priority + 1 if last_ticket else 0,
        )

    # TODO add tests
    @classmethod
    def create_ticket_from_github_issue(cls, board_id: int, title: str, body: str) -> Ticket:
        category = Category.objects \
            .filter(board_id=board_id) \
            .order_by('added_at') \
            .first()

        last_ticket = None
        if category:
            last_ticket = Ticket.objects \
                .filter(category_id=category.id) \
                .order_by('-priority') \
                .only('priority') \
                .first()
        else:
            category = CategoryService.create_category(CategoryService.NOT_SORTED, board_id)

        return Ticket.objects.create(
            category_id=category.id,
            title=title,
            body=body,
            priority=last_ticket.priority + 1 if last_ticket else 0,
        )

    @classmethod
    def update_ticket(cls, ticket_id: int, validated_data: dict) -> Ticket:
        ticket = Ticket.objects.filter(id=ticket_id).first()
        if not ticket:
            raise TicketNotFoundException

        ticket.title = validated_data['title']
        ticket.due_date = validated_data['due_date']
        ticket.body = validated_data['body']
        ticket.save()

        return ticket

    # TODO add tests
    @classmethod
    def delete_ticket(cls, ticket_id):
        ticket = Ticket.objects.filter(id=ticket_id).first()
        if not ticket:
            raise TicketNotFoundException

        Ticket.objects \
            .filter(category_id=ticket.category_id, priority__gt=ticket.priority) \
            .update(priority=F('priority') - 1)

        ticket.delete()

    # TODO add tests
    @classmethod
    def move_ticket(cls, ticket_id: int, insert_after_ticket_id: Optional[int], new_category_id: int) -> Ticket:
        ticket = Ticket.objects.filter(id=ticket_id).first()
        if not ticket:
            raise TicketNotFoundException

        if not insert_after_ticket_id:
            new_priority = 0
        else:
            previous_ticket = Ticket.objects.filter(id=insert_after_ticket_id).first()
            if not previous_ticket:
                raise TicketNotFoundException

            if ticket.category_id == new_category_id:
                if ticket.priority > previous_ticket.priority:
                    new_priority = previous_ticket.priority + 1
                else:
                    new_priority = previous_ticket.priority
            else:
                new_priority = previous_ticket.priority + 1

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
                .update(
                    priority=Case(
                        When(category_id=new_category_id, priority__gte=new_priority, then=F('priority') + 1),
                        When(category_id=ticket.category_id, priority__gt=ticket.priority, then=F('priority') - 1),
                        default=F('priority'),
                    )
                )

        ticket.category_id = new_category_id
        ticket.priority = new_priority
        ticket.save(update_fields=('priority', 'category_id'))

        return ticket
