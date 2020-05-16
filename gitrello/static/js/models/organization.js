export class Organization {
    constructor({id, name, added_at, organizationMemberships, boards}) {
        this.id = id;
        this.name = name;
        this.added_at = added_at;
        this.organizationMemberships = organizationMemberships;
        this.boards = boards;
    }
}
