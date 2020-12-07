export class Organization {
    constructor({id, name, addedAt, organizationMemberships, boards}) {
        this.id = id;
        this.name = name;
        this.addedAt = addedAt;
        this.organizationMemberships = organizationMemberships;
        this.boards = boards;
    }
}
