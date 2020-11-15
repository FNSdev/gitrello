import {httpClient, } from "../httpClient.js";
import {Comment, } from "../models/comment.js";
import {Ticket, } from "../models/ticket.js";
import {GITrelloError, } from "../errors.js";

class TicketRepository {
    resourceUrl = '/api/v1/tickets'

    constructor(httpClient) {
        this.httpClient = httpClient;
    }

    async create(categoryId) {
        const data = {
            'category_id': categoryId,
        }

        try {
            const response = await this.httpClient.post({url: this.resourceUrl, data: data})
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

    async getTicketDetails(ticketId) {
        try {
            const query = `
            query {
              ticket (id: "${ticketId}") {
                body,
                comments {
                  edges {
                    node {
                      id,
                      addedAt,
                      message,
                      author {
                        organizationMembership {
                          user {
                            firstName,
                            lastName,
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
            `

            const response = await this.httpClient.query({query: query});
            const comments = [];

            response['data']['ticket']['comments']['edges'].forEach(comment => {
               comment = comment['node'];
               comments.push(new Comment({
                   id: comment['id'],
                   addedAt: comment['addedAt'],
                   message: comment['message'],
                   authorFirstName: comment['author']['organizationMembership']['user']['firstName'],
                   authorLastName: comment['author']['organizationMembership']['user']['lastName'],
               }));
            });

            return new Ticket({
                body: response['data']['ticket']['body'],
                comments: comments,
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

    async update(ticket, {title= null, body = null, dueDate = null}) {
        try {
            const response = await this.httpClient.patch({
                url: `${this.resourceUrl}/${ticket.id}`,
                data: {
                    'title': title,
                    'body': body,
                    'due_date': dueDate,
                },
            });

            ticket.title = response['title'];
            ticket.body = response['body'];
            ticket.dueDate = response['due_date'];

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

    async move(ticket, insertAfterTicketId, categoryId) {
        try {
            const response = await this.httpClient.post({
                url: `${this.resourceUrl}/${ticket.id}/actions/move`,
                data: {
                    'insert_after_ticket_id': insertAfterTicketId,
                    'category_id': categoryId,
                },
            });

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

    async delete(ticketId) {
        try {
            await this.httpClient.delete({url: `${this.resourceUrl}/${ticketId}`})
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
