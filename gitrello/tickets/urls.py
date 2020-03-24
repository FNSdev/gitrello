from django.urls import path

from tickets.api.views import (
    CategoriesView, TicketsView, TicketView, TicketAssignmentsView, TicketAssignmentView,
)

app_name = 'tickets'

urlpatterns = [
    path('v1/categories', CategoriesView.as_view(), name='categories'),
    path('v1/tickets', TicketsView.as_view(), name='tickets'),
]
