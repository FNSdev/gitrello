from django.db.transaction import atomic
from rest_framework import views
from rest_framework.response import Response

from github_integration.api.permissions import GithubIntegrationServicePermission
from github_integration.api.serializers import CreateTicketSerializer
from gitrello.handlers import retry_on_transaction_serialization_error
from tickets.services import TicketService


# TODO schema & tests
class TicketsView(views.APIView):
    permission_classes = (GithubIntegrationServicePermission, )

    @retry_on_transaction_serialization_error
    @atomic
    def post(self, request, *args, **kwargs):
        serializer = CreateTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        TicketService.create_ticket_from_github_issue(**serializer.validated_data)

        return Response(status=201)
