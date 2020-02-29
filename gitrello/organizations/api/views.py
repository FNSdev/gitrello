from rest_framework import views
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from gitrello.exceptions import APIRequestValidationException
from gitrello.status_codes import StatusCode
from organizations.api.serializers import CreateOrganizationSerializer
from organizations.services import OrganizationService


class CreateOrganizationView(views.APIView):
    ORGANIZATION_ALREADY_EXISTS = 'Organization with given name already exists'

    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def post(self, request, *args, **kwargs):
        serializer = CreateOrganizationSerializer(data=request.data)
        if not serializer.is_valid():
            raise APIRequestValidationException(serializer_errors=serializer.errors)

        organization = OrganizationService().create_organization(owner=request.user, **serializer.validated_data)
        if not organization:
            return Response(
                status=400,
                data={
                    'error_code': StatusCode.ALREADY_EXISTS.value,
                    'error_message': self.ORGANIZATION_ALREADY_EXISTS,
                }
            )

        return Response(
            status=201,
            data={
                'id': organization.id,
                'name': organization.name,
            }
        )
