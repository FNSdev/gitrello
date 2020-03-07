import logging

from django.db import IntegrityError

from organizations.choices import OrganizationMemberRole
from organizations.exceptions import OrganizationMembershipAlreadyExists
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
            raise OrganizationMembershipAlreadyExists
