import graphene

from organizations.api.graphql.nodes import OrganizationNode, OrganizationInviteNode, OrganizationMembershipNode


class OrganizationConnection(graphene.relay.Connection):
    class Meta:
        node = OrganizationNode


class OrganizationInviteConnection(graphene.relay.Connection):
    class Meta:
        node = OrganizationInviteNode


class OrganizationMembershipConnection(graphene.relay.Connection):
    class Meta:
        node = OrganizationMembershipNode
