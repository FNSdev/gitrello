from django.db.transaction import atomic
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.services import PermissionsService
from gitrello.exceptions import PermissionDeniedException
from gitrello.handlers import retry_on_transaction_serialization_error
from tickets.api.serializers import (
    CreateCategorySerializer, CreateTicketSerializer, CreateTicketAssignmentSerializer, CreateCommentSerializer,
    UpdateTicketSerializer,
)
from tickets.services import CategoryService, CommentService, TicketAssignmentService, TicketService


class CategoriesView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
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
        return Response(
            status=201,
            data={
                'id': str(category.id),
                'board_id': str(category.board_id),
                'name': category.name,
            },
        )


class TicketsView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
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
        return Response(
            status=201,
            data={
                'id': str(ticket.id),
                'category_id': str(ticket.category_id),
                'priority': ticket.priority,
            },
        )


class TicketView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
    def patch(self, request, *args, **kwargs):
        serializer = UpdateTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        permissions = PermissionsService.get_ticket_permissions(ticket_id=kwargs['id'], user_id=request.user.id)
        if not permissions.can_mutate:
            raise PermissionDeniedException

        ticket = TicketService.update_ticket(ticket_id=kwargs['id'], validated_data=serializer.validated_data)
        return Response(
            status=200,
            data={
                'id': str(ticket.id),
                'title': ticket.title,
                'body': ticket.body,
                'due_date': ticket.due_date,
                'priority': ticket.priority,
                'category_id': str(ticket.category_id),
            },
        )

    # TODO add tests
    @retry_on_transaction_serialization_error
    @atomic
    def delete(self, request, *args, **kwargs):
        permissions = PermissionsService.get_ticket_permissions(ticket_id=kwargs['id'], user_id=request.user.id)
        if not permissions.can_delete:
            raise PermissionDeniedException

        TicketService.delete_ticket(ticket_id=kwargs['id'])
        return Response(status=204)


class TicketAssignmentsView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
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
        return Response(
            status=201,
            data={
                'id': str(ticket_assignment.id),
                'ticket_id': str(ticket_assignment.ticket_id),
                'assignee_id': str(ticket_assignment.assignee_id),
            },
        )


class TicketAssignmentView(views.APIView):
    permission_classes = (IsAuthenticated, )

    @retry_on_transaction_serialization_error
    @atomic
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
        return Response(
            status=201,
            data={
                'id': str(comment.id),
                'ticket_id': str(comment.ticket_id),
                'author_id': str(comment.author_id),
                'message': comment.message,
                'added_at': comment.added_at,
            },
        )
