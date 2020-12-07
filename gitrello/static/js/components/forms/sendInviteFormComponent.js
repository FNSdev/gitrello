import {organizationInviteRepository, } from "../../repositories/organizationInviteRepository.js";

const template = document.createElement('template')
template.innerHTML = `
    <style>
      .form {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }
            
      .form__header {
        margin: 10px;
      }
      
      .form__email-input {
        margin-top: 10px;
      }
      
      .form__message-input {
        margin-top: 10px;
      }
      
      .form__button {
        margin: 10px;
      }      
    </style>
    <form class="form">
      <h1 class="form__header">Send invite</h1>
      <input-component required minlength="5" maxlength="100" id="form-email" type="email" class="form__input" placeholder="Email"></input-component>
      <input-component required maxlength="100" id="form-message" type="text" class="form__input" placeholder="Message"></input-component>
      <errors-list-component id="form-errors" class="form__errors"></errors-list-component>
      <button-component type="success" id="send-invite-button" class="form__button"/>
        Send
      </button-component>
    </form>
`

export class SendInviteFormComponent extends HTMLElement {
    constructor() {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        this._callback = null;
        this._organizationId = null;
    }

    connectedCallback() {
        this.shadowRoot.querySelector('#send-invite-button').addEventListener(
            'click', () => this.onSendInvite()
        );
    }

    async onSendInvite() {
        const errorsList = this.shadowRoot.getElementById('form-errors');
        errorsList.clear();

        if (!this.shadowRoot.querySelector('#form-email').checkValidity() ||
            !this.shadowRoot.querySelector('#form-message').checkValidity()
        ) {
            errorsList.addError(errorsList.defaultErrorMessage);
            return;
        }

        try {
            const invite = await organizationInviteRepository.create(
                this.shadowRoot.querySelector('#form-email').value,
                this.shadowRoot.querySelector('#form-message').value,
                this._organizationId,
            )

            if (this._callback != null) {
                this._callback(invite);
            }
        }
        catch (e) {
            errorsList.addError(e.message);
        }
    }

    set callback(callback) {
        this._callback = callback;
    }

    set organizationId(id) {
        this._organizationId = id;
    }
}

window.customElements.define('send-invite-form-component', SendInviteFormComponent);
