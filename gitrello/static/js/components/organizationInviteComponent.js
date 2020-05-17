import {organizationInviteRepository, } from "../repositories/organizationInviteRepository.js";

const template = document.createElement('template')
template.innerHTML = `
    <style>
      .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border: 3px solid var(--primary-dark);
        border-radius: 10px;
        box-shadow: var(--default-shadow);
        width: 400px;
      }
      
      .container__organization-name {
        margin-top: 10px;
        text-align: center;
        font-size: 32px;
      }
      
      .container__added-at {
        text-align: center;
        margin-top: 10px;
        font-size: 12px;
      }
      
      .container__line {
        width: 350px;
      }
      
      .container__message {
        text-align: center;
        margin-top: 10px;
        font-size: 24px;
      }
      
      .container__actions-wrapper {
        margin-top: 10px;
        display: flex;
        align-items: center; 
      }
      
      .container__actions-wrapper__button {
        margin: 10px;
      }
    </style>
    <div class="container">
      <div id="organization-name" class="container__organization-name"></div>
      <div id="added-at" class="container__added-at"></div>
      <hr class="container__line">
      <div id="message" class="container__message"></div>
      <errors-list-component id="errors-list" class="container__errors-list"></errors-list-component>
      <div class="container__actions-wrapper">
        <button-component id="accept-button" type="success" class="container__actions-wrapper__button">Accept</button-component>
        <button-component id="decline-button" type="danger" class="container__actions-wrapper__button">Decline</button-component>  
      </div>
    </div>
`

export class OrganizationInviteComponent extends HTMLElement {
    constructor(organizationInvite) {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        this.organizationInvite = organizationInvite;
        this.stateHasChanged = null;
    }

    connectedCallback() {
        this.shadowRoot.getElementById('organization-name').innerHTML = this.organizationInvite.organization.name;
        this.shadowRoot.getElementById('added-at').innerHTML = new Date(this.organizationInvite.addedAt).toUTCString();
        this.shadowRoot.getElementById('message').innerHTML = this.organizationInvite.message;

        this.shadowRoot.getElementById('accept-button').addEventListener('click', async () => {
            await this.onAcceptButtonClick();
        })
        this.shadowRoot.getElementById('decline-button').addEventListener('click', async () => {
            await this.onDeclineButtonClick();
        })
    }

    async onAcceptButtonClick() {
        await this._updateStatus(true);
    }

    async onDeclineButtonClick() {
        await this._updateStatus(false);
    }

    async _updateStatus(accept) {
        try {
            this.shadowRoot.getElementById('errors-list').clear();
            const organizationInvite = await organizationInviteRepository.updateStatus(
                this.organizationInvite.id,
                accept,
            );

            if (this.stateHasChanged != null) {
                this.stateHasChanged(organizationInvite);
            }
        }
        catch (e) {
            this.shadowRoot.getElementById('errors-list').addError(e.message);
        }
    }
}

window.customElements.define('organization-invite-component', OrganizationInviteComponent);
