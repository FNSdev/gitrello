from rest_framework import views
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from gitrello.exceptions import APIRequestValidationException, PermissionDeniedException
from tickets.api.serializers import (
    CreateCategorySerializer, CreateTicketSerializer, UpdateTicketSerializer, CreateTicketAssignmentSerializer,
)
from tickets.services import CategoryService, TicketService


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
                'id': category.id,
                'board_id': category.board_id,
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
                'id': ticket.id,
                'category_id': ticket.category_id,
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
                'id': ticket.id,
                'title': ticket.title,
                'body': ticket.body,
                'due_date': ticket.due_date,
            }
        )


class TicketAssignmentsView(views.APIView):
    pass


class TicketAssignmentView(views.APIView):
    pass
