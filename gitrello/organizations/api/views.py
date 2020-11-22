from django.db.transaction import atomic
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.services import PermissionsService
from gitrello.exceptions import PermissionDeniedException
from gitrello.handlers import retry_on_transaction_serialization_error
from gitrello.schema import gitrello_schema
from organizations.api.serializers import (
    CreateOrganizationSerializer, CreateOrganizationResponseSerializer, CreateOrganizationInviteSerializer,
    CreateOrganizationInviteResponseSerializer, UpdateOrganizationInviteSerializer,
    UpdateOrganizationMembershipResponseSerializer, UpdateOrganizationMembershipSerializer,
)
from organizations.services import OrganizationService, OrganizationInviteService, OrganizationMembershipService


class OrganizationsView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
    @gitrello_schema(
        query_serializer=CreateOrganizationSerializer, responses={201: CreateOrganizationResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = CreateOrganizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organization = OrganizationService.create_organization(owner_id=request.user.id, **serializer.validated_data)
        response_serializer = CreateOrganizationResponseSerializer(instance=organization)
        return Response(
            status=201,
            data=response_serializer.data,
        )


class OrganizationInvitesView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
    @gitrello_schema(
        query_serializer=CreateOrganizationInviteSerializer,
        responses={201: CreateOrganizationInviteResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = CreateOrganizationInviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        permissions = PermissionsService.get_organization_permissions(
            organization_id=serializer.validated_data['organization_id'],
            user_id=request.user.id,
        )
        if not permissions.can_mutate:
            raise PermissionDeniedException

        invite = OrganizationInviteService.create_organization_invite(**serializer.validated_data)
        response_serializer = CreateOrganizationInviteResponseSerializer(instance=invite)
        return Response(
            status=201,
            data=response_serializer.data,
        )


class OrganizationInviteView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
    @gitrello_schema(query_serializer=UpdateOrganizationInviteSerializer, responses={204: ''})
    def patch(self, request, *args, **kwargs):
        serializer = UpdateOrganizationInviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

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
    @gitrello_schema(responses={204: ''})
    def delete(self, request, *args, **kwargs):
        permissions = PermissionsService.get_organization_membership_permissions(
            organization_membership_id=kwargs['id'],
            user_id=request.user.id,
        )
        if not permissions.can_delete:
            raise PermissionDeniedException

        OrganizationMembershipService.delete_organization_membership(organization_membership_id=kwargs['id'])
        return Response(status=204)

    # TODO add tests
    @retry_on_transaction_serialization_error
    @atomic
    @gitrello_schema(
        request_body=UpdateOrganizationMembershipSerializer,
        responses={'200': UpdateOrganizationMembershipResponseSerializer},
    )
    def patch(self, request, *args, **kwargs):
        serializer = UpdateOrganizationMembershipSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        permissions = PermissionsService.get_organization_membership_permissions(
            organization_membership_id=kwargs['id'],
            user_id=request.user.id,
        )
        if not permissions.can_mutate:
            raise PermissionDeniedException

        organization_membership = OrganizationMembershipService.update_role(
            organization_membership_id=kwargs['id'],
            role=serializer.validated_data['role'],
        )

        response_serializer = UpdateOrganizationMembershipResponseSerializer(instance=organization_membership)
        return Response(
            status=200,
            data=response_serializer.data,
        )
