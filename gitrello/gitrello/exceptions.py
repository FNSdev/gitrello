class GITrelloException(Exception):
    """Base class for all GITrello project exceptions"""


class APIRequestValidationException(GITrelloException):
    def __init__(self, serializer_errors):
        self.serializer_errors = serializer_errors
