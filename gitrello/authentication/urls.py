from django.urls import path

from authentication.api.views import AuthTokenView, UsersView, UserView

app_name = 'authentication'

urlpatterns = [
    path('v1/auth-token', AuthTokenView.as_view(), name='auth-token'),
    path('v1/users', UsersView.as_view(), name='users'),
    path('v1/users/<int:id>', UserView.as_view(), name='user'),
]
