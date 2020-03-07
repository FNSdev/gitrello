from rest_framework import views
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from gitrello.exceptions import APIRequestValidationException
from organizations.api.serializers import (
    CreateOrganizationSerializer, CreateOrganizationInviteSerializer, UpdateOrganizationInviteSerializer,
)
from organizations.services import OrganizationService, OrganizationInviteService, OrganizationMembershipService


class OrganizationView(views.APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def post(self, request, *args, **kwargs):
        serializer = CreateOrganizationSerializer(data=request.data)
        if not serializer.is_valid():
            raise APIRequestValidationException(serializer_errors=serializer.errors)

        organization = OrganizationService().create_organization(owner=request.user, **serializer.validated_data)
        return Response(
            status=201,
            data={
                'id': organization.id,
                'name': organization.name,
            }
        )


class OrganizationInviteView(views.APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def post(self, request, *args, **kwargs):
        serializer = CreateOrganizationInviteSerializer(data=request.data)
        if not serializer.is_valid():
            raise APIRequestValidationException(serializer_errors=serializer.errors)

        invite = OrganizationInviteService().send_invite(auth_user_id=request.user.id, **serializer.validated_data)
        return Response(
            status=201,
            data={
                'id': invite.id,
                'status': invite.get_status_display(),
            }
        )

    def put(self, request, *args, **kwargs):
        serializer = UpdateOrganizationInviteSerializer(data=request.data)
        if not serializer.is_valid():
            raise APIRequestValidationException(serializer_errors=serializer.errors)

        invite = OrganizationInviteService().update_invite(
            auth_user_id=request.user.id,
            organization_invite_id=kwargs['id'],
            **serializer.validated_data,
        )
        return Response(
            status=200,
            data={
                'id': invite.id,
                'status': invite.get_status_display(),
            }
        )


class OrganizationMembershipView(views.APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def delete(self, request, *args, **kwargs):
        OrganizationMembershipService().delete_member(
            auth_user_id=request.user.id,
            organization_membership_id=kwargs['id'],
        )
        return Response(status=204)
