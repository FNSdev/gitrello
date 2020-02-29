class OrganizationMemberRole:
    OWNER = 'OWNER'
    ADMIN = 'ADMIN'
    MEMBER = 'MEMBER'

    CHOICES = (
        (OWNER, 'Owner'),
        (ADMIN, 'Admin'),
        (MEMBER, 'Member'),
    )


class OrganizationInviteStatus:
    PENDING = 'PENDING'
    ACCEPTED = 'ACCEPTED'
    DECLINED = 'DECLINED'

    CHOICES = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declined'),
    )
