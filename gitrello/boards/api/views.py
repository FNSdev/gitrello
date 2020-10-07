from django.db.transaction import atomic
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.services import PermissionsService
from boards.api.serializers import CreateBoardSerializer, CreateBoardMembershipSerializer, GetBoardPermissionsSerializer
from boards.services import BoardService, BoardMembershipService
from gitrello.exceptions import PermissionDeniedException
from gitrello.handlers import retry_on_transaction_serialization_error


class BoardsView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
    def post(self, request, *args, **kwargs):
        serializer = CreateBoardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        permissions = PermissionsService.get_organization_permissions(
            organization_id=serializer.validated_data['organization_id'],
            user_id=request.user.id,
        )
        if not permissions.can_mutate:
            raise PermissionDeniedException

        service = BoardService()
        board = service.create_board(**serializer.validated_data)
        return Response(
            status=201,
            data={
                'id': str(board.id),
                'name': board.name,
            },
        )


class BoardMembershipsView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
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
        return Response(
            status=201,
            data={
                'id': str(board_membership.id),
            },
        )


class BoardMembershipView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
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
    def get(self, request, *args, **kwargs):
        serializer = GetBoardPermissionsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        permissions = PermissionsService.get_board_permissions(**serializer.validated_data)
        return Response(status=200, data=permissions.to_json())
