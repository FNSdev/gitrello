import logging
from typing import Optional

from django.db import IntegrityError

from authentication.models import User
from organizations.choices import OrganizationMemberRole
from organizations.models import Organization, OrganizationMembership

logger = logging.getLogger(__name__)


class OrganizationService:
    def create_organization(self, name: str, owner: User) -> Optional[Organization]:
        try:
            organization = Organization.objects.create(name=name)
        except IntegrityError:
            logger.exception('Attempted to create Organization %s, but this name is already taken', name)
            return None

        OrganizationMembership.objects.create(
            organization=organization,
            user=owner,
            role=OrganizationMemberRole.OWNER,
        )

        return organization
