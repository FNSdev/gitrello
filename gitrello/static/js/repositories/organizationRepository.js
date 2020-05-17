import {httpClient, } from "../httpClient.js";
import {GITrelloError, } from "../errors.js";
import {Board, } from "../models/board.js";
import {BoardMembership, } from "../models/boardMembership.js";
import {Organization, } from "../models/organization.js";
import {OrganizationMembership, } from "../models/organizationMembership.js";
import {User, } from "../models/user.js";

class OrganizationRepository {
    createOrganizationUrl = '/api/v1/organizations'
    getOrganizationUrl = '/api/v1/organizations'

    constructor(httpClient) {
        this.httpClient = httpClient;
    }

    async create(name) {
        const data = {
            'name': name,
        }

        try {
            const response = await this.httpClient.post({url: this.createOrganizationUrl, data: data})
            return new Organization({
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

    async get(id) {
        try {
            const response = await this.httpClient.get({url: `${this.getOrganizationUrl}/${id}`})

            const organizationMemberships = [];
            response['organization_memberships'].forEach(organizationMembership => {
                 organizationMemberships.push(new OrganizationMembership({
                     id: organizationMembership['id'],
                     role: organizationMembership['role'],
                     user: new User({
                         id: organizationMembership['user']['id'],
                         username: organizationMembership['user']['username'],
                         email: organizationMembership['user']['email'],
                         firstName: organizationMembership['user']['first_name'],
                         lastName: organizationMembership['user']['last_name'],
                     }),
                 }));
            });

            const boards = [];
            response['boards'].forEach(board => {
                const boardMemberships = []
                board['board_memberships'].forEach(boardMembership => {
                    boardMemberships.push(new BoardMembership({
                        id: boardMembership['id'],
                        organizationMembership: new OrganizationMembership({
                             id: boardMembership['organization_membership']['id'],
                             role: boardMembership['organization_membership']['role'],
                             user: new User({
                                 id: boardMembership['organization_membership']['user']['id'],
                                 username: boardMembership['organization_membership']['user']['username'],
                                 email: boardMembership['organization_membership']['user']['email'],
                                 firstName: boardMembership['organization_membership']['user']['first_name'],
                                 lastName: boardMembership['organization_membership']['user']['last_name'],
                             }),
                        })
                    }));
                })

                boards.push(new Board({
                    id: board['id'],
                    name: board['name'],
                    boardMemberships: boardMemberships,
                }));
            });

            return new Organization({
                id: response['id'],
                name: response['name'],
                addedAt: response['added_at'],
                organizationMemberships: organizationMemberships,
                boards: boards,
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

export const organizationRepository = new OrganizationRepository(httpClient);
