import {authService, } from "../../services/authService.js";
import {router, } from "../../router.js";
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
      .login-form {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }
            
      .login-form__header {
        margin: 10px;
      }
      
      .login-form__input {
        margin-top: 10px;
      }
      
      .login-form__button {
        margin: 10px;
      }
      
      .login-form__errors {
        display: flex;
        flex-direction: column;
        justify-content: center;
      }
      
      .login-form__errors__list {
        overflow-y: auto;
        max-height: 300px;
      }
      
      .login-form__errors__list__item {
        margin: 10px;
        padding: 10px;
        border: 3px solid var(--red);
        border-radius: 15px;
        font-size: 16px;
      }
    </style>
    <form class="login-form">
      <h1 class="login-form__header">Welcome Back!</h1>
      <input-component required minlength="5" maxlength="150" id="login-form-username" type="text" class="login-form__input" placeholder="Your Username"></input-component>
      <input-component required maxlength="128" id="login-form-password" type="password" class="login-form__input" placeholder="Your Password"></input-component>
      <div class="login-form__errors">
        <ul id="login-form-errors-list" class="login-form__errors__list"></ul>          
      </div>
      <button-component type="success" id="login-button" class="login-form__button btn btn-success"/>
        Log In
      </button-component>
    </form>
`

export class LogInFormComponent extends HTMLElement {
    constructor() {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));
    }

    connectedCallback() {
        this.shadowRoot.querySelector('#login-button').addEventListener(
            'click', () => this.onLogin()
        );
    }

    onLogin(event) {
        const errorsList = this.shadowRoot.querySelector('#login-form-errors-list');
        errorsList.innerHTML = '';

        if (!this.shadowRoot.querySelector('#login-form-username').checkValidity() ||
            !this.shadowRoot.querySelector('#login-form-password').checkValidity()
        ) {
            errorsList.innerHTML = `
              <li class="login-form__errors__list__item">Please, fill out required fields with correct data</li>
            `;
            return
        }

        // TODO
    }
}

window.customElements.define('log-in-form-component', LogInFormComponent);
