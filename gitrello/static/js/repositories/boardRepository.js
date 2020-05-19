import {httpClient, } from "../httpClient.js";
import {GITrelloError, } from "../errors.js";
import {Board, } from "../models/board.js";

class BoardRepository {
    createBoardUrl = '/api/v1/boards';

    constructor(httpClient) {
        this.httpClient = httpClient;
    }

    async create(name, organizationId) {
        const data = {
            'name': name,
            'organization_id': organizationId,
        }

        try {
            const response = await this.httpClient.post({url: this.createBoardUrl, data: data})
            return new Board({
                id: response['id'].toString(),
                name: response['name'],
            })
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

export const boardRepository = new BoardRepository(httpClient);
