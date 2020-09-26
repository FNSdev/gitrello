import {httpClient, } from "../httpClient.js";
import {GITrelloError, } from "../errors.js";
import {Organization, } from "../models/organization.js";
import {OrganizationInvite, } from "../models/organizationInvite.js";

class OrganizationInviteRepository {
    createOrganizationInviteUrl = '/api/v1/organization-invites'

    constructor(httpClient) {
        this.httpClient = httpClient;
    }

    async create(email, message, organizationId) {
        const data = {
            'email': email,
            'message': message,
            'organization_id': organizationId,
        }

        try {
            const response = await this.httpClient.post({url: this.createOrganizationInviteUrl, data: data})
            return new OrganizationInvite({
                id: response['id'],
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

    async getAll() {
        try {
            const query = `
              query {
                organizationInvites {
                  edges {
                    node {
                      id,
                      addedAt,
                      message,
                      organizationName,
                    }
                  }
                }
              }
            `
            const response = await this.httpClient.query({query: query})
            const organizationInvites = [];
            response['data']['organizationInvites']['edges'].forEach(organizationInvite => {
                organizationInvite = organizationInvite['node'];
                organizationInvites.push(new OrganizationInvite({
                    id: organizationInvite['id'],
                    message: organizationInvite['message'],
                    addedAt: organizationInvite['addedAt'],
                    organization: new Organization({
                        name: organizationInvite['organizationName'],
                    }),
                }));
            })

            return organizationInvites;
        }
        catch (e) {
            console.log(e.message);
            if (e instanceof GITrelloError) {
                throw e;
            }
            throw new GITrelloError();
        }
    }

    async updateStatus(organizationInviteId, accept) {
        const data = {
            'accept': accept,
        }

        try {
            await this.httpClient.patch({
                url: `${this.createOrganizationInviteUrl}/${organizationInviteId}`,
                data: data,
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

export const organizationInviteRepository = new OrganizationInviteRepository(httpClient);
