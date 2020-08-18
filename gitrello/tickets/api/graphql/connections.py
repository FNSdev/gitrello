import graphene

from tickets.api.graphql.nodes import CategoryNode, CommentNode, TicketNode, TicketAssignmentNode


class CategoryConnection(graphene.relay.Connection):
    class Meta:
        node = CategoryNode


class CommentConnection(graphene.relay.Connection):
    class Meta:
        node = CommentNode


class TicketConnection(graphene.relay.Connection):
    class Meta:
        node = TicketNode


class TicketAssignmentConnection(graphene.relay.Connection):
    class Meta:
        node = TicketAssignmentNode
