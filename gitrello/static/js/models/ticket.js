export class Ticket {
    constructor({id, addedAt, title, body, dueDate, assignments}) {
        this.id = id;
        this.addedAt = addedAt;
        this.title = title;
        this.body = body;
        this.dueDate = dueDate;
        this.assignments = assignments;
    }
}
