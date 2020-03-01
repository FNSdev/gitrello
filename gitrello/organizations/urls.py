from django.urls import path

from organizations.api.views import CreateOrganizationView, CreateOrganizationInviteView

app_name = 'organizations'

urlpatterns = [
    path('v1/organizations', CreateOrganizationView.as_view(), name='create_organization'),
    path('v1/organization-invites', CreateOrganizationInviteView.as_view(), name='create_organization_invite')
]
