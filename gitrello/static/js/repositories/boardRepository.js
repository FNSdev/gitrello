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
    createBoardUrl = '/api/v1/boards'
    getBoardUrl = '/api/v1/boards'

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
            const response = await this.httpClient.get({url: `${this.getBoardUrl}/${boardId}`})

            const boardMemberships = [];
            response['board_memberships'].forEach(boardMembership => {
                boardMemberships.push(new BoardMembership({
                    id: boardMembership['id'],
                    addedAt: boardMembership['added_at'],
                    organizationMembership: new OrganizationMembership({
                        id: boardMembership['organization_membership']['id'],
                        role: boardMembership['organization_membership']['role'],
                        user: new User({
                            id: boardMembership['organization_membership']['user']['id'],
                            addedAt: boardMembership['organization_membership']['user']['added_at'],
                            firstName: boardMembership['organization_membership']['user']['first_name'],
                            lastName: boardMembership['organization_membership']['user']['last_name'],
                            email: boardMembership['organization_membership']['user']['email'],
                            username: boardMembership['organization_membership']['user']['username'],
                        })
                    })
                }))
            });

            const categories = [];
            response['categories'].forEach(category => {
                const tickets = [];
                category['tickets'].forEach(ticket => {
                    const assignments = [];
                    ticket['assignments'].forEach(assignment => {
                        assignments.push(new TicketAssignment({
                            id: assignment['id'],
                            addedAt: assignment['added_at'],
                            boardMembership: new BoardMembership({
                                id: assignment['assignee']['id'],
                                addedAt: assignment['assignee']['added_at'],
                                organizationMembership: new OrganizationMembership({
                                    id: assignment['assignee']['organization_membership']['id'],
                                    role: assignment['assignee']['organization_membership']['role'],
                                    user: new User({
                                        id: assignment['assignee']['organization_membership']['user']['id'],
                                        addedAt: assignment['assignee']['organization_membership']['user']['added_at'],
                                        firstName: assignment['assignee']['organization_membership']['user']['first_name'],
                                        lastName: assignment['assignee']['organization_membership']['user']['last_name'],
                                        email: assignment['assignee']['organization_membership']['user']['email'],
                                        username: assignment['assignee']['organization_membership']['user']['username'],
                                    })
                                })
                            })
                        }));
                    })

                    tickets.push(new Ticket({
                        id: ticket['id'],
                        addedAt: ticket['added_at'],
                        title: ticket['title'],
                        body: ticket['body'],
                        dueDate: ticket['due_date'],
                        assignments: assignments,
                    }))
                })

                categories.push(new Category({
                    id: category['id'],
                    addedAt: category['added_at'],
                    name: category['name'],
                    tickets: tickets,
                }))
            });

            return new Board({
                id: response['id'],
                name: response['name'],
                addedAt: response['added_at'],
                categories: categories,
                boardMemberships: boardMemberships,
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

export const boardRepository = new BoardRepository(httpClient);
