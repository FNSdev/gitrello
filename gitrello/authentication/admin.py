from django.contrib import admin

from authentication.models import OauthState, User


admin.site.register(OauthState)
admin.site.register(User)
