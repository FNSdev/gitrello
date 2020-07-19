import graphene

from boards.api.graphql.nodes import BoardNode, BoardMembershipNode


class BoardConnection(graphene.relay.Connection):
    class Meta:
        node = BoardNode


class BoardMembershipConnection(graphene.relay.Connection):
    class Meta:
        node = BoardMembershipNode
