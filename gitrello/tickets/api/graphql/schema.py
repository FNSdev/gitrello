import graphene
import graphene_django_optimizer as gql_optimizer

from tickets.api.graphql.connections import CategoryConnection, TicketConnection, TicketAssignmentConnection
from tickets.api.graphql.nodes import CategoryNode, TicketNode, TicketAssignmentNode
from tickets.models import Category, Ticket, TicketAssignment


class Query(graphene.ObjectType):
    categories = graphene.ConnectionField(CategoryConnection)
    category = graphene.Field(CategoryNode, id=graphene.String())

    tickets = graphene.ConnectionField(TicketConnection)
    ticket = graphene.Field(TicketNode, id=graphene.String())

    ticket_assignments = graphene.ConnectionField(TicketAssignmentConnection)
    ticket_assignment = graphene.Field(TicketAssignmentNode, id=graphene.String())

    def resolve_categories(self, info, **kwargs):
        return gql_optimizer \
            .query(
                Category.objects.filter(board__members__user=info.context.user),
                info,
            )

    def resolve_category(self, info, **kwargs):
        return gql_optimizer \
            .query(
                Category.objects.filter(id=kwargs.get('id'), board__members__user=info.context.user),
                info,
            ) \
            .first()

    def resolve_tickets(self, info, **kwargs):
        return gql_optimizer \
            .query(
                Ticket.objects.filter(category__board__members__user=info.context.user),
                info,
            )

    def resolve_ticket(self, info, **kwargs):
        return gql_optimizer \
            .query(
                Ticket.objects.filter(id=kwargs.get('id'), category__board__members__user=info.context.user),
                info,
            ) \
            .first()

    def resolve_ticket_assignments(self, info, **kwargs):
        return gql_optimizer \
            .query(
                TicketAssignment.objects.filter(assignee__organization_membership__user=info.context.user),
                info,
            )

    def resolve_ticket_assignment(self, info, **kwargs):
        return gql_optimizer \
            .query(
                Ticket.objects.filter(id=kwargs.get('id'), category__board__members__user=info.context.user),
                info,
            ) \
            .first()
