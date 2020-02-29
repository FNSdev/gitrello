from django.contrib import admin

from organizations.models import Organization, OrganizationInvite, OrganizationMembership


admin.site.register(Organization)
admin.site.register(OrganizationInvite)
admin.site.register(OrganizationMembership)
