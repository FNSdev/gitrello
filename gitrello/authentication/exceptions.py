from gitrello.exceptions import GITrelloException


class UserAlreadyExistsException(GITrelloException):
    message = 'User with given username and/or email already exists'
