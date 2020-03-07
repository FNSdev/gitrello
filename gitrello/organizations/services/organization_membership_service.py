import logging

from django.db import IntegrityError
from django.db.models import Q

from organizations.choices import OrganizationMemberRole
from organizations.exceptions import (
    OrganizationMembershipAlreadyExistsException, OrganizationMembershipNotFoundException,
    CanNotLeaveOrganizationException,
)
from organizations.models import OrganizationMembership
from gitrello.exceptions import PermissionDeniedException

logger = logging.getLogger(__name__)


class OrganizationMembershipService:
    def add_member(
        self,
        organization_id: int,
        user_id: int,
        role: str = OrganizationMemberRole.MEMBER
    ) -> OrganizationMembership:
        try:
            return OrganizationMembership.objects.create(
                organization_id=organization_id,
                user_id=user_id,
                role=role,
            )
        except IntegrityError:
            logger.warning('Could not add user %s to organization %s', user_id, organization_id)
            raise OrganizationMembershipAlreadyExistsException

    # TODO delete/update invite?
    def delete_member(self, auth_user_id: int, organization_membership_id):
        try:
            membership = OrganizationMembership.objects.get(id=organization_membership_id)
        except OrganizationMembership.DoesNotExist:
            raise OrganizationMembershipNotFoundException

        if not self._can_delete_member(auth_user_id, membership):
            raise PermissionDeniedException

        if membership.role == OrganizationMemberRole.OWNER:
            raise CanNotLeaveOrganizationException

        membership.delete()

    def _can_delete_member(self, auth_user_id: int, membership: OrganizationMembership):
        query = OrganizationMembership.objects.filter(
            Q(organization_id=membership.organization_id),
            Q(user_id=auth_user_id),
        )
        if membership.role == OrganizationMemberRole.OWNER:
            raise CanNotLeaveOrganizationException
        elif membership.role == OrganizationMemberRole.ADMIN:
            query = query.filter(role=OrganizationMemberRole.OWNER)
        elif membership.role == OrganizationMemberRole.MEMBER:
            query = query.filter(Q(role=OrganizationMemberRole.OWNER) | Q(role=OrganizationMemberRole.ADMIN))

        return query.exists() or auth_user_id == membership.user_id
