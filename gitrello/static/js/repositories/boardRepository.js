import {httpClient, } from "../httpClient.js";
import {GITrelloError, } from "../errors.js";
import {Board, } from "../models/board.js";
import {BoardMembership, } from "../models/boardMembership.js";
import {Category, } from "../models/category.js";
import {OrganizationMembership, } from "../models/organizationMembership.js";
import {Ticket, } from "../models/ticket.js";
import {TicketAssignment, } from "../models/ticketAssignment.js";
import {User, } from "../models/user.js";

class BoardRepository {
    createBoardUrl = '/api/v1/boards';

    constructor(httpClient) {
        this.httpClient = httpClient;
    }

    async create(name, organizationId) {
        const data = {
            'name': name,
            'organization_id': organizationId,
        }

        try {
            const response = await this.httpClient.post({url: this.createBoardUrl, data: data})
            return new Board({
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

    async get(boardId) {
        try {
            const query = `
            query {
              board (id: "${boardId}") {
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
                          username,
                          email,
                        }
                      }
                    }
                  }
                },
                categories {
                  edges {
                    node {
                      id,
                      name,
                      tickets {
                        edges {
                          node {
                            id,
                            addedAt,
                            title,
                            dueDate,
                            priority,
                            assignments {
                              edges {
                                node {
                                  id,
                                  assignee {
                                    id,
                                    organizationMembership {
                                      id,
                                      user {
                                        id,
                                        firstName,
                                        lastName,
                                        username,
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
                  }
                }
              }          
            }
            `
            const response = await this.httpClient.query({query: query})
            const boardMemberships = [];
            response['data']['board']['boardMemberships']['edges'].forEach(boardMembership => {
                boardMembership = boardMembership['node'];
                boardMemberships.push(new BoardMembership({
                    id: boardMembership['id'],
                    organizationMembership: new OrganizationMembership({
                        id: boardMembership['organizationMembership']['id'],
                        role: boardMembership['organizationMembership']['role'],
                        user: new User({
                            id: boardMembership['organizationMembership']['user']['id'],
                            firstName: boardMembership['organizationMembership']['user']['firstName'],
                            lastName: boardMembership['organizationMembership']['user']['lastName'],
                            email: boardMembership['organizationMembership']['user']['email'],
                            username: boardMembership['organizationMembership']['user']['username'],
                        })
                    })
                }))
            });
            const categories = [];
            response['data']['board']['categories']['edges'].forEach(category => {
                const tickets = [];
                category = category['node'];
                category['tickets']['edges'].forEach(ticket => {
                    const assignments = [];
                    ticket = ticket['node'];
                    ticket['assignments']['edges'].forEach(assignment => {
                        assignment = assignment['node'];
                        assignments.push(new TicketAssignment({
                            id: assignment['id'],
                            boardMembership: new BoardMembership({
                                id: assignment['assignee']['id'],
                                organizationMembership: new OrganizationMembership({
                                    id: assignment['assignee']['organizationMembership']['id'],
                                    user: new User({
                                        id: assignment['assignee']['organizationMembership']['user']['id'],
                                        firstName: assignment['assignee']['organizationMembership']['user']['firstName'],
                                        lastName: assignment['assignee']['organizationMembership']['user']['lastName'],
                                        email: assignment['assignee']['organizationMembership']['user']['email'],
                                        username: assignment['assignee']['organizationMembership']['user']['username'],
                                    })
                                })
                            })
                        }));
                    })
                    tickets.push(new Ticket({
                        id: ticket['id'],
                        addedAt: ticket['addedAt'],
                        title: ticket['title'],
                        dueDate: ticket['dueDate'],
                        assignments: assignments,
                        priority: ticket['priority'],
                    }))
                })
                categories.push(new Category({
                    id: category['id'],
                    name: category['name'],
                    tickets: tickets,
                }))
            });

            return new Board({
                id: response['data']['board']['id'],
                name: response['data']['board']['name'],
                categories: categories,
                boardMemberships: boardMemberships,
            });
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

export const boardRepository = new BoardRepository(httpClient);
