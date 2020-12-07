from django.db.models import Subquery

from authentication.exceptions import UserNotFoundException
from authentication.models import User
from organizations.exceptions import (
    OrganizationNotFoundException, OrganizationInviteAlreadyExistsException, OrganizationInviteNotFoundException,
    OrganizationMembershipAlreadyExistsException,
)
from organizations.models import Organization, OrganizationInvite, OrganizationMembership
from organizations.services.organization_membership_service import OrganizationMembershipService


class OrganizationInviteService:
    @classmethod
    def create_organization_invite(cls, organization_id: int, email: str, message: str) -> OrganizationInvite:
        if not Organization.objects.filter(id=organization_id).exists():
            raise OrganizationNotFoundException

        if not User.objects.filter(email=email).exists():
            raise UserNotFoundException

        if OrganizationInvite.objects.filter(organization_id=organization_id, user__email=email).exists():
            raise OrganizationInviteAlreadyExistsException

        if OrganizationMembership.objects.filter(user__email=email, organization_id=organization_id).exists():
            raise OrganizationMembershipAlreadyExistsException

        return OrganizationInvite.objects.create(
            organization_id=Subquery(Organization.objects.filter(id=organization_id).values('id')),
            user_id=Subquery(User.objects.filter(email=email).values('id')),
            message=message,
        )

    @classmethod
    def accept_or_decline_invite(cls, organization_invite_id: int, accept: bool):
        invite = OrganizationInvite.objects.filter(id=organization_invite_id).first()
        if not invite:
            raise OrganizationInviteNotFoundException

        if accept:
            OrganizationMembershipService.create_organization_membership(
                organization_id=invite.organization_id,
                user_id=invite.user_id,
            )

        invite.delete()
