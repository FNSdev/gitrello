from django.conf import settings
from rest_framework import permissions


class GithubIntegrationServicePermission(permissions.BasePermission):
    message = 'Invalid access token'

    def has_permission(self, request, view):
        return request.META.get('GITHUB_INTEGRATION_SERVICE_TOKEN') == settings.GITHUB_INTEGRATION_SERVICE_TOKEN
