import logging
import time
from functools import wraps
from typing import Callable

from django.db import IntegrityError
from psycopg2 import errorcodes
from requests import RequestException
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler

from gitrello.exceptions import (
    GITrelloException, APIRequestValidationException, PermissionDeniedException, AuthenticationFailedException,
    HttpRequestException,
)

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    logger.exception(exc)

    if isinstance(exc, AuthenticationFailed):
        return Response(
            status=401,
            data={
                'error_code': AuthenticationFailedException.code,
                'error_message': AuthenticationFailedException.message,
                'error_details': {'error': str(exc)}
            }
        )

    if isinstance(exc, ValidationError):
        return Response(
            status=400,
            data={
                'error_code': APIRequestValidationException.code,
                'error_message': APIRequestValidationException.message,
                'error_details': {field: errors for field, errors in exc.detail.items()},
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


def retry_on_transaction_serialization_error(
    original_function: Callable = None,
    *,
    num_retries: int = 3,
    on_failure: GITrelloException = GITrelloException,
    delay: float = 0.02,
    backoff: float = 2,
) -> Callable:
    """
    Should be used along with atomic() decorator to retry when transaction with serializable isolation level fails.
    Should not be used in an inner nested transaction
    """

    def retry(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay_ = delay
            for i in range(num_retries):
                try:
                    return func(*args, **kwargs)
                except IntegrityError as e:
                    if i == num_retries - 1:
                        logger.exception('Attempted to retry %s %s times, but failed', func.__name__, num_retries)
                        raise on_failure

                    if getattr(e.__cause__, 'pgcode', '') == errorcodes.SERIALIZATION_FAILURE:
                        logger.warning('Transaction failed for %s. Retrying', func.__name__)
                        time.sleep(delay_)
                        delay_ *= backoff
                    else:
                        raise e

        return wrapper

    if original_function:
        return retry(original_function)

    return retry


def safe_http_request(original_function: Callable = None):
    @wraps(original_function)
    def wrapper(*args, **kwargs):
        try:
            return original_function(*args, **kwargs)
        except RequestException as e:
            logger.exception('HTTP Request exception in %s', original_function.__name__)
            raise HttpRequestException from e

    return wrapper
