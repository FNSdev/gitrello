from django.db import models


class Category(models.Model):
    class Meta:
        ordering = ['priority', ]

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    priority = models.IntegerField()
    name = models.CharField(max_length=100)
    board = models.ForeignKey(to='boards.Board', related_name='categories', on_delete=models.CASCADE)


class Ticket(models.Model):
    class Meta:
        ordering = ['priority', ]

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    priority = models.IntegerField()
    title = models.CharField(max_length=100, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    category = models.ForeignKey(to='tickets.Category', related_name='tickets', on_delete=models.CASCADE)
    assignees = models.ManyToManyField(
        to='boards.BoardMembership',
        through='tickets.TicketAssignment',
        related_name='tickets',
    )


class TicketAssignment(models.Model):
    class Meta:
        unique_together = (
            ('ticket', 'assignee'),
        )

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ticket = models.ForeignKey(to='tickets.Ticket', on_delete=models.CASCADE, related_name='assignments')
    assignee = models.ForeignKey(to='boards.BoardMembership', on_delete=models.CASCADE, related_name='assignments')


class Comment(models.Model):
    class Meta:
        ordering = ('-added_at', )

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ticket = models.ForeignKey(to='tickets.Ticket', related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(to='boards.BoardMembership', related_name='comments', on_delete=models.CASCADE)
    message = models.TextField()
