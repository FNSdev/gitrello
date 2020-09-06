from django.conf import settings
from django.urls import reverse
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['GITHUB_CLIENT_ID'] = settings.GITHUB_CLIENT_ID
        context_data['GITHUB_DEFAULT_SCOPES'] = ','.join(settings.GITHUB_DEFAULT_SCOPES)
        context_data['GITHUB_REDIRECT_URL'] = f'{settings.URL}{reverse("authentication:github-oauth")}'
        context_data['GITHUB_INTEGRATION_SERVICE_URL'] = settings.GITHUB_INTEGRATION_SERVICE_URL

        return context_data
