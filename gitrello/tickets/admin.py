from django.contrib import admin

from tickets.models import Category, Ticket, TicketAssignment


admin.site.register(Category)
admin.site.register(Ticket)
admin.site.register(TicketAssignment)
