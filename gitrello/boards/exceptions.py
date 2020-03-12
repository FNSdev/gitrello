from gitrello.exceptions import GITrelloException


class GITrelloBoardsException(GITrelloException):
    pass


class BoardNotFoundException(GITrelloBoardsException):
    message = 'Board was not found'
    code = 401


class BoardMembershipNotFoundException(GITrelloBoardsException):
    message = 'Board membership was not found'
    code = 411


class BoardMembershipAlreadyExistsException(GITrelloBoardsException):
    message = 'User is already added to this board'
    code = 412


class CanNotLeaveBoardException(GITrelloBoardsException):
    message = "Owner can not leave board"
    code = 423
