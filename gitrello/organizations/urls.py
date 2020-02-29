from django.urls import path

from organizations.api.views import CreateOrganizationView

app_name = 'organizations'

urlpatterns = [
    path('v1/organizations', CreateOrganizationView.as_view(), name='create_organization'),
]
