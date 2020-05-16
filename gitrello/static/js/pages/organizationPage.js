import {Page, } from "./page.js";

export class OrganizationPage extends Page {
    template = `
      <div class="organization-container">
        <div class="organization-container__content">
          <div id="boards-list" class="organization-container__content__boards-list"></div>
        </div>
      </div>
    `

    constructor(authService, router, params) {
        super(authService, router, params);

        this.organizationId = params['organizationId'];
    }

    getTemplate() {
        if (!this.authService.isAuthenticated()) {
            return this.notAuthenticatedTemplate;
        }
        return this.template;
    }

    async beforeRender() {
        await super.beforeRender();

        try {
            // TODO
        }
        catch (e) {
            // TODO handle PermissionDenied
            console.log(e);
        }
    }

    async afterRender() {
        await super.afterRender();

        if (!this.authService.isAuthenticated()) {
            return;
        }
    }
}
