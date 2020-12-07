from django.contrib import admin

from boards.models import Board, BoardMembership


admin.site.register(Board)
admin.site.register(BoardMembership)
