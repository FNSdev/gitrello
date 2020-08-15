from django.urls import path

from tickets.api.views import (
    CategoriesView, CommentsView, TicketsView, TicketView, TicketAssignmentsView, TicketAssignmentView,
)

app_name = 'tickets'

urlpatterns = [
    path('v1/categories', CategoriesView.as_view(), name='categories'),
    path('v1/comments', CommentsView.as_view(), name='comments'),
    path('v1/tickets', TicketsView.as_view(), name='tickets'),
    path('v1/tickets/<int:id>', TicketView.as_view(), name='ticket'),
    path('v1/ticket-assignments', TicketAssignmentsView.as_view(), name='ticket_assignments'),
    path('v1/ticket-assignments/<int:id>', TicketAssignmentView.as_view(), name='ticket_assignment'),
]
