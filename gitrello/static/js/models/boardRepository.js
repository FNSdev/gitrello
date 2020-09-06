export class BoardRepository {
    constructor({id, boardId, repositoryName, repositoryOwner}) {
        this.id = id;
        this.boardId = boardId;
        this.repositoryName = repositoryName;
        this.repositoryOwner = repositoryOwner;
    }
}
