import {httpClient, } from "../httpClient.js";
import {GITrelloError, } from "../errors.js";
import {GithubRepository, } from "../models/githubRepository.js";

class GithubRepositoryRepository {
    getGithubRepositoriesUrl = `${window.GITHUB_INTEGRATION_SERVICE_URL}/api/v1/github-repositories`;

    constructor(httpClient) {
        this.httpClient = httpClient;
    }

    async getAll() {
        try {
            const response = await this.httpClient.get({url: this.getGithubRepositoriesUrl})

            const githubRepositories = [];
            response.forEach(githubRepository => {
                githubRepositories.push(
                    new GithubRepository({
                        name: githubRepository['name'],
                        owner: githubRepository['owner'],
                    }),
                );
            })

            return githubRepositories;
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

export const githubRepositoryRepository = new GithubRepositoryRepository(httpClient);
