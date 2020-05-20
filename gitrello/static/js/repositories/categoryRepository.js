import {httpClient, } from "../httpClient.js";
import {Category, } from "../models/category.js";
import {GITrelloError, } from "../errors.js";

class CategoryRepository {
    createCategoryUrl = '/api/v1/categories'

    constructor(httpClient) {
        this.httpClient = httpClient;
    }

    async create(name, boardId) {
        const data = {
            'name': name,
            'board_id': boardId,
        }

        try {
            const response = await this.httpClient.post({url: this.createCategoryUrl, data: data})
            return new Category({
                id: response['id'],
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

export const categoryRepository = new CategoryRepository(httpClient);
