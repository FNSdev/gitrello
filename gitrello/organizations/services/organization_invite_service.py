import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q

from authentication.exceptions import UserNotFoundException
from authentication.models import User
from gitrello.exceptions import PermissionDeniedException
from organizations.choices import OrganizationMemberRole
from organizations.exceptions import (
    GITrelloOrganizationsException, OrganizationNotFoundException, OrganizationInviteAlreadyExistsException,
)
from organizations.models import OrganizationInvite, OrganizationMembership

logger = logging.getLogger(__name__)


class OrganizationInviteService:
    _organization_not_found_pattern = r'Key (organization_id)='
    _user_not_found_pattern = r'User matching query'
    _already_invited_pattern = r'already exists'

    # TODO is it possible to avoid extra query?
    def send_invite(self, user_id: int, organization_id: int, email: str, message: str) -> OrganizationInvite:
        if not self._can_send_invite(user_id, organization_id):
            raise PermissionDeniedException

        try:
            invite = OrganizationInvite.objects.create(
                organization_id=organization_id,
                user=User.objects.get(email=email),
                message=message,
            )
            return invite
        except (IntegrityError, ObjectDoesNotExist) as e:
            logger.warning('Could not send invite in organization %s to user %s', organization_id, email)
            self._process_send_invite_exception(e)

    def _can_send_invite(self, user_id: int, organization_id: int):
        return OrganizationMembership.objects.filter(
            Q(organization_id=organization_id),
            Q(user_id=user_id),
            Q(role=OrganizationMemberRole.OWNER) | Q(role=OrganizationMemberRole.ADMIN)
        )

    def _process_send_invite_exception(self, e: IntegrityError):
        if e.args[0].find(self._organization_not_found_pattern) != -1:
            raise OrganizationNotFoundException

        if e.args[0].find(self._user_not_found_pattern) != -1:
            raise UserNotFoundException

        if e.args[0].find(self._already_invited_pattern) != -1:
            raise OrganizationInviteAlreadyExistsException

        raise GITrelloOrganizationsException
