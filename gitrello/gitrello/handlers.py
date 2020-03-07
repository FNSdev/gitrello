from rest_framework.response import Response
from rest_framework.views import exception_handler

from gitrello.exceptions import GITrelloException, APIRequestValidationException, PermissionDeniedException


def custom_exception_handler(exc, context):
    if isinstance(exc, APIRequestValidationException):
        return Response(
            status=400,
            data={
                'error_code': exc.code,
                'error_message': exc.message,
                'error_details': {field: errors for field, errors in exc.serializer_errors.items()},
            }
        )

    if isinstance(exc, PermissionDeniedException):
        return Response(
            status=403,
            data={
                'error_code': exc.code,
                'error_message': exc.message,
            }
        )

    if isinstance(exc, GITrelloException):
        return Response(
            status=400,
            data={
                'error_code': exc.code,
                'error_message': exc.message,
            }
        )

    response = exception_handler(exc, context)
    return response
