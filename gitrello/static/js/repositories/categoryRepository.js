import {httpClient, } from "../httpClient.js";
import {Category, } from "../models/category.js";
import {GITrelloError, } from "../errors.js";

class CategoryRepository {
    resourceUrl = '/api/v1/categories'

    constructor(httpClient) {
        this.httpClient = httpClient;
    }

    async create(name, boardId) {
        const data = {
            'name': name,
            'board_id': boardId,
        }

        try {
            const response = await this.httpClient.post({url: this.resourceUrl, data: data})
            return new Category({
                id: response['id'],
                priority: response['priority'],
                name: response['name'],
                tickets: [],
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

    async move(category, insertAfterCategoryId) {
        try {
            const response = await this.httpClient.post({
                url: `${this.resourceUrl}/${category.id}/actions/move`,
                data: {'insert_after_category_id': insertAfterCategoryId},
            });

            category.priority = response['priority'];
            return category;
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
