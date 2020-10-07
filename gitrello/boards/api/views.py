from django.db.transaction import atomic
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.api.serializers import PermissionsSerializer
from authentication.services import PermissionsService
from boards.api.serializers import (
    CreateBoardSerializer, CreateBoardMembershipSerializer, GetBoardPermissionsSerializer,
    CreateBoardMembershipResponseSerializer, CreateBoardResponseSerializer,
)
from boards.services import BoardService, BoardMembershipService
from gitrello.exceptions import PermissionDeniedException
from gitrello.handlers import retry_on_transaction_serialization_error
from gitrello.schema import gitrello_schema


class BoardsView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
    @gitrello_schema(query_serializer=CreateBoardSerializer, responses={201: CreateBoardResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = CreateBoardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        permissions = PermissionsService.get_organization_permissions(
            organization_id=serializer.validated_data['organization_id'],
            user_id=request.user.id,
        )
        if not permissions.can_mutate:
            raise PermissionDeniedException

        board = BoardService.create_board(**serializer.validated_data)
        response_serializer = CreateBoardResponseSerializer(instance=board)
        return Response(
            status=201,
            data=response_serializer.data,
        )


class BoardMembershipsView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
    @gitrello_schema(
        query_serializer=CreateBoardMembershipSerializer,
        responses={201: CreateBoardMembershipResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = CreateBoardMembershipSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        permissions = PermissionsService.get_board_permissions(
            board_id=serializer.validated_data['board_id'],
            user_id=request.user.id,
        )
        if not permissions.can_mutate:
            raise PermissionDeniedException

        board_membership = BoardMembershipService.create_board_membership(**serializer.validated_data)
        response_serializer = CreateBoardMembershipResponseSerializer(instance=board_membership)
        return Response(
            status=201,
            data=response_serializer.data,
        )


class BoardMembershipView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
    @gitrello_schema(responses={204: ''})
    def delete(self, request, *args, **kwargs):
        permissions = PermissionsService.get_board_membership_permissions(
            board_membership_id=kwargs['id'],
            user_id=request.user.id,
        )
        if not permissions.can_delete:
            raise PermissionDeniedException

        BoardMembershipService.delete_board_membership(board_membership_id=kwargs['id'])
        return Response(status=204)


class BoardPermissionsView(views.APIView):
    @retry_on_transaction_serialization_error
    @atomic
    @gitrello_schema(
        operation_id='board-permissions_details',
        query_serializer=GetBoardPermissionsSerializer,
        responses={200: PermissionsSerializer, 401: None, 403: None},
    )
    def get(self, request, *args, **kwargs):
        serializer = GetBoardPermissionsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        permissions = PermissionsService.get_board_permissions(**serializer.validated_data)
        return Response(status=200, data=permissions.to_json())
