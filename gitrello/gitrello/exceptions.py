class GITrelloException(Exception):
    """Base class for all GITrello project exceptions"""

    message = 'Unknown exception'
    code = 0


class APIRequestValidationException(GITrelloException):
    message = 'Request validation failed'
    code = 100

    def __init__(self, serializer_errors):
        self.serializer_errors = serializer_errors
