import factory

from authentication.tests.factories import UserFactory
from organizations.models import Organization, OrganizationMembership, OrganizationInvite


class OrganizationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.sequence(lambda i: f'organization_{i}')


class OrganizationMembershipFactory(factory.DjangoModelFactory):
    class Meta:
        model = OrganizationMembership

    organization = factory.SubFactory(OrganizationFactory)
    user = factory.SubFactory(UserFactory)


class OrganizationInviteFactory(factory.DjangoModelFactory):
    class Meta:
        model = OrganizationInvite

    organization = factory.SubFactory(OrganizationFactory)
    user = factory.SubFactory(UserFactory)
    message = factory.sequence(lambda i: f'invite_{i}')
