from django.contrib import admin
from django.urls import path, include

import authentication.urls
import boards.urls
import core.urls
import organizations.urls
import tickets.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(authentication.urls, namespace='authentication')),
    path('api/', include(organizations.urls, namespace='organizations')),
    path('api/', include(boards.urls, namespace='boards')),
    path('api/', include(tickets.urls, namespace='tickets')),
    path('', include(core.urls, namespace='core')),
]
