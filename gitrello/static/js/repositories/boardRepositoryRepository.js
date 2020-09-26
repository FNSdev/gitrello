import {httpClient, } from "../httpClient.js";
import {GITrelloError, HttpClientNotFoundError, } from "../errors.js";
import {BoardRepository, } from "../models/boardRepository.js";

class BoardRepositoryRepository {
    getBoardRepositoryUrl = `${window.GITHUB_INTEGRATION_SERVICE_URL}/api/v1/board-repository`;
    createOrUpdateBoardRepositoryUrl = `${window.GITHUB_INTEGRATION_SERVICE_URL}/api/v1/board-repositories`;

    constructor(httpClient) {
        this.httpClient = httpClient;
    }

    async getByBoardId(boardId) {
        const params = {
            'board_id': boardId,
        }

        try {
            const response = await this.httpClient.get({url: this.getBoardRepositoryUrl, params})

            return new BoardRepository({
                id: response['id'],
                boardId: response['board_id'],
                repositoryName: response['repository_name'],
                repositoryOwner: response['repository_owner'],
            });
        }
        catch (e) {
            console.log(e.message);
            if(e instanceof HttpClientNotFoundError) {
                return null;
            }
            if (e instanceof GITrelloError) {
                throw e;
            }
            throw new GITrelloError();
        }
    }

    async createOrUpdate(boardId, repositoryName, repositoryOwner) {
        const data = {
            'board_id': boardId,
            'repository_name': repositoryName,
            'repository_owner': repositoryOwner,
        }

        try {
            const response = await this.httpClient.put({url: this.createOrUpdateBoardRepositoryUrl, data});

            return new BoardRepository({
                id: response['id'],
                boardId: response['board_id'],
                repositoryName: response['repository_name'],
                repositoryOwner: response['repository_owner'],
            });
        }
        catch (e) {
            console.log(e.message);
            if (e instanceof GITrelloError) {
                throw e;
            }
            throw new GITrelloError();
        }
    }
}

export const boardRepositoryRepository = new BoardRepositoryRepository(httpClient);
