import {httpClient, } from "../httpClient.js";
import {GITrelloError, } from "../errors.js";
import {Comment, } from "../models/comment.js";

class CommentRepository {
    createCommentUrl = '/api/v1/comments'

    constructor(httpClient) {
        this.httpClient = httpClient;
    }

    async create(ticket, message) {
        const data = {
            'ticket_id': ticket.id,
            'message': message,
        }

        try {
            const response = await this.httpClient.post({url: this.createCommentUrl, data: data})
            return new Comment({
                id: response['id'],
                addedAt: response['added_at'],
                message: response['message'],
                ticket: ticket,
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

export const commentRepository = new CommentRepository(httpClient);
