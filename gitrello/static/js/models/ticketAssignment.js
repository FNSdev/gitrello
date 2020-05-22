export class TicketAssignment {
    constructor({id, addedAt, ticket, boardMembership}) {
        this.id = id;
        this.addedAt = addedAt;
        this.ticket = ticket;
        this.boardMembership = boardMembership;
    }
}
