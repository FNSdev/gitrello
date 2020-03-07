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


class OrganizationMembershipNotFoundException(GITrelloOrganizationsException):
    message = 'User is not a member of a given organization'
    code = 321


class OrganizationMembershipAlreadyExistsException(GITrelloOrganizationsException):
    message = "User is already in organization"
    code = 322


class CanNotLeaveOrganizationException(GITrelloOrganizationsException):
    message = "Owner can not leave organization"
    code = 323
