from typing import List

from django.db.transaction import atomic

from gitrello.handlers import retry_on_transaction_serialization_error
from organizations.choices import OrganizationMemberRole
from organizations.exceptions import (
    OrganizationMembershipAlreadyExistsException, OrganizationMembershipNotFoundException,
    CanNotLeaveOrganizationException,
)
from organizations.models import OrganizationMembership


class OrganizationMembershipService:
    def add_member(
        self,
        organization_id: int,
        user_id: int,
        role: str = OrganizationMemberRole.MEMBER
    ) -> OrganizationMembership:
        if OrganizationMembership.objects.filter(organization_id=organization_id, user_id=user_id).exists():
            raise OrganizationMembershipAlreadyExistsException

        return OrganizationMembership.objects.create(
            organization_id=organization_id,
            user_id=user_id,
            role=role,
        )

    # TODO delete/update invite?
    @retry_on_transaction_serialization_error
    def delete_member(self, organization_membership_id):
        membership = OrganizationMembership.objects.filter(id=organization_membership_id).first()
        if not membership:
            raise OrganizationMembershipNotFoundException

        membership.delete()

    @retry_on_transaction_serialization_error
    @atomic
    def can_delete_member(self, user_id: int, organization_membership_id: int) -> bool:
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

    def get_organization_memberships(self, user_id: int) -> List[OrganizationMembership]:
        return OrganizationMembership.objects \
            .filter(user_id=user_id) \
            .prefetch_related('organization', 'board_memberships', 'board_memberships__board')
