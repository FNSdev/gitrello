from django.urls import path

from authentication.api.views import CreateUserView

app_name = 'authentication'

urlpatterns = [
    path('v1/users', CreateUserView.as_view(), name='create_user'),
]
