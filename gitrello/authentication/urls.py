from django.urls import path

from authentication.api.views import UsersView

app_name = 'authentication'

urlpatterns = [
    path('v1/users', UsersView.as_view(), name='users'),
]
