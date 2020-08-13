from django.db.transaction import atomic

from gitrello.handlers import retry_on_transaction_serialization_error
from organizations.choices import OrganizationMemberRole
from organizations.exceptions import OrganizationAlreadyExistsException
from organizations.models import Organization
from organizations.services.organization_membership_service import OrganizationMembershipService


class OrganizationService:
    @retry_on_transaction_serialization_error
    @atomic
    def create_organization(self, name: str, owner_id: int) -> Organization:
        if Organization.objects.filter(name=name).exists():
            raise OrganizationAlreadyExistsException

        organization = Organization.objects.create(name=name)
        OrganizationMembershipService().add_member(
            organization_id=organization.id,
            user_id=owner_id,
            role=OrganizationMemberRole.OWNER,
        )
        return organization
