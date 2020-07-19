import graphene
import graphene_django_optimizer as gql_optimizer

from organizations.api.graphql.connections import (
    OrganizationConnection, OrganizationInviteConnection, OrganizationMembershipConnection,
)
from organizations.api.graphql.nodes import OrganizationNode, OrganizationInviteNode, OrganizationMembershipNode
from organizations.models import Organization, OrganizationInvite, OrganizationMembership
from gitrello.exceptions import PermissionDeniedException


class Query(graphene.ObjectType):
    organizations = graphene.ConnectionField(OrganizationConnection)
    organization = graphene.Field(OrganizationNode, id=graphene.String())

    organization_invites = graphene.ConnectionField(OrganizationInviteConnection)
    organization_invite = graphene.Field(OrganizationInviteNode, id=graphene.String())

    organization_memberships = graphene.ConnectionField(OrganizationMembershipConnection)
    organization_membership = graphene.Field(OrganizationMembershipNode, id=graphene.String())

    def resolve_organizations(self, info, **kwargs):
        return gql_optimizer.query(Organization.objects.filter(members=info.context.user), info)

    # TODO 403 or 404?
    def resolve_organization(self, info, **kwargs):
        if not info.context.user.is_organization_member(kwargs.get('id')):
            raise PermissionDeniedException

        return gql_optimizer.query(Organization.objects.filter(id=kwargs.get('id')), info).first()

    def resolve_organization_invites(self, info, **kwargs):
        return gql_optimizer.query(OrganizationInvite.objects.filter(user=info.context.user), info)

    def resolve_organization_invite(self, info, **kwargs):
        return gql_optimizer \
            .query(
                OrganizationInvite.objects.filter(id=kwargs.get('id'), user=info.context.user),
                info,
            ) \
            .first()

    def resolve_organization_memberships(self, info, **kwargs):
        return gql_optimizer.query(OrganizationMembership.objects.filter(user=info.context.user), info)

    def resolve_organization_membership(self, info, **kwargs):
        return gql_optimizer \
            .query(
                OrganizationMembership.objects.filter(id=kwargs.get('id'), user=info.context.user),
                info,
            ) \
            .first()
