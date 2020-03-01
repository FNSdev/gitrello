from gitrello.exceptions import GITrelloException


class GITrelloOrganizationsException(GITrelloException):
    pass


class OrganizationNotFoundException(GITrelloOrganizationsException):
    message = 'Organization was not found'
    code = 301


class OrganizationAlreadyExistsException(GITrelloOrganizationsException):
    message = 'Organization with given name already exists'
    code = 302


class OrganizationInviteAlreadyExistsException(GITrelloOrganizationsException):
    message = 'Invite has been already sent'
    code = 312
