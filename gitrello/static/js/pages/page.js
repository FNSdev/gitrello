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

    accessDeniedTemplate = `
      <div class="access-denied-container">
        <div class="access-denied-container__content">
          <div class="access-denied-container__content__error">Error 403</div>
          <div class="access-denied-container__content__error-message">Access Denied</div>
          <div class="access-denied-container__content__link-container">
            <a class="access-denied-container__content__link-container__link route" href="/organizations">
              Return to Organizations Page
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
