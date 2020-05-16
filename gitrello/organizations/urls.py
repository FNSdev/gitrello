from django.urls import path

from organizations.api.views import (
    OrganizationsView, OrganizationInvitesView, OrganizationInviteView,
    OrganizationMembershipView, OrganizationMembershipsView, OrganizationView,
)

app_name = 'organizations'

urlpatterns = [
    path('v1/organizations', OrganizationsView.as_view(), name='organizations'),
    path('v1/organizations/<int:id>', OrganizationView.as_view(), name='organization'),
    path('v1/organization-invites', OrganizationInvitesView.as_view(), name='organization_invites'),
    path('v1/organization-invites/<int:id>', OrganizationInviteView.as_view(), name='organization_invite'),
    path('v1/organization-memberships', OrganizationMembershipsView.as_view(), name='organization-memberships'),
    path(
        'v1/organization-memberships/<int:id>',
        OrganizationMembershipView.as_view(),
        name='organization_membership'
    ),
]
