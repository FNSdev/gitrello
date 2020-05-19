import {cookieService, } from "./services/cookieService.js";
import {tokenService, } from "./services/tokenService.js";
import {
    GITrelloError, HttpClientError, HttpClientPermissionDeniedError, HttpClientBadRequestError,
    HttpClientUnauthorizedError,
} from "./errors.js";

export class HttpClient {
    constructor(tokenService, cookieService) {
        this.tokenService = tokenService;
        this.cookieService = cookieService;
    }

    _getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.cookieService.getCookie('csrftoken'),
        }

        if (this.tokenService.token != null) {
            headers['Authorization'] = `Token ${this.tokenService.token}`;
        }

        return headers;
    }

    async _makeRequest({url, method, data = null, headers = null}) {
        if (headers == null) {
            headers = this._getHeaders();
        }

        const init = {
            method: method,
            headers: headers,
        }

        if (data != null) {
            init['body'] = JSON.stringify(data);
        }

        const response = await fetch(url, init);
        let json = null;

        try {
            json = await response.json();
        }
        catch (e) {
            if (response.status === 204) {
                return;
            }
            throw new GITrelloError();
        }

        if (response.status === 403) {
            throw new HttpClientPermissionDeniedError(json['error_message']);
        }
        if (response.status === 401) {
            throw new HttpClientUnauthorizedError(json['error_message']);
        }
        if (response.status === 400) {
            throw new HttpClientBadRequestError(
                json['error_message'],
                json['error_details'],
            );
        }
        if (response.status === 500) {
            throw new HttpClientError('Service is unavailable')
        }

        return json;
    }

    async post({url, data = {}, headers = null}) {
        return await this._makeRequest({url: url, method: 'POST', data: data, headers: headers});
    }

    async patch({url, data = {}, headers = null}) {
        return await this._makeRequest({url: url, method: 'PATCH', data: data, headers: headers});
    }

    async delete({url, headers = null}) {
        return await this._makeRequest({url: url, method: 'DELETE', headers: headers});
    }

    async get({url, params = {}, headers = null}) {
        let paramsQuery = '?'
        for (let [key, value] of Object.entries(params)) {
            paramsQuery += `${key}=${encodeURIComponent(value.toString())}&`
        }

        return await this._makeRequest({url: url + paramsQuery, method: 'GET', headers: headers});
    }
}

export const httpClient = new HttpClient(tokenService, cookieService);
