import {httpClient, } from "../httpClient.js";
import {GITrelloError, RepositoryError, } from "../errors.js";
import {User, } from "../models/user.js";

class UserRepository {
    getUserUrl = '/api/v1/users';
    createUserUrl = '/api/v1/users';

    constructor(httpClient) {
        this.httpClient = httpClient;
    }

    async createUser(userName, email, firstName, lastName, password) {
        const data = {
            'username': userName,
            'email': email,
            'first_name': firstName,
            'last_name': lastName,
            'password': password,
        }

        try {
            const response = await this.httpClient.post(this.createUserUrl, data)
            return new User(
                response['id'],
                response['token'],
                userName,
                email,
                firstName,
                lastName,
            )
        }
        catch (e) {
            console.log(e.message);
            if (e instanceof GITrelloError) {
                throw new RepositoryError(e.message);
            }
            throw new GITrelloError();
        }
    }

    async getUser(id) {
        try {
            const response = await this.httpClient.get(`${this.getUserUrl}/${id}`)
            return new User(
                response['id'],
                response['token'],
                response['username'],
                response['email'],
                response['first_name'],
                response['last_name'],
            )
        }
        catch (e) {
            console.log(e.message);
            if (e instanceof GITrelloError) {
                throw new RepositoryError(e.message);
            }
            throw new GITrelloError();
        }
    }
}

export const userRepository = new UserRepository(httpClient);
