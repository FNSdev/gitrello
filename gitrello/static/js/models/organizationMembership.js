export class Role {
    static MEMBER = 'MEMBER'
    static ADMIN = 'ADMIN'
    static OWNER = 'OWNER'
}

export class OrganizationMembership {
    constructor({id, role, organization, user, boardMemberships}) {
        this.id = id;
        this.role = role;
        this.organization = organization;
        this.boardMemberships = boardMemberships;
        this.user = user;
    }
}
