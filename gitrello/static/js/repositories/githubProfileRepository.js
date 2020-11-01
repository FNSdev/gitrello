import {httpClient, } from "../httpClient.js";
import {GITrelloError, HttpClientNotFoundError, } from "../errors.js";
import {GithubProfile, } from "../models/githubProfile.js";

class GithubProfileRepository {
    getGithubProfileUrl = `${window.GITHUB_INTEGRATION_SERVICE_URL}/api/v1/github-profile`;
    deleteGithubProfileUrl = `${window.GITHUB_INTEGRATION_SERVICE_URL}/api/v1/github-profile`;

    constructor(httpClient) {
        this.httpClient = httpClient;
    }

    async get() {
        try {
            const response = await this.httpClient.get({url: this.getGithubProfileUrl})
            return new GithubProfile({
                id: response['id'],
                githubUserId: response['github_user_id'],
                githubLogin: response['github_login'],
            })
        }
        catch (e) {
            console.log(e.message);
            if (e instanceof HttpClientNotFoundError) {
                return null;
            }
            if (e instanceof GITrelloError) {
                throw e;
            }
            throw new GITrelloError();
        }
    }

    async delete() {
        try {
            return await this.httpClient.delete({url: this.deleteGithubProfileUrl})
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

export const githubProfileRepository = new GithubProfileRepository(httpClient);
