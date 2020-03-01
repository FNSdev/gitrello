from gitrello.exceptions import GITrelloException


class GITRelloAuthenticationException(GITrelloException):
    code = 200


class UserNotFoundException(GITRelloAuthenticationException):
    message = 'User was not found'
    code = 201


class UserAlreadyExistsException(GITRelloAuthenticationException):
    message = 'User with given username and/or email already exists'
    code = 202
