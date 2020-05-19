from django.db.models import Q, Subquery
from django.db.transaction import atomic

from authentication.exceptions import UserNotFoundException
from authentication.models import User
from gitrello.handlers import retry_on_transaction_serialization_error
from organizations.choices import OrganizationMemberRole, OrganizationInviteStatus
from organizations.exceptions import (
    OrganizationNotFoundException, OrganizationInviteAlreadyExistsException, OrganizationInviteNotFoundException,
    OrganizationMembershipAlreadyExistsException,
)
from organizations.models import Organization, OrganizationInvite, OrganizationMembership
from organizations.services.organization_membership_service import OrganizationMembershipService


class OrganizationInviteService:
    @retry_on_transaction_serialization_error
    @atomic
    def send_invite(self, organization_id: int, email: str, message: str) -> OrganizationInvite:
        if not Organization.objects.filter(id=organization_id).exists():
            raise OrganizationNotFoundException

        if not User.objects.filter(email=email).exists():
            raise UserNotFoundException

        if OrganizationInvite.objects.filter(organization_id=organization_id, user__email=email).exists():
            raise OrganizationInviteAlreadyExistsException

        # TODO add test
        if OrganizationMembership.objects.filter(user__email=email, organization_id=organization_id).exists():
            raise OrganizationMembershipAlreadyExistsException

        return OrganizationInvite.objects.create(
            organization_id=Subquery(Organization.objects.filter(id=organization_id).values('id')),
            user_id=Subquery(User.objects.filter(email=email).values('id')),
            message=message,
        )

    @retry_on_transaction_serialization_error
    @atomic
    def update_invite(self, organization_invite_id: int, accept: bool) -> OrganizationInvite:
        invite = OrganizationInvite.objects.filter(id=organization_invite_id).first()
        if not invite:
            raise OrganizationInviteNotFoundException

        invite.status = OrganizationInviteStatus.ACCEPTED if accept else OrganizationInviteStatus.DECLINED
        invite.save()

        if accept:
            OrganizationMembershipService().add_member(
                organization_id=invite.organization_id,
                user_id=invite.user_id,
            )

        return invite

    @retry_on_transaction_serialization_error
    def can_send_invite(self, user_id: int, organization_id: int):
        return OrganizationMembership.objects.filter(
            Q(organization_id=organization_id),
            Q(user_id=user_id),
            Q(role=OrganizationMemberRole.OWNER) | Q(role=OrganizationMemberRole.ADMIN),
        ).exists()

    @retry_on_transaction_serialization_error
    def can_update_invite(self, user_id: int, organization_invite_id: int):
        return OrganizationInvite.objects.filter(
            id=organization_invite_id,
            user_id=user_id,
        ).exists()

    def get_pending_invites(self, user_id):
        return OrganizationInvite.objects \
            .filter(user_id=user_id, status=OrganizationInviteStatus.PENDING) \
            .select_related('organization')
