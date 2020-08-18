from graphene_django.types import DjangoObjectType

from gitrello.utils.graphql import GITrelloNode
from tickets.models import Category, Comment, Ticket, TicketAssignment


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'board',
            'tickets',
        )
        interfaces = (GITrelloNode, )


class CommentNode(DjangoObjectType):
    class Meta:
        model = Comment
        fields = (
            'id',
            'added_at',
            'ticket',
            'author',
            'message',
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
            'comments',
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
