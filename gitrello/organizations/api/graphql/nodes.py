import graphene
import graphene_django_optimizer as gql_optimizer
from django.db.models import Prefetch
from graphene_django.types import DjangoObjectType

from boards.models import Board
from gitrello.utils.graphql import GITrelloNode
from organizations.models import Organization, OrganizationInvite, OrganizationMembership


class OrganizationNode(gql_optimizer.OptimizedDjangoObjectType):
    class Meta:
        model = Organization
        fields = (
            'id',
            'name',
            'organization_memberships',
            'boards',
        )
        interfaces = (GITrelloNode, )

    @gql_optimizer.resolver_hints(
        prefetch_related=lambda info: Prefetch(
            'boards',
            queryset=gql_optimizer.query(Board.objects.filter(members__user_id=info.context.user.id), info),
            to_attr='visible_boards',
        ),
    )
    def resolve_boards(root, info):
        return getattr(root, 'visible_boards')


class OrganizationInviteNode(DjangoObjectType):
    class Meta:
        model = OrganizationInvite
        fields = (
            'id',
            'added_at',
            'organization_name',
            'user',
            'status',
            'message',
        )
        interfaces = (GITrelloNode, )

    organization_name = graphene.String()

    @gql_optimizer.resolver_hints(
        select_related=('organization', ),
        only=('organization__name', ),
    )
    def resolve_organization_name(root, info):
        return root.organization.name


class OrganizationMembershipNode(DjangoObjectType):
    class Meta:
        model = OrganizationMembership
        fields = (
            'id',
            'organization',
            'user',
            'role',
            'board_memberships',
        )
        interfaces = (GITrelloNode, )
