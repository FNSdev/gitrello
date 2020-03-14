from django.urls import path

from boards.api.views import BoardsView, BoardMembershipsView, BoardMembershipView

app_name = 'boards'

urlpatterns = [
    path('v1/boards', BoardsView.as_view(), name='boards'),
    path('v1/board-memberships', BoardMembershipsView.as_view(), name='board_memberships'),
    path('v1/board-membership/<int:id>', BoardMembershipView.as_view(), name='board_membership'),
]
