export class Organization {
    constructor({id, name, added_at: addedAt, organizationMemberships, boards}) {
        this.id = id;
        this.name = name;
        this.added_at = addedAt;
        this.organizationMemberships = organizationMemberships;
        this.boards = boards;
    }
}
