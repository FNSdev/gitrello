import {organizationMembershipRepository, } from "../repositories/organizationMembershipRepository.js";
import {OrganizationMembership, } from "../models/organizationMembership.js";
import {OrganizationMembershipComponent, } from "../components/organizationMembershipComponent.js";
import {Page, } from "./page.js";

export class OrganizationsPage extends Page {
    template = `
      <div class="organizations-container">
        <div class="organizations-container__content">
          <create-organization-form-component id="create-organization-form"></create-organization-form-component>
          <div id="organizations-list" class="organizations-container__content__organizations-list"></div>
        </div>
      </div>
    `

    constructor(authService, router, params) {
        super(authService, router, params);
    }

    getTemplate() {
        if (!this.authService.isAuthenticated()) {
            return this.notAuthenticatedTemplate;
        }
        return this.template;
    }

    async afterRender() {
        await super.afterRender();

        if (!this.authService.isAuthenticated()) {
            return;
        }

        document.getElementById('create-organization-form').callback = (organization) => {
            this.afterOrganizationCreated(organization);
        };

        try {
            const organizationMemberships = await organizationMembershipRepository.getAll();
            const organizationsList = document.getElementById('organizations-list');
            organizationMemberships.forEach(organizationMembership => {
                const element = new OrganizationMembershipComponent(organizationMembership);
                organizationsList.appendChild(element);
            });
        }
        catch (e) {
            console.log(e);
        }
    }

    afterOrganizationCreated(organization) {
        const organizationMembership = new OrganizationMembership({
            role: 'OWNER',
            organization: organization,
            boardMemberships: [],
        });

        const organizationsList = document.getElementById('organizations-list');
        const element = new OrganizationMembershipComponent(organizationMembership);
        organizationsList.appendChild(element);
    }
}
