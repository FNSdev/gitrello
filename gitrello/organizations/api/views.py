from django.db.transaction import atomic
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.services import PermissionsService
from gitrello.exceptions import APIRequestValidationException, PermissionDeniedException
from gitrello.handlers import retry_on_transaction_serialization_error
from organizations.api.serializers import (
    CreateOrganizationSerializer, CreateOrganizationInviteSerializer, UpdateOrganizationInviteSerializer,
)
from organizations.services import OrganizationService, OrganizationInviteService, OrganizationMembershipService


class OrganizationsView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
    def post(self, request, *args, **kwargs):
        serializer = CreateOrganizationSerializer(data=request.data)
        if not serializer.is_valid():
            raise APIRequestValidationException(serializer_errors=serializer.errors)

        organization = OrganizationService.create_organization(owner_id=request.user.id, **serializer.validated_data)
        return Response(
            status=201,
            data={
                'id': str(organization.id),
                'name': organization.name,
            },
        )


class OrganizationInvitesView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
    def post(self, request, *args, **kwargs):
        serializer = CreateOrganizationInviteSerializer(data=request.data)
        if not serializer.is_valid():
            raise APIRequestValidationException(serializer_errors=serializer.errors)

        permissions = PermissionsService.get_organization_permissions(
            organization_id=serializer.validated_data['organization_id'],
            user_id=request.user.id,
        )
        if not permissions.can_mutate:
            raise PermissionDeniedException

        invite = OrganizationInviteService.create_organization_invite(**serializer.validated_data)
        return Response(
            status=201,
            data={
                'id': str(invite.id),
                'user_id': invite.user.id,
                'organization_id': invite.organization.id,
                'message': invite.message,
            },
        )


class OrganizationInviteView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
    def patch(self, request, *args, **kwargs):
        serializer = UpdateOrganizationInviteSerializer(data=request.data)
        if not serializer.is_valid():
            raise APIRequestValidationException(serializer_errors=serializer.errors)

        permissions = PermissionsService.get_organization_invite_permissions(
            organization_invite_id=kwargs['id'],
            user_id=request.user.id,
        )
        if not permissions.can_mutate or not permissions.can_delete:
            raise PermissionDeniedException

        OrganizationInviteService.accept_or_decline_invite(organization_invite_id=kwargs['id'], **serializer.validated_data)
        return Response(status=204)


class OrganizationMembershipView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
    def delete(self, request, *args, **kwargs):
        permissions = PermissionsService.get_organization_membership_permissions(
            organization_membership_id=kwargs['id'],
            user_id=request.user.id,
        )
        if not permissions.can_delete:
            raise PermissionDeniedException

        OrganizationMembershipService.delete_organization_membership(organization_membership_id=kwargs['id'])
        return Response(status=204)
