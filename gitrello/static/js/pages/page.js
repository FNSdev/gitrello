export class Page {
    constructor(authService, router, params = {}) {
        this.params = params;
        this.authService = authService;
        this.router = router;
    }

    beforeRender() {
    }

    getTemplate() {
    }

    afterRender() {
    }
}
