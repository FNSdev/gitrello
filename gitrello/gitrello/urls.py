from django.contrib import admin
from django.urls import path, include

import authentication.urls
import organizations.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(authentication.urls, namespace='authentication')),
    path('api/', include(organizations.urls, namespace='organizations')),
]
