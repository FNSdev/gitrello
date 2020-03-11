import logging
from typing import Union

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q, Subquery
from django.db.transaction import atomic

from authentication.exceptions import UserNotFoundException
from authentication.models import User
from organizations.choices import OrganizationMemberRole, OrganizationInviteStatus
from organizations.exceptions import (
    GITrelloOrganizationsException, OrganizationNotFoundException, OrganizationInviteAlreadyExistsException,
)
from organizations.models import Organization, OrganizationInvite, OrganizationMembership
from organizations.services.organization_membership_service import OrganizationMembershipService

logger = logging.getLogger(__name__)


class OrganizationInviteService:
    _organization_not_found_pattern = r'null value in column "organization_id"'
    _user_not_found_pattern = r'null value in column "user_id"'
    _already_invited_pattern = r'already exists'

    # Django checks foreign key constraint only when transaction is committed.
    # It will be impossible to test it using TestCase, if I'll write it like `organization_id=organization_id`
    def send_invite(self, organization_id: int, email: str, message: str) -> OrganizationInvite:
        try:
            invite = OrganizationInvite.objects.create(
                organization_id=Subquery(Organization.objects.filter(id=organization_id).values('id')),
                user_id=Subquery(User.objects.filter(email=email).values('id')),
                message=message,
            )
            return invite
        except (IntegrityError, ObjectDoesNotExist) as e:
            logger.warning('Could not send invite in organization %s to user %s', organization_id, email)
            self._process_send_invite_exception(e)

    @atomic
    def update_invite(self, organization_invite_id: int, accept: bool) -> OrganizationInvite:
        invite = OrganizationInvite.objects.select_for_update().get(id=organization_invite_id)
        invite.status = OrganizationInviteStatus.ACCEPTED if accept else OrganizationInviteStatus.DECLINED
        invite.save()

        if accept:
            OrganizationMembershipService().add_member(
                organization_id=invite.organization_id,
                user_id=invite.user_id,
            )

        return invite

    def can_send_invite(self, user_id: int, organization_id: int):
        return OrganizationMembership.objects.filter(
            Q(organization_id=organization_id),
            Q(user_id=user_id),
            Q(role=OrganizationMemberRole.OWNER) | Q(role=OrganizationMemberRole.ADMIN),
        ).exists()

    def can_update_invite(self, user_id: int, organization_invite_id: int):
        return OrganizationInvite.objects.filter(
            id=organization_invite_id,
            user_id=user_id,
        ).exists()

    def _process_send_invite_exception(self, e: Union[IntegrityError, ObjectDoesNotExist]):
        if e.args[0].find(self._organization_not_found_pattern) != -1:
            raise OrganizationNotFoundException

        if e.args[0].find(self._user_not_found_pattern) != -1:
            raise UserNotFoundException

        if e.args[0].find(self._already_invited_pattern) != -1:
            raise OrganizationInviteAlreadyExistsException

        raise GITrelloOrganizationsException
