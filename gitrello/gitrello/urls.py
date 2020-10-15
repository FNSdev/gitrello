from django.contrib import admin
from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

import authentication.urls
import boards.urls
import core.urls
import github_integration.urls
import organizations.urls
import tickets.urls
from gitrello.schema import DRFAuthenticatedGraphQLView

schema_view = get_schema_view(
   openapi.Info(
      title="GITrello API",
      default_version='v1',
      contact=openapi.Contact(email="fnsdevelopment@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny, ),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/v1/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/v1/swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/graphql', csrf_exempt(DRFAuthenticatedGraphQLView.as_view(graphiql=True))),
    path('api/', include(authentication.urls, namespace='authentication')),
    path('api/', include(organizations.urls, namespace='organizations')),
    path('api/', include(boards.urls, namespace='boards')),
    path('api/', include(tickets.urls, namespace='tickets')),
    path('oauth/', include(github_integration.urls, namespace='github_integration')),
    path('', include(core.urls, namespace='core')),
]
