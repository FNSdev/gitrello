import {authService, } from "../services/authService.js";

export class Page {
    constructor(params = {}) {
        this.params = params;
        this.authService = authService;
    }

    beforeRender() {
    }

    getTemplate() {
    }

    afterRender() {
    }
}
