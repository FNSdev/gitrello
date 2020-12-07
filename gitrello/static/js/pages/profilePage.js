import {organizationInviteRepository, } from "../repositories/organizationInviteRepository.js";
import {OrganizationInviteComponent, } from "../components/organizationInviteComponent.js";
import {Page, } from "./page.js";
import {ProfileComponent, } from "../components/profileComponent.js";

export class ProfilePage extends Page {
    template = `
      <div class="profile-container">
        <div id="profile-container-content" class="profile-container__content">
          <div id="invites-list" class="profile-container__content__invites-list"></div>
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

        try {
            this.organizationInvites = await organizationInviteRepository.getAll();
            this._insertInvites(this.organizationInvites);
        }
        catch (e) {
            console.log(e);
        }

        const profileComponent = new ProfileComponent(this.authService.user);
        document.getElementById('profile-container-content').prepend(profileComponent);
    }

    _insertInvites(organizationInvites) {
        organizationInvites.forEach(organizationInvite => {
            const organizationInviteComponent = new OrganizationInviteComponent(organizationInvite);
            organizationInviteComponent.stateHasChanged = (organizationInvite) => {
                this._onStateChanged(organizationInvite);
            }
            document.getElementById('invites-list').appendChild(organizationInviteComponent);
        })
    }

    _onStateChanged(organizationInvite) {
        document.getElementById('invites-list').innerHTML = '';
        this.organizationInvites = this.organizationInvites.filter(invite => {
            if (invite.id !== organizationInvite.id) {
                return invite;
            }
        });
        this._insertInvites(this.organizationInvites);
    }
}
