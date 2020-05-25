import {httpClient, } from "../httpClient.js";
import {Ticket, } from "../models/ticket.js";
import {GITrelloError, } from "../errors.js";

class TicketRepository {
    createTicketUrl = '/api/v1/tickets'
    updateTicketUrl = '/api/v1/tickets'

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
                priority: response['priority'],
                title: null,
                body: null,
                dueDate: null,
                assignments: [],
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

    async update(ticket, {title= null, body = null, dueDate = null, priority = null, categoryId = null}) {
        try {
            const response = await this.httpClient.patch({
                url: `${this.updateTicketUrl}/${ticket.id}`,
                data: {
                    'title': title,
                    'body': body,
                    'due_date': dueDate,
                    'priority': priority,
                    'category_id': categoryId,
                }
            });

            ticket.title = response['title'];
            ticket.body = response['body'];
            ticket.dueDate = response['due_date'];
            ticket.priority = response['priority'];

            return ticket;
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
