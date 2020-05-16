from django.db.transaction import atomic

from gitrello.handlers import retry_on_transaction_serialization_error
from organizations.choices import OrganizationMemberRole
from organizations.exceptions import OrganizationAlreadyExistsException
from organizations.models import Organization, OrganizationMembership
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
            role=OrganizationMemberRole.OWNER
        )
        return organization

    def can_get_organization(self, user_id: int, organization_id: int) -> bool:
        return OrganizationMembership.objects.filter(
            organization_id=organization_id,
            user_id=user_id,
        ).exists()

    def get_organization(self, organization_id: int) -> Organization:
        return Organization.objects \
            .filter(id=organization_id) \
            .prefetch_related(
                'organization_memberships',
                'organization_memberships__user',
                'boards',
                'boards__board_memberships',
                'boards__board_memberships__organization_membership',
                'boards__board_memberships__organization_membership__user',
            ) \
            .first()
