from organizations.choices import OrganizationMemberRole
from organizations.exceptions import (
    OrganizationMembershipAlreadyExistsException, OrganizationMembershipNotFoundException,
    CanNotLeaveOrganizationException,
)
from organizations.models import OrganizationMembership


class OrganizationMembershipService:
    @classmethod
    def create_organization_membership(
        cls,
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

    @classmethod
    def delete_organization_membership(cls, organization_membership_id):
        organization_membership = OrganizationMembership.objects \
            .filter(id=organization_membership_id) \
            .values('role') \
            .first()

        if not organization_membership:
            raise OrganizationMembershipNotFoundException

        if organization_membership['role'] == OrganizationMemberRole.OWNER:
            raise CanNotLeaveOrganizationException

        OrganizationMembership.objects.filter(id=organization_membership_id).delete()
