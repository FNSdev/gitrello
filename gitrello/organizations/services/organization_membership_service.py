import logging

from django.db import IntegrityError

from organizations.choices import OrganizationMemberRole
from organizations.exceptions import (
    OrganizationMembershipAlreadyExistsException, OrganizationMembershipNotFoundException,
    CanNotLeaveOrganizationException,
)
from organizations.models import OrganizationMembership

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
    def delete_member(self, organization_membership_id):
        membership = OrganizationMembership.objects.filter(id=organization_membership_id).first()
        if not membership:
            raise OrganizationMembershipNotFoundException

        membership.delete()

    def can_delete_member(self, user_id: int, organization_membership_id: int):
        membership_to_delete = OrganizationMembership.objects.filter(id=organization_membership_id).first()
        if not membership_to_delete:
            return False

        if membership_to_delete.role == OrganizationMemberRole.OWNER:
            raise CanNotLeaveOrganizationException

        # User wants to leave organization
        if membership_to_delete.user_id == user_id:
            return True

        membership = OrganizationMembership.objects.filter(
            organization_id=membership_to_delete.organization_id,
            user_id=user_id,
        ).values('role').first()

        if not membership:
            return False

        # ADMIN users can be deleted from organization only by it's owner
        if membership_to_delete.role == OrganizationMemberRole.ADMIN:
            return membership['role'] == OrganizationMemberRole.OWNER

        # MEMBER users can be deleted from organization by owner and admins
        return membership['role'] == OrganizationMemberRole.OWNER or membership['role'] == OrganizationMemberRole.ADMIN
