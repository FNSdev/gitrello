from django.contrib import admin
from django.urls import path, include

import authentication.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(authentication.urls, namespace='auth')),
]
