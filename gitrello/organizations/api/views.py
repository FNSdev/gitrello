from rest_framework import views
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.exceptions import UserNotFoundException
from gitrello.exceptions import APIRequestValidationException
from organizations.api.serializers import CreateOrganizationSerializer, CreateOrganizationInviteSerializer
from organizations.exceptions import GITrelloOrganizationsException
from organizations.services import OrganizationService, OrganizationInviteService


class CreateOrganizationView(views.APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def post(self, request, *args, **kwargs):
        serializer = CreateOrganizationSerializer(data=request.data)
        if not serializer.is_valid():
            raise APIRequestValidationException(serializer_errors=serializer.errors)

        try:
            organization = OrganizationService().create_organization(owner=request.user, **serializer.validated_data)
        except GITrelloOrganizationsException as e:
            return Response(
                status=400,
                data={
                    'error_code': e.code,
                    'error_message': e.message,
                }
            )

        return Response(
            status=201,
            data={
                'id': organization.id,
                'name': organization.name,
            }
        )


class CreateOrganizationInviteView(views.APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def post(self, request, *args, **kwargs):
        serializer = CreateOrganizationInviteSerializer(data=request.data)
        if not serializer.is_valid():
            raise APIRequestValidationException(serializer_errors=serializer.errors)

        try:
            invite = OrganizationInviteService().send_invite(**serializer.validated_data)
        except (GITrelloOrganizationsException, UserNotFoundException) as e:
            return Response(
                status=400,
                data={
                    'error_code': e.code,
                    'error_message': e.message,
                }
            )

        return Response(
            status=201,
            data={
                'id': invite.id,
                'status': invite.get_status_display(),
            }
        )
