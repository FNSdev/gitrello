import graphene_django_optimizer as gql_optimizer
from graphene_django.types import DjangoObjectType

from boards.models import Board, BoardMembership
from gitrello.utils.graphql import GITrelloNode


class BoardNode(gql_optimizer.OptimizedDjangoObjectType):
    class Meta:
        model = Board
        fields = (
            'id',
            'name',
            'organization',
            'board_memberships',
            'categories',
        )
        interfaces = (GITrelloNode, )


class BoardMembershipNode(DjangoObjectType):
    class Meta:
        model = BoardMembership
        fields = (
            'id',
            'board',
            'organization_membership',
        )
        interfaces = (GITrelloNode, )
