from django.urls import path

from tickets.api.views import CategoriesView

app_name = 'tickets'

urlpatterns = [
    path('v1/categories', CategoriesView.as_view(), name='categories'),
]
