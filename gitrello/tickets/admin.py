from django.contrib import admin

from tickets.models import Category, Comment, Ticket, TicketAssignment


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Ticket)
admin.site.register(TicketAssignment)
