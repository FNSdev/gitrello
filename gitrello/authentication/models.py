from django.contrib.auth.models import AbstractUser
from django.db import models

from boards.models import BoardMembership
from organizations.models import OrganizationMembership


class User(AbstractUser):
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=100)

    def is_organization_member(self, organization_id: int) -> bool:
        return OrganizationMembership.objects \
            .filter(user_id=self.id, organization_id=organization_id) \
            .exists()

    def is_board_member(self, board_id: int) -> bool:
        return BoardMembership.objects \
            .filter(organization_membership__user_id=self.id, board_id=board_id) \
            .exists()
