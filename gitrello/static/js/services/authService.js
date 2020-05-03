import {httpClient, } from "../httpClient.js";
import {tokenService, } from "./tokenService.js";
import {User} from "../models/user.js";
import {GITrelloError} from "../errors.js";

export class AuthService {
    _authTokenUrl = '/api/v1/auth-token'
    _authTokenOwnerUrl = '/api/v1/auth-token/owner'

    static _instance = null;

    constructor(tokenService, httpClient) {
        this.tokenService = tokenService;
        this.httpClient = httpClient;
    }

    static async build() {
        if (AuthService._instance != null) {
            return AuthService._instance;
        }

        const authService = new AuthService(tokenService, httpClient);
        if (tokenService.token == null) {
            authService._user = null;
            return authService;
        }

        try {
            const response = await httpClient.get({url: authService._authTokenOwnerUrl})
            authService._user = new User(
                response['id'],
                tokenService.token,
                response['username'],
                response['email'],
                response['first_name'],
                response['last_name'],
            );
        }
        catch (e) {
            console.log(e);
            authService._user = null;
        }

        AuthService._instance = authService;
        return authService;
    }

    isAuthenticated() {
        return this._user != null;
    }

    get user() {
        return this._user;
    }

    set user(user) {
        this._user = user;
        this.tokenService.token = user.token;
    }

    async logIn(userName, password) {
        const headers = {
            'Authorization': `Basic ${btoa(`${userName}:${password}`)}`,
        }
        try {
            const response = await this.httpClient.get({url: this._authTokenUrl, headers: headers});

            this.tokenService.token = response['token'];
            this._user = new User(
                response['user']['id'],
                response['token'],
                response['user']['username'],
                response['user']['email'],
                response['user']['first_name'],
                response['user']['last_name'],
            );

            return this._user;
        }
        catch (e) {
            console.log(e);
            if (e instanceof GITrelloError) {
                throw e;
            }
            throw new GITrelloError();
        }

    }

    logOut() {
        this._user = null;
        this.tokenService.token = null;
    }
}
