export class Board {
    constructor({id, name, addedAt, boardMemberships, organization, categories}) {
        this.id = id;
        this.name = name;
        this.addedAt = addedAt;
        this.boardMemberships = boardMemberships;
        this.organization = organization;
        this.categories = categories;
    }
}
