import {httpClient, } from "../httpClient.js";
import {GITrelloError, } from "../errors.js";
import {Organization, } from "../models/organization.js";
import {OrganizationInvite, } from "../models/organizationInvite.js";

class OrganizationInviteRepository {
    createOrganizationInviteUrl = '/api/v1/organization-invites'
    getOrganizationInvitesUrl = '/api/v1/organization-invites'

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
                status: response['status'],
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
            const response = await this.httpClient.get({url: this.getOrganizationInvitesUrl})

            const organizationInvites = [];
            response.forEach(organizationInvite => {
                organizationInvites.push(new OrganizationInvite({
                    id: organizationInvite['id'],
                    status: organizationInvite['status'],
                    message: organizationInvite['message'],
                    addedAt: organizationInvite['added_at'],
                    organization: new Organization({
                        id: organizationInvite['organization']['id'],
                        addedAt: organizationInvite['organization']['added_at'],
                        name: organizationInvite['organization']['name'],
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
            const response = await this.httpClient.patch({
                url: `${this.createOrganizationInviteUrl}/${organizationInviteId}`,
                data: data,
            });
            return new OrganizationInvite({
                id: response['id'],
                status: response['status'],
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

export const organizationInviteRepository = new OrganizationInviteRepository(httpClient);
