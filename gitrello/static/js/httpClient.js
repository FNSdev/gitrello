import {authService, } from "./services/authService.js";
import {cookieService, } from "./services/cookieService.js";
import {HttpClientError, HttpClientPermissionDeniedError, HttpClientBadRequestError, } from "./errors.js";

export class HttpClient {
    constructor(authService, cookieService) {
        this.authService = authService;
        this.cookieService = cookieService;
    }

    async _makeRequest(url, method, data = {}) {
        const headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.cookieService.getCookie('csrftoken'),
        }

        if (this.authService.isAuthenticated()) {
            headers['Authorization'] = `Token ${this.authService.getToken()}`;
        }

        const response = await fetch(url, {
            method: method,
            headers: headers,
            body: JSON.stringify(data),
        })

        data = await response.json();

        if (response.status === 403) {
            throw new HttpClientPermissionDeniedError(data['error_message']);
        }
        if (response.status === 400) {
            throw new HttpClientBadRequestError(
                data['error_message'],
                data['error_details'],
            );
        }
        if (response.status === 500) {
            throw new HttpClientError('Service is unavailable')
        }

        return data;
    }

    async post(url, data = {}) {
        return await this._makeRequest(url, 'POST', data);
    }
}

export const httpClient = new HttpClient(authService, cookieService);
