import {httpClient, } from "../httpClient.js";
import {GITrelloError, } from "../errors.js";
import {OrganizationInvite, } from "../models/organizationInvite.js";

class OrganizationInviteRepository {
    createOrganizationInviteUrl = '/api/v1/organization-invites';

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
}

export const organizationInviteRepository = new OrganizationInviteRepository(httpClient);
