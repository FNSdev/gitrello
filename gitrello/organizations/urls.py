from django.urls import path

from organizations.api.views import (
    CreateOrganizationView, CreateOrganizationInviteView, UpdateOrganizationInviteView,
    DeleteOrganizationMembershipView,
)

app_name = 'organizations'

urlpatterns = [
    path('v1/organizations', CreateOrganizationView.as_view(), name='create_organization'),
    path('v1/organization-invites', CreateOrganizationInviteView.as_view(), name='create_organization_invite'),
    path('v1/organization-invites/<int:id>', UpdateOrganizationInviteView.as_view(), name='update_organization_invite'),
    path(
        'v1/organization-memberships/<int:id>',
        DeleteOrganizationMembershipView.as_view(),
        name='delete_organization_membership'
    ),
]
