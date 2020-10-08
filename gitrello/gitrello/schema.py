import graphene
from drf_yasg.openapi import Response
from drf_yasg.utils import swagger_auto_schema
from graphene_django.views import GraphQLView
from graphql.error import GraphQLLocatedError
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.settings import api_settings

from authentication.api.graphql.schema import Query as AuthenticationQuery
from boards.api.graphql.schema import Query as BoardsQuery
from gitrello.exceptions import (
    APIRequestValidationException, AuthenticationFailedException, GITrelloException, PermissionDeniedException,
)
from gitrello.serializers import ErrorResponseSerializer
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


def gitrello_schema(**kwargs):
    responses = kwargs.pop('responses', {})
    if 400 not in responses:
        responses[400] = Response(
            schema=ErrorResponseSerializer,
            description='Given request is invalid for some reason',
            examples={
                'application/json': {
                    'error_code': APIRequestValidationException.code,
                    'error_message': APIRequestValidationException.message,
                    'error_details': {
                        'name': ['This field is required.', ],
                        'age': ['Not a valid integer', ],
                    }
                }
            }
        )
    if 401 not in responses:
        responses[401] = Response(
            schema=ErrorResponseSerializer,
            description='Authentication credentials were not provided or are incorrect',
            examples={
                'application/json': {
                    'error_code': AuthenticationFailedException.code,
                    'error_message': AuthenticationFailedException.message,
                    'error_details': {
                        'error': 'Authentication credentials were not provided.'
                    }
                },
            }
        )
    if 403 not in responses:
        responses[403] = Response(
            schema=ErrorResponseSerializer,
            description='User is authenticated, but not authorized to perform some action or access some data',
            examples={
                'application/json': {
                    'error_code': PermissionDeniedException.code,
                    'error_message': PermissionDeniedException.message,
                },
            }
        )

    security = kwargs.pop('security', None)
    if security is None:
        security = [{
            'Bearer': [],
        }]

    return swagger_auto_schema(
        responses=responses,
        security=security,
        **kwargs,
    )
