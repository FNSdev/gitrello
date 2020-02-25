from rest_framework.response import Response
from rest_framework.views import exception_handler

from gitrello.exceptions import APIRequestValidationException
from gitrello.status_codes import StatusCode


def custom_exception_handler(exc, context):
    if isinstance(exc, APIRequestValidationException):
        return Response(
            status=400,
            data={
                'error_code': StatusCode.BAD_REQUEST.value,
                'error_message': 'Request validation failed',
                'error_details': {field: errors for field, errors in exc.serializer_errors.items()},
            }
        )

    response = exception_handler(exc, context)
    return response
