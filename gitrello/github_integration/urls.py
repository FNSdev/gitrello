from django.urls import path

from github_integration.views import GithubOauthView

app_name = 'github_integration'

oauth_urlpatterns = [
    path('oauth/v1/github', GithubOauthView.as_view(), name='github-oauth'),
]

api_urlpatterns = []

urlpatterns = oauth_urlpatterns + api_urlpatterns
