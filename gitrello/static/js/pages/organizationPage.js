import {organizationRepository, } from "../repositories/organizationRepository.js";
import {HttpClientPermissionDeniedError, } from "../errors.js";
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
        this.hasAccess = true;
    }

    getTemplate() {
        if (!this.authService.isAuthenticated()) {
            return this.notAuthenticatedTemplate;
        }

        if (!this.hasAccess) {
            return this.accessDeniedTemplate;
        }

        return this.template;
    }

    async beforeRender() {
        await super.beforeRender();

        // TODO maybe its better to return 403 if member tries to get organization info
        try {
            this.organization = await organizationRepository.get(this.organizationId);
            const membership = this.organization.organizationMemberships.find(organizationMembership => {
                if (organizationMembership.user.id === this.authService.user.id) {
                    return organizationMembership;
                }
            })

            if (membership.role === 'MEMBER') {
                this.hasAccess = false;
            }
        }
        catch (e) {
            if (e instanceof HttpClientPermissionDeniedError) {
                this.hasAccess = false;
            }

            console.log(e);
        }
    }

    async afterRender() {
        await super.afterRender();

        if (!this.authService.isAuthenticated() || !this.hasAccess) {
            return;
        }
    }
}
