import {httpClient, } from "../httpClient.js";
import {GITrelloError, } from "../errors.js";
import {OauthState, } from "../models/oauthState.js";

class OauthStateRepository {
    createOauthStateUrl = '/api/v1/oauth-states';

    // Providers
    GITHUB_PROVIDER = 'GITHUB';

    constructor(httpClient) {
        this.httpClient = httpClient;
    }

    async create(provider) {
        const data = {
            'provider': provider,
        }

        try {
            const response = await this.httpClient.post({url: this.createOauthStateUrl, data: data})
            return new OauthState({
                id: response['id'],
                provider: response['provider'],
                state: response['state'],
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

export const oauthStateRepository = new OauthStateRepository(httpClient);
