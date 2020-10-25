from django.urls import path

from github_integration.api.views import TicketsView
from github_integration.views import GithubOauthView

app_name = 'github_integration'

oauth_urlpatterns = [
    path('v1/github', GithubOauthView.as_view(), name='github-oauth'),
]

api_urlpatterns = [
    path('api/v1/tickets', TicketsView.as_view(), name='tickets'),
]

urlpatterns = oauth_urlpatterns + api_urlpatterns
