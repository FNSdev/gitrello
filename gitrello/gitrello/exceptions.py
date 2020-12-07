class GITrelloException(Exception):
    """Base class for all GITrello project exceptions"""

    message = 'Unknown exception'
    code = 0


class APIRequestValidationException(GITrelloException):
    message = 'Request validation failed'
    code = 1


class PermissionDeniedException(GITrelloException):
    message = 'Permission denied'
    code = 2


class AuthenticationFailedException(GITrelloException):
    message = 'Authentication failed'
    code = 3


class HttpRequestException(GITrelloException):
    message = 'An error occurred when accessing an external service'
    code = 4
