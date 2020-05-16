import {organizationRepository, } from "../../repositories/organizationRepository.js";

const template = document.createElement('template')
template.innerHTML = `
    <style>
      ul,
      ul li {
        margin: 0;
        padding: 0;
        text-indent: 0;
        list-style-type: none;
      }
      .form {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }
            
      .form__header {
        margin: 10px;
        text-align: center;
      }
      
      .form__input {
        margin-top: 10px;
      }
      
      .form__button {
        margin: 10px;
      }      
    </style>
    <form class="form">
      <h1 class="form__header">New Organization</h1>
      <input-component required minlength="5" maxlength="100" id="form-organization-name" type="text" class="form__input" placeholder="Organization name">
      </input-component>
      <errors-list-component id="form-errors" class="form__errors"></errors-list-component>
      <button-component type="success" id="create-organization-button" class="form__button"/>
        Create
      </button-component>
    </form>
`

export class CreateOrganizationFormComponent extends HTMLElement {
    constructor() {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        this._callback = null;
    }

    connectedCallback() {
        this.shadowRoot.querySelector('#create-organization-button').addEventListener(
            'click', () => this.onCreateOrganization()
        );
    }

    async onCreateOrganization() {
        const errorsList = this.shadowRoot.getElementById('form-errors');
        errorsList.clear();

        if (!this.shadowRoot.querySelector('#form-organization-name').checkValidity()) {
            errorsList.addError(errorsList.defaultErrorMessage);
            return;
        }

        try {
            const organization = await organizationRepository.create(
                this.shadowRoot.querySelector('#form-organization-name').value,
            )

            if (this._callback != null) {
                this._callback(organization);
            }
        }
        catch (e) {
            errorsList.addError(e.message);
        }
    }

    set callback(callback) {
        this._callback = callback;
    }
}

window.customElements.define('create-organization-form-component', CreateOrganizationFormComponent);
