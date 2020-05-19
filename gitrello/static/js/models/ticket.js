export class Ticket {
    constructor({id, addedAt, title, body, dueDate, assignees}) {
        this.id = id;
        this.addedAt = addedAt;
        this.title = title;
        this.body = body;
        this.dueDate = dueDate;
        this.assignees = assignees;
    }
}
