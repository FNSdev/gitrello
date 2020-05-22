import {httpClient, } from "../httpClient.js";
import {BoardMembership, } from "../models/boardMembership.js";
import {GITrelloError, } from "../errors.js";
import {TicketAssignment, } from "../models/ticketAssignment.js";

class TicketAssignmentRepository {
    createTicketAssignmentUrl = '/api/v1/ticket-assignments'
    deleteTicketAssignmentUrl = '/api/v1/ticket-assignments'

    constructor(httpClient) {
        this.httpClient = httpClient;
    }

    async create(ticketId, boardMembershipId) {
        const data = {
            'ticket_id': ticketId,
            'board_membership_id': boardMembershipId,
        }

        try {
            const response = await this.httpClient.post({url: this.createTicketAssignmentUrl, data: data})
            return new TicketAssignment({
                id: response['id'],
                boardMembership: new BoardMembership({
                    id: boardMembershipId,
                })
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

    async delete(ticketAssignmentId) {
        try {
            await this.httpClient.delete({url: `${this.deleteTicketAssignmentUrl}/${ticketAssignmentId}`})
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

export const ticketAssignmentRepository = new TicketAssignmentRepository(httpClient);
