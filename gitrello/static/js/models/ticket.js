export class Ticket {
    constructor({id, addedAt, title, body, dueDate, assignments, priority, comments}) {
        this.id = id;
        this.addedAt = addedAt;
        this.title = title;
        this.body = body;
        this.dueDate = dueDate;
        this.assignments = assignments;
        this.priority = priority;
        this.comments = comments;
    }
}
