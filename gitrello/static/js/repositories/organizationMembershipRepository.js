import {httpClient, } from "../httpClient.js";
import {BoardMembership, } from "../models/boardMembership.js";
import {GITrelloError, } from "../errors.js";
import {Board, } from "../models/board.js";
import {Organization, } from "../models/organization.js";
import {OrganizationMembership, } from "../models/organizationMembership.js";


class OrganizationMembershipRepository {
    resourceUrl = '/api/v1/organization-memberships'

    constructor(httpClient) {
        this.httpClient = httpClient;
    }

    async getAll() {
        try {
            const query = `
              query {
                organizationMemberships {
                  edges {
                    node {
                      id,
                      role,
                      organization {
                        id,
                        name,
                      },
                      boardMemberships {
                        edges {
                          node {
                            id,
                            board {
                              id,
                              name,
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            `
            const response = await this.httpClient.query({query: query})
            const organizationMemberships = [];
            response['data']['organizationMemberships']['edges'].forEach(organizationMembership => {
                const boardMemberships = [];
                organizationMembership = organizationMembership['node'];
                organizationMembership['boardMemberships']['edges'].forEach(boardMembership => {
                    boardMembership = boardMembership['node'];
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
            await this.httpClient.delete({url: `${this.resourceUrl}/${organizationMembershipId}`})
        }
        catch (e) {
            console.log(e.message);
            if (e instanceof GITrelloError) {
                throw e;
            }
            throw new GITrelloError();
        }
    }

    async updateRole(organizationMembershipId, newRole) {
        try {
            const data = {'role': newRole};
            const response = await this.httpClient.patch({
                url: `${this.resourceUrl}/${organizationMembershipId}`,
                data: data,
            })

            return response['role'];
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
