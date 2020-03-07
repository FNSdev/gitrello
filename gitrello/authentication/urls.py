from django.urls import path

from authentication.api.views import UserView

app_name = 'authentication'

urlpatterns = [
    path('v1/users', UserView.as_view(), name='user'),
]
