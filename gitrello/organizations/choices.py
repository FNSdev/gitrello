class OrganizationMemberRole:
    OWNER = 'OWNER'
    ADMIN = 'ADMIN'
    MEMBER = 'MEMBER'

    CHOICES = (
        (OWNER, 'Owner'),
        (ADMIN, 'Admin'),
        (MEMBER, 'Member'),
    )
