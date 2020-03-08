import logging

from django.db import IntegrityError
from django.db.transaction import atomic

from organizations.choices import OrganizationMemberRole
from organizations.exceptions import OrganizationAlreadyExistsException
from organizations.models import Organization
from organizations.services.organization_membership_service import OrganizationMembershipService

logger = logging.getLogger(__name__)


class OrganizationService:
    @atomic
    def create_organization(self, name: str, owner_id: int) -> Organization:
        try:
            organization = Organization.objects.create(name=name)
        except IntegrityError:
            logger.exception('Attempted to create Organization %s, but this name is already taken', name)
            raise OrganizationAlreadyExistsException

        OrganizationMembershipService().add_member(
            organization_id=organization.id,
            user_id=owner_id,
            role=OrganizationMemberRole.OWNER
        )
        return organization
