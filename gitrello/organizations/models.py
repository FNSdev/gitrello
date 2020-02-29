from django.db import models

from organizations.choices import OrganizationMemberRole, OrganizationInviteStatus


class Organization(models.Model):
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(
        to='authentication.User',
        through='organizations.OrganizationMembership',
        related_name='organizations',
    )
    invites = models.ManyToManyField(
        to='authentication.User',
        through='organizations.OrganizationInvite',
        related_name='invites',
    )

    def __str__(self):
        return self.name


class OrganizationMembership(models.Model):
    class Meta:
        unique_together = (
            ('organization', 'user'),
        )

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    organization = models.ForeignKey(to=Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE)
    role = models.CharField(
        max_length=30,
        choices=OrganizationMemberRole.CHOICES,
        default=OrganizationMemberRole.MEMBER
    )


class OrganizationInvite(models.Model):
    class Meta:
        unique_together = (
            ('organization', 'user'),
        )

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    organization = models.ForeignKey(to=Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(to='authentication.User', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=30,
        choices=OrganizationInviteStatus.CHOICES,
        default=OrganizationInviteStatus.PENDING,
    )
    message = models.TextField()
