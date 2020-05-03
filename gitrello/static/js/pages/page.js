export class Page {
    constructor(authService, router, params = {}) {
        this.params = params;
        this.authService = authService;
        this.router = router;
    }

    async beforeRender() {
    }

    getTemplate() {
    }

    async afterRender() {
    }
}
