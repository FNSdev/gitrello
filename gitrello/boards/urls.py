from django.urls import path

from boards.api.views import BoardsView, BoardMembershipsView, BoardMembershipView, BoardView

app_name = 'boards'

urlpatterns = [
    path('v1/boards', BoardsView.as_view(), name='boards'),
    path('v1/boards/<int:id>', BoardView.as_view(), name='board'),
    path('v1/board-memberships', BoardMembershipsView.as_view(), name='board_memberships'),
    path('v1/board-memberships/<int:id>', BoardMembershipView.as_view(), name='board_membership'),
]
