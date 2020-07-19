from graphene_django.types import DjangoObjectType

from authentication.models import User
from gitrello.utils.graphql import GITrelloNode


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'organization_memberships',
        )
        interfaces = (GITrelloNode, )
