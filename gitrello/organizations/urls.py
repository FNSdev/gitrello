from django.urls import path

from organizations.api.views import OrganizationView, OrganizationInviteView, OrganizationMembershipView

app_name = 'organizations'

urlpatterns = [
    path('v1/organizations', OrganizationView.as_view(), name='organization'),
    path('v1/organization-invites', OrganizationInviteView.as_view(), name='organization_invite'),
    path('v1/organization-invites/<int:id>', OrganizationInviteView.as_view(), name='organization_invite'),
    path('v1/organization-memberships', OrganizationMembershipView.as_view(), name='organization-membership'),
    path('v1/organization-memberships/<int:id>', OrganizationMembershipView.as_view(), name='organization-membership'),
]
