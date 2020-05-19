export class BoardMembership {
    constructor({id, board, addedAt, organizationMembership}) {
        this.id = id;
        this.board = board;
        this.addedAt = addedAt;
        this.organizationMembership = organizationMembership;
    }
}
