export class Comment {
    constructor({id, addedAt, message, ticket, authorFirstName, authorLastName}) {
        this.id = id;
        this.addedAt = addedAt;
        this.message = message;
        this.ticket = ticket;
        this.authorFirstName = authorFirstName;
        this.authorLastName = authorLastName;
    }
}
