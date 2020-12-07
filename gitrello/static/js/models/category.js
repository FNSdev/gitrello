export class Category {
    constructor({id, priority, addedAt, name, tickets}) {
        this.id = id;
        this.priority = priority;
        this.addedAt = addedAt;
        this.name = name;
        this.tickets = tickets;
    }
}
