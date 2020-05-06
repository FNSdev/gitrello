from django.urls import re_path

from core.views import IndexView

app_name = 'core'

urlpatterns = [
    re_path(r'^.*$', IndexView.as_view(), name='index'),
]
