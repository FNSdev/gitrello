from django.urls import path

from authentication.api.views import AuthTokenOwnerView, LoginView, OauthStatesView, UsersView

app_name = 'authentication'

urlpatterns = [
    path('v1/auth-token', LoginView.as_view(), name='auth-token'),
    path('v1/auth-token/owner', AuthTokenOwnerView.as_view(), name='auth-token-owner'),
    path('v1/oauth-states', OauthStatesView.as_view(), name='oauth-states'),
    path('v1/users', UsersView.as_view(), name='users'),
]
