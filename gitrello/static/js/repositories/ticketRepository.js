import {httpClient, } from "../httpClient.js";
import {Ticket, } from "../models/ticket.js";
import {GITrelloError, } from "../errors.js";

class TicketRepository {
    createTicketUrl = '/api/v1/tickets'

    constructor(httpClient) {
        this.httpClient = httpClient;
    }

    async create(categoryId) {
        const data = {
            'category_id': categoryId,
        }

        try {
            const response = await this.httpClient.post({url: this.createTicketUrl, data: data})
            return new Ticket({
                id: response['id'],
                title: null,
                dueDate: null,
                assignees: [],
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

export const ticketRepository = new TicketRepository(httpClient);
