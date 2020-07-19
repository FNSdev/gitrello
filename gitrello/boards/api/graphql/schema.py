import graphene
import graphene_django_optimizer as gql_optimizer

from boards.api.graphql.connections import BoardConnection, BoardMembershipConnection
from boards.api.graphql.nodes import BoardNode, BoardMembershipNode
from boards.models import Board, BoardMembership
from gitrello.exceptions import PermissionDeniedException


class Query(graphene.ObjectType):
    boards = graphene.ConnectionField(BoardConnection)
    board = graphene.Field(BoardNode, id=graphene.String())

    board_memberships = graphene.ConnectionField(BoardMembershipConnection)
    board_membership = graphene.Field(BoardMembershipNode, id=graphene.String())

    def resolve_boards(self, info, **kwargs):
        return gql_optimizer.query(
            Board.objects.filter(board_memberships__organization_membership__user=info.context.user),
            info,
        )

    # TODO 403 or 404?
    def resolve_board(self, info, **kwargs):
        if not info.context.user.is_board_member(kwargs.get('id')):
            raise PermissionDeniedException

        return gql_optimizer.query(Board.objects.filter(id=kwargs.get('id')), info).first()

    def resolve_board_memberships(self, info, **kwargs):
        return gql_optimizer.query(
            BoardMembership.objects.filter(organization_membership__user=info.context.user),
            info,
        )

    def resolve_board_membership(self, info, **kwargs):
        return gql_optimizer \
            .query(
                BoardMembership.objects.filter(id=kwargs.get('id'), organization_membership__user=info.context.user),
                info,
            ) \
            .first()
