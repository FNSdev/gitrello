from organizations.choices import OrganizationMemberRole
from organizations.exceptions import OrganizationAlreadyExistsException
from organizations.models import Organization
from organizations.services.organization_membership_service import OrganizationMembershipService


class OrganizationService:
    @classmethod
    def create_organization(cls, name: str, owner_id: int) -> Organization:
        if Organization.objects.filter(name=name).exists():
            raise OrganizationAlreadyExistsException

        organization = Organization.objects.create(name=name)
        OrganizationMembershipService.create_organization_membership(
            organization_id=organization.id,
            user_id=owner_id,
            role=OrganizationMemberRole.OWNER,
        )
        return organization
