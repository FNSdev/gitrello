import graphene
import graphene_django_optimizer as gql_optimizer

from authentication.api.graphql.nodes import UserNode
from authentication.models import User
from gitrello.exceptions import PermissionDeniedException


class Query(graphene.ObjectType):
    user = graphene.Field(UserNode, id=graphene.String())

    def resolve_user(self, info, **kwargs):
        if not kwargs.get('id') == str(info.context.user.id):
            raise PermissionDeniedException

        return gql_optimizer.query(User.objects.filter(id=info.context.user.id), info).first()
