class GITrelloException(Exception):
    """Base class for all GITrello project exceptions"""

    message = None


class APIRequestValidationException(GITrelloException):
    message = 'Request validation failed'

    def __init__(self, serializer_errors):
        self.serializer_errors = serializer_errors
