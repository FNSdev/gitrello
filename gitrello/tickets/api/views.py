from rest_framework import views
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from gitrello.exceptions import APIRequestValidationException, PermissionDeniedException
from tickets.api.serializers import (
    CreateCategorySerializer, CreateTicketSerializer, UpdateTicketSerializer, CreateTicketAssignmentSerializer,
)
from tickets.services import CategoryService, TicketAssignmentService, TicketService


class CategoriesView(views.APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def post(self, request, *args, **kwargs):
        serializer = CreateCategorySerializer(data=request.data)
        if not serializer.is_valid():
            raise APIRequestValidationException(serializer_errors=serializer.errors)

        service = CategoryService()
        if not service.can_create_category(user_id=request.user.id, board_id=serializer.validated_data['board_id']):
            raise PermissionDeniedException

        category = service.create_category(**serializer.validated_data)
        return Response(
            status=201,
            data={
                'id': str(category.id),
                'board_id': str(category.board_id),
                'name': category.name,
            }
        )


class TicketsView(views.APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def post(self, request, *args, **kwargs):
        serializer = CreateTicketSerializer(data=request.data)
        if not serializer.is_valid():
            raise APIRequestValidationException(serializer_errors=serializer.errors)

        service = TicketService()
        if not service.can_create_ticket(user_id=request.user.id, category_id=serializer.validated_data['category_id']):
            raise PermissionDeniedException

        ticket = service.create_ticket(**serializer.validated_data)
        return Response(
            status=201,
            data={
                'id': str(ticket.id),
                'category_id': str(ticket.category_id),
            }
        )


class TicketView(views.APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def patch(self, request, *args, **kwargs):
        serializer = UpdateTicketSerializer(data=request.data)
        if not serializer.is_valid():
            raise APIRequestValidationException(serializer_errors=serializer.errors)

        service = TicketService()
        if not service.can_update_ticket(user_id=request.user.id, ticket_id=kwargs['id']):
            raise PermissionDeniedException

        ticket = service.update_ticket(ticket_id=kwargs['id'], validated_data=serializer.validated_data)
        return Response(
            status=200,
            data={
                'id': str(ticket.id),
                'title': ticket.title,
                'body': ticket.body,
                'due_date': ticket.due_date,
            }
        )


class TicketAssignmentsView(views.APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def post(self, request, *args, **kwargs):
        serializer = CreateTicketAssignmentSerializer(data=request.data)
        if not serializer.is_valid():
            raise APIRequestValidationException(serializer_errors=serializer.errors)

        service = TicketAssignmentService()
        if not service.can_assign_member(
            user_id=request.user.id,
            ticket_id=serializer.validated_data['ticket_id'],
            board_membership_id=serializer.validated_data['board_membership_id'],
        ):
            raise PermissionDeniedException

        ticket_assignment = service.assign_member(**serializer.validated_data)
        return Response(
            status=201,
            data={
                'id': str(ticket_assignment.id),
                'ticket_id': str(ticket_assignment.ticket_id),
                'assignee_id': str(ticket_assignment.assignee_id),
            }
        )


class TicketAssignmentView(views.APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def delete(self, request, *args, **kwargs):
        service = TicketAssignmentService()
        if not service.can_unassign_member(user_id=request.user.id, ticket_assignment_id=kwargs['id']):
            raise PermissionDeniedException

        service.unassign_member(ticket_assignment_id=kwargs['id'])
        return Response(status=204)
