from gitrello.exceptions import GITrelloException


class GITrelloTicketsException(GITrelloException):
    pass


class CategoryNotFoundException(GITrelloTicketsException):
    message = 'Category was not found'
    code = 501


class TicketNotFoundException(GITrelloTicketsException):
    message = 'Ticket was not found'
    code = 511
