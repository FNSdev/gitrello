from gitrello.exceptions import GITrelloException


class GithubException(GITrelloException):
    message = 'Something went wrong when using Github API'
    code = 220

    def __init__(self, error, error_description):
        self.error = error
        self.error_description = error_description


class GithubAccountUsedByAnotherUserException(GITrelloException):
    message = 'This GitHub account is being used by another GITrello user'
    code = 230
