from django.db.transaction import atomic
from rest_framework import views, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.services import PermissionsService
from gitrello.exceptions import PermissionDeniedException
from gitrello.handlers import retry_on_transaction_serialization_error
from gitrello.schema import gitrello_schema
from tickets.api.serializers import (
    CreateCategorySerializer, CreateTicketSerializer, CreateTicketAssignmentSerializer, CreateCommentSerializer,
    UpdateTicketSerializer, CreateCategoryResponseSerializer, CreateTicketAssignmentResponseSerializer,
    CreateCommentResponseSerializer, CreateTicketResponseSerializer, UpdateTicketResponseSerializer,
    MoveTicketActionResponseSerializer, MoveTicketActionSerializer, MoveCategoryActionSerializer,
    MoveCategoryActionResponseSerializer,
)
from tickets.services import CategoryService, CommentService, TicketAssignmentService, TicketService


class CategoriesView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
    @gitrello_schema(request_body=CreateCategorySerializer, responses={201: CreateCategoryResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = CreateCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        permissions = PermissionsService.get_board_permissions(
            board_id=serializer.validated_data['board_id'],
            user_id=request.user.id,
        )
        if not permissions.can_read:
            raise PermissionDeniedException

        category = CategoryService.create_category(**serializer.validated_data)
        response_serializer = CreateCategoryResponseSerializer(instance=category)
        return Response(
            status=201,
            data=response_serializer.data,
        )


class CategoryActionsViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, )

    # TODO add tests
    @retry_on_transaction_serialization_error
    @atomic
    @gitrello_schema(
        request_body=MoveCategoryActionSerializer,
        responses={200: MoveCategoryActionResponseSerializer},
    )
    def move(self, request, *args, **kwargs):
        serializer = MoveCategoryActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        permissions = PermissionsService.get_category_permissions(category_id=kwargs['id'], user_id=request.user.id)
        if not permissions.can_mutate:
            raise PermissionDeniedException

        category = CategoryService.move_category(
            category_id=kwargs['id'],
            insert_after_category_id=serializer.validated_data['insert_after_category_id'],
        )
        response_serializer = MoveCategoryActionResponseSerializer(instance=category)
        return Response(status=200, data=response_serializer.data)


class TicketsView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
    @gitrello_schema(request_body=CreateTicketSerializer, responses={201: CreateTicketResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = CreateTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        permissions = PermissionsService.get_category_permissions(
            category_id=serializer.validated_data['category_id'],
            user_id=request.user.id,
        )
        if not permissions.can_mutate:
            raise PermissionDeniedException

        ticket = TicketService.create_ticket(**serializer.validated_data)
        response_serializer = CreateTicketResponseSerializer(instance=ticket)
        return Response(
            status=201,
            data=response_serializer.data,
        )


class TicketView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
    @gitrello_schema(request_body=UpdateTicketSerializer, responses={200: UpdateTicketResponseSerializer})
    def patch(self, request, *args, **kwargs):
        serializer = UpdateTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        permissions = PermissionsService.get_ticket_permissions(ticket_id=kwargs['id'], user_id=request.user.id)
        if not permissions.can_mutate:
            raise PermissionDeniedException

        ticket = TicketService.update_ticket(ticket_id=kwargs['id'], validated_data=serializer.validated_data)
        response_serializer = UpdateTicketResponseSerializer(instance=ticket)
        return Response(
            status=200,
            data=response_serializer.data,
        )

    # TODO add tests
    @retry_on_transaction_serialization_error
    @atomic
    @gitrello_schema(responses={204: ''})
    def delete(self, request, *args, **kwargs):
        permissions = PermissionsService.get_ticket_permissions(ticket_id=kwargs['id'], user_id=request.user.id)
        if not permissions.can_delete:
            raise PermissionDeniedException

        TicketService.delete_ticket(ticket_id=kwargs['id'])
        return Response(status=204)


class TicketActionsViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, )

    # TODO add tests
    @retry_on_transaction_serialization_error
    @atomic
    @gitrello_schema(request_body=MoveTicketActionSerializer, responses={200: MoveTicketActionResponseSerializer})
    def move(self, request, *args, **kwargs):
        serializer = MoveTicketActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        permissions = PermissionsService.get_ticket_permissions(ticket_id=kwargs['id'], user_id=request.user.id)
        if not permissions.can_mutate:
            raise PermissionDeniedException

        ticket = TicketService.move_ticket(
            ticket_id=kwargs['id'],
            insert_after_ticket_id=serializer.validated_data['insert_after_ticket_id'],
            new_category_id=serializer.validated_data['category_id'],
        )
        response_serializer = MoveTicketActionResponseSerializer(instance=ticket)
        return Response(status=200, data=response_serializer.data)


class TicketAssignmentsView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
    @gitrello_schema(
        request_body=CreateTicketAssignmentSerializer,
        responses={201: CreateTicketAssignmentResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = CreateTicketAssignmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        permissions = PermissionsService.get_ticket_permissions(
            ticket_id=serializer.validated_data['ticket_id'],
            user_id=request.user.id,
        )
        if not permissions.can_mutate:
            raise PermissionDeniedException

        ticket_assignment = TicketAssignmentService.create_ticket_assignment(**serializer.validated_data)
        response_serializer = CreateTicketAssignmentResponseSerializer(instance=ticket_assignment)
        return Response(
            status=201,
            data=response_serializer.data,
        )


class TicketAssignmentView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
    @gitrello_schema(responses={204: ''})
    def delete(self, request, *args, **kwargs):
        service = TicketAssignmentService()

        permissions = PermissionsService.get_ticket_assignment_permissions(
            ticket_assignment_id=kwargs['id'],
            user_id=request.user.id,
        )
        if not permissions.can_delete:
            raise PermissionDeniedException

        service.delete_ticket_assignment(ticket_assignment_id=kwargs['id'])
        return Response(status=204)


class CommentsView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
    @gitrello_schema(request_body=CreateCommentSerializer, responses={201: CreateCommentResponseSerializer})
    def post(self, request, *args, **kwargs):
        serializer = CreateCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        permissions = PermissionsService.get_ticket_permissions(
            ticket_id=serializer.validated_data['ticket_id'],
            user_id=request.user.id,
        )
        if not permissions.can_mutate:
            raise PermissionDeniedException

        comment = CommentService.create_comment(user_id=request.user.id, **serializer.validated_data)
        response_serializer = CreateCommentResponseSerializer(instance=comment)
        return Response(
            status=201,
            data=response_serializer.data,
        )
