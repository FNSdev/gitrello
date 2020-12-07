from django.urls import path

from tickets.api.views import (
    CategoryActionsViewSet, CategoriesView, CategoryView, CommentsView, TicketActionsViewSet, TicketsView, TicketView,
    TicketAssignmentsView, TicketAssignmentView,
)

app_name = 'tickets'

urlpatterns = [
    path('v1/categories', CategoriesView.as_view(), name='categories'),
    path('v1/categories/<int:id>', CategoryView.as_view(), name='category'),
    path('v1/categories/<int:id>/actions/move', CategoryActionsViewSet.as_view({'post': 'move'}), name='move-category'),
    path('v1/comments', CommentsView.as_view(), name='comments'),
    path('v1/tickets', TicketsView.as_view(), name='tickets'),
    path('v1/tickets/<int:id>', TicketView.as_view(), name='ticket'),
    path('v1/tickets/<int:id>/actions/move', TicketActionsViewSet.as_view({'post': 'move'}), name='move-ticket'),
    path('v1/ticket-assignments', TicketAssignmentsView.as_view(), name='ticket_assignments'),
    path('v1/ticket-assignments/<int:id>', TicketAssignmentView.as_view(), name='ticket_assignment'),
]
