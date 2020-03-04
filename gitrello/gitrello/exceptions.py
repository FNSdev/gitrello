class GITrelloException(Exception):
    """Base class for all GITrello project exceptions"""

    message = 'Unknown exception'
    code = 0


class APIRequestValidationException(GITrelloException):
    message = 'Request validation failed'
    code = 1

    def __init__(self, serializer_errors):
        self.serializer_errors = serializer_errors


class PermissionDeniedException(GITrelloException):
    message = 'Permission denied'
    code = 2
