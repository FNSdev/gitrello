from rest_framework import views
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from gitrello.exceptions import APIRequestValidationException, PermissionDeniedException
from tickets.api.serializers import CreateCategorySerializer
from tickets.services import CategoryService


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
