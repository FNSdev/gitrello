import graphene
from graphene_django.views import GraphQLView
from graphql.error import GraphQLLocatedError
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.settings import api_settings

from authentication.api.graphql.schema import Query as AuthenticationQuery
from boards.api.graphql.schema import Query as BoardsQuery
from gitrello.exceptions import GITrelloException
from organizations.api.graphql.schema import Query as OrganizationsQuery
from tickets.api.graphql.schema import Query as TicketsQuery


class Query(
    AuthenticationQuery,
    BoardsQuery,
    OrganizationsQuery,
    TicketsQuery,
    graphene.ObjectType,
):
    pass


class DRFAuthenticatedGraphQLView(GraphQLView):
    def parse_body(self, request):
        if isinstance(request, Request):
            return request.data
        return super().parse_body(request)

    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super().as_view(*args, **kwargs)
        view = permission_classes((IsAuthenticated, ))(view)
        view = authentication_classes(api_settings.DEFAULT_AUTHENTICATION_CLASSES + [SessionAuthentication, ])(view)
        view = api_view(['GET', 'POST', ])(view)
        return view

    @classmethod
    def format_error(cls, error):
        if isinstance(error, GITrelloException):
            return {
                'error_code': error.code,
                'error_message': error.message,
            }

        if isinstance(error, GraphQLLocatedError) and isinstance(error.original_error, GITrelloException):
            return {
                'error_code': error.original_error.code,
                'error_message': error.original_error.message,
            }

        return super().format_error(error)


schema = graphene.Schema(query=Query)
