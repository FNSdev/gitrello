import {httpClient, } from "../httpClient.js";
import {GITrelloError, } from "../errors.js";
import {BoardMembership, } from "../models/boardMembership.js";
import {OrganizationMembership, } from "../models/organizationMembership.js";

class BoardMembershipRepository {
    createBoardMembershipUrl = '/api/v1/board-memberships'
    deleteBoardMembershipUrl = '/api/v1/board-memberships'

    constructor(httpClient) {
        this.httpClient = httpClient;
    }

    async create(boardId, organizationMembershipId) {
        const data = {
            'board_id': boardId,
            'organization_membership_id': organizationMembershipId,
        }

        try {
            const response = await this.httpClient.post({url: this.createBoardMembershipUrl, data: data})
            return new BoardMembership({
                id: response['id'],
                organizationMembership: new OrganizationMembership({id: organizationMembershipId}),
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

    async delete(boardMembershipId) {
        try {
            await this.httpClient.delete({url: `${this.createBoardMembershipUrl}/${boardMembershipId}`})
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

export const boardMembershipRepository = new BoardMembershipRepository(httpClient);
