from django.urls import path

from organizations.api.views import CreateOrganizationView, OrganizationInviteView

app_name = 'organizations'

urlpatterns = [
    path('v1/organizations', CreateOrganizationView.as_view(), name='create_organization'),
    path('v1/organization-invites', OrganizationInviteView.as_view(), name='create_organization_invite'),
    path('v1/organization-invites/<int:id>', OrganizationInviteView.as_view(), name='update_organization_invite'),
]
