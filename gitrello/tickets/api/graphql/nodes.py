import graphene_django_optimizer as gql_optimizer
from graphene_django.types import DjangoObjectType

from gitrello.utils.graphql import GITrelloNode
from tickets.models import Category, Ticket, TicketAssignment


class CategoryNode(gql_optimizer.OptimizedDjangoObjectType):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'board',
            'tickets',
        )
        interfaces = (GITrelloNode, )


class TicketNode(DjangoObjectType):
    class Meta:
        model = Ticket
        fields = (
            'id',
            'added_at',
            'priority',
            'title',
            'body',
            'due_date',
            'category',
            'assignments',
        )
        interfaces = (GITrelloNode, )


class TicketAssignmentNode(DjangoObjectType):
    class Meta:
        model = TicketAssignment
        fields = (
            'id',
            'ticket',
            'assignee',
        )
        interfaces = (GITrelloNode, )
