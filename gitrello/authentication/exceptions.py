from gitrello.exceptions import GITrelloException


class GITRelloAuthenticationException(GITrelloException):
    code = 200


class UserNotFoundException(GITRelloAuthenticationException):
    message = 'User was not found'
    code = 201


class UserAlreadyExistsException(GITRelloAuthenticationException):
    message = 'User with given username and/or email already exists'
    code = 202


class OauthStateNotFoundException(GITRelloAuthenticationException):
    message = 'OauthState was not found'
    code = 211


class GithubException(GITrelloException):
    message = 'Something went wrong when using Github API'
    code = 220

    def __init__(self, error, error_description):
        self.error = error
        self.error_description = error_description
