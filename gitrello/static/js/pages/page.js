export class Page {
    notAuthenticatedTemplate = `
      <div class="not-authenticated-container">
        <div class="not-authenticated-container__content">
            <div class="not-authenticated-container__content__error">Error 401</div>
            <div class="not-authenticated-container__content__error-message">Not Authorized</div>
            <div class="not-authenticated-container__content__link-container">
              <a class="not-authenticated-container__content__link-container__link route" href="/">
                Go to Login page
              </a> 
            </div>       
        </div>
      </div>
    `

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
