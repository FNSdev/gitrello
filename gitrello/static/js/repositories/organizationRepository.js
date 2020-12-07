import {httpClient, } from "../httpClient.js";
import {GITrelloError, } from "../errors.js";
import {Board, } from "../models/board.js";
import {BoardMembership, } from "../models/boardMembership.js";
import {Organization, } from "../models/organization.js";
import {OrganizationMembership, } from "../models/organizationMembership.js";
import {User, } from "../models/user.js";

class OrganizationRepository {
    createOrganizationUrl = '/api/v1/organizations'

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

    async get(organizationId) {
        try {
            const query = `
              query {
                organization (id: "${organizationId}") {
                  id,
                  name,
                  organizationMemberships {
                    edges {
                      node {
                        id,
                        role,
                        user {
                          id,
                          firstName,
                          lastName,
                          username,
                          email,
                        }
                      }
                    }
                  },
                  boards {
                    edges {
                      node {
                        id,
                        name,
                        boardMemberships {
                          edges {
                            node {
                              id,
                              organizationMembership {
                                id,
                                role,
                                user {
                                  id,
                                  firstName,
                                  lastName,
                                  email,
                                }
                              }
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
            response['data']['organization']['organizationMemberships']['edges'].forEach(organizationMembership => {
                organizationMembership = organizationMembership['node'];
                organizationMemberships.push(new OrganizationMembership({
                     id: organizationMembership['id'],
                     role: organizationMembership['role'],
                     user: new User({
                         id: organizationMembership['user']['id'],
                         username: organizationMembership['user']['username'],
                         email: organizationMembership['user']['email'],
                         firstName: organizationMembership['user']['firstName'],
                         lastName: organizationMembership['user']['lastName'],
                     }),
                 }));
            });
            const boards = [];
            response['data']['organization']['boards']['edges'].forEach(board => {
                const boardMemberships = [];
                board = board['node'];
                board['boardMemberships']['edges'].forEach(boardMembership => {
                    boardMembership = boardMembership['node'];
                    boardMemberships.push(new BoardMembership({
                        id: boardMembership['id'],
                        organizationMembership: new OrganizationMembership({
                             id: boardMembership['organizationMembership']['id'],
                             role: boardMembership['organizationMembership']['role'],
                             user: new User({
                                 id: boardMembership['organizationMembership']['user']['id'],
                                 username: boardMembership['organizationMembership']['user']['username'],
                                 email: boardMembership['organizationMembership']['user']['email'],
                                 firstName: boardMembership['organizationMembership']['user']['firstName'],
                                 lastName: boardMembership['organizationMembership']['user']['lastName'],
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
                id: response['data']['organization']['id'],
                name: response['data']['organization']['name'],
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
