import {httpClient, } from "../httpClient.js";
import {GITrelloError, } from "../errors.js";
import {Organization, } from "../models/organization.js";

class OrganizationRepository {
    createOrganizationUrl = '/api/v1/organizations';

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
}

export const organizationRepository = new OrganizationRepository(httpClient);
