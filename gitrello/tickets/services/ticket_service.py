from django.db.models import Subquery
from django.db.transaction import atomic

from boards.models import BoardMembership
from organizations.models import OrganizationMembership
from gitrello.handlers import retry_on_transaction_serialization_error
from tickets.exceptions import CategoryNotFoundException, TicketNotFoundException
from tickets.models import Category, Ticket


class TicketService:
    @retry_on_transaction_serialization_error
    @atomic
    def create_ticket(self, category_id: int) -> Ticket:
        if not Category.objects.filter(id=category_id).exists():
            raise CategoryNotFoundException

        return Ticket.objects.create(
            category_id=Subquery(Category.objects.filter(id=category_id).values('id')),
        )

    @retry_on_transaction_serialization_error
    @atomic
    def update_ticket(self, ticket_id: int, validated_data: dict) -> Ticket:
        ticket = Ticket.objects.filter(id=ticket_id).first()
        if not ticket:
            raise TicketNotFoundException

        for k, v in validated_data.items():
            setattr(ticket, k, v)

        ticket.save()
        return ticket

    @retry_on_transaction_serialization_error
    @atomic
    def can_create_ticket(self, user_id: int, category_id: int) -> bool:
        category = Category.objects.filter(id=category_id).values('board_id', 'board__organization_id').first()

        return BoardMembership.objects.filter(
            organization_membership_id=Subquery(
                OrganizationMembership.objects.filter(
                    organization_id=category['board__organization_id'],
                    user_id=user_id,
                ).values('id')
            ),
            board_id=category['board_id'],
        ).exists()

    @retry_on_transaction_serialization_error
    @atomic
    def can_update_ticket(self, user_id: int, ticket_id: int):
        ticket = Ticket.objects.filter(
            id=ticket_id
        ).values(
            'category__board_id',
            'category__board__organization_id',
        ).first()

        return BoardMembership.objects.filter(
            organization_membership_id=Subquery(
                OrganizationMembership.objects.filter(
                    organization_id=ticket['category__board__organization_id'],
                    user_id=user_id,
                ).values('id')
            ),
            board_id=ticket['category__board_id'],
        ).exists()
