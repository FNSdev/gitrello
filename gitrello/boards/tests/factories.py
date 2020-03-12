import factory

from boards.models import Board, BoardMembership
from organizations.tests.factories import OrganizationFactory, OrganizationMembershipFactory


class BoardFactory(factory.DjangoModelFactory):
    class Meta:
        model = Board

    name = factory.sequence(lambda i: f'board_{i}')
    organization = factory.SubFactory(OrganizationFactory)


class BoardMembershipFactory(factory.DjangoModelFactory):
    class Meta:
        model = BoardMembership

    board = factory.SubFactory(BoardFactory)
    organization_membership = factory.SubFactory(OrganizationMembershipFactory)
