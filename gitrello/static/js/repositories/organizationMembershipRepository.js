import {httpClient, } from "../httpClient.js";
import {BoardMembership, } from "../models/boardMembership.js";
import {GITrelloError, } from "../errors.js";
import {Board, } from "../models/board.js";
import {Organization, } from "../models/organization.js";
import {OrganizationMembership, } from "../models/organizationMembership.js";


class OrganizationMembershipRepository {
    getOrganizationMembershipsUrl = '/api/v1/organization-memberships'
    deleteOrganizationMembershipUrl = '/api/v1/organization-memberships'

    constructor(httpClient) {
        this.httpClient = httpClient;
    }

    async getAll() {
        try {
            const response = await this.httpClient.get({url: this.getOrganizationMembershipsUrl})
            const organizationMemberships = [];
            response.forEach(organizationMembership => {
                const boardMemberships = [];
                organizationMembership['board_memberships'].forEach(boardMembership => {
                    boardMemberships.push(new BoardMembership({
                        id: boardMembership['id'],
                        board: new Board({
                            id: boardMembership['board']['id'],
                            name: boardMembership['board']['name'],
                        }),
                    }));
                });
                organizationMemberships.push(new OrganizationMembership({
                    id: organizationMembership['id'],
                    role: organizationMembership['role'],
                    organization: new Organization({
                        id: organizationMembership['organization']['id'],
                        name: organizationMembership['organization']['name'],
                        addedAt: organizationMembership['organization']['added_at'],
                    }),
                    boardMemberships: boardMemberships,
                }))
            });

            return organizationMemberships;
        }
        catch (e) {
            console.log(e.message);
            if (e instanceof GITrelloError) {
                throw e;
            }
            throw new GITrelloError();
        }
    }

    async delete(organizationMembershipId) {
        try {
            await this.httpClient.delete({url: `${this.deleteOrganizationMembershipUrl}/${organizationMembershipId}`})
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

export const organizationMembershipRepository = new OrganizationMembershipRepository(httpClient);
