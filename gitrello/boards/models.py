from django.db import models


class Board(models.Model):
    class Meta:
        ordering = ('-added_at', )
        unique_together = (
            ('name', 'organization'),
        )

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)
    organization = models.ForeignKey(to='organizations.Organization', related_name='boards', on_delete=models.CASCADE)
    members = models.ManyToManyField(
        to='organizations.OrganizationMembership',
        through='boards.BoardMembership',
        related_name='boards',
    )


class BoardMembership(models.Model):
    class Meta:
        unique_together = (
            ('board', 'organization_membership'),
        )

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    board = models.ForeignKey(to='boards.Board', on_delete=models.CASCADE, related_name='board_memberships')
    organization_membership = models.ForeignKey(
        to='organizations.OrganizationMembership',
        on_delete=models.CASCADE,
        related_name='board_memberships',
    )
