import {AuthService, } from "../../services/authService.js";
import {Router, } from "../../router.js";
import {userRepository, } from "../../repositories/userRepository.js";

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
      .signup-form {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }
            
      .signup-form__header {
        margin: 10px;
      }
      
      .signup-form__input {
        margin-top: 10px;
      }
      
      .signup-form__button {
        margin: 10px;
      }
    </style>
    <form class="signup-form">
      <h1 class="signup-form__header">New Account</h1>
      <input-component required minlength="5" maxlength="150" id="signup-form-username" type="text" class="signup-form__input" placeholder="Your Username"></input-component>
      <input-component required id="signup-form-email" type="email" class="signup-form__input" placeholder="Your Email"></input-component>
      <input-component required maxlength="30" id="signup-form-first-name" type="text" class="signup-form__input" placeholder="Your First Name"></input-component>
      <input-component required maxlength="100" id="signup-form-last-name" type="text" class="signup-form__input" placeholder="Your Last Name"></input-component>
      <input-component required maxlength="128" id="signup-form-password" type="password" class="signup-form__input" placeholder="Your Password"></input-component>
      <errors-list-component id="signup-form-errors" class="signup-form__errors"></errors-list-component>
      <button-component type="success" id="signup-button" class="signup-form__button btn btn-success"/>
        Get Started
      </button-component>
    </form>
`

export class SignUpFormComponent extends HTMLElement {
    constructor() {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));
    }

    connectedCallback() {
        this.shadowRoot.querySelector('#signup-button').addEventListener(
            'click', () => this.onSignUp()
        );
    }

    async onSignUp() {
        const errorsList = this.shadowRoot.getElementById('signup-form-errors');
        errorsList.clear();

        if (!this.shadowRoot.querySelector('#signup-form-username').checkValidity() ||
            !this.shadowRoot.querySelector('#signup-form-email').checkValidity() ||
            !this.shadowRoot.querySelector('#signup-form-first-name').checkValidity() ||
            !this.shadowRoot.querySelector('#signup-form-last-name').checkValidity() ||
            !this.shadowRoot.querySelector('#signup-form-password').checkValidity()
        ) {
            errorsList.addError(errorsList.defaultErrorMessage);
            return;
        }

        try {
            const user = await userRepository.create(
                this.shadowRoot.querySelector('#signup-form-username').value,
                this.shadowRoot.querySelector('#signup-form-email').value,
                this.shadowRoot.querySelector('#signup-form-first-name').value,
                this.shadowRoot.querySelector('#signup-form-last-name').value,
                this.shadowRoot.querySelector('#signup-form-password').value,
            );

            const authService = await AuthService.build();
            const router = await Router.build();
            authService.user = user;
            await router.navigate('/profile');
        }
        catch (e) {
            errorsList.addError(e.message);
        }
    }
}

window.customElements.define('sign-up-form-component', SignUpFormComponent);
