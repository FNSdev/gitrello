import {Page, } from "./page.js";

export class HomePage extends Page {
    authTemplate = `
      <div class="auth-container">
        <div class="auth-container__tab">
          <ul class="auth-container__tab__list">
            <li class="auth-container__tab__list__item" id="auth-container-tab-list-item-signup">
              <a class="auth-container__tab__list__item__link">Sign Up</a>
            </li>
            <li class="auth-container__tab__list__item" id="auth-container-tab-list-item-login">
              <a class="auth-container__tab__list__item__link">Log In</a>
            </li>
          </ul>
          <div class="auth-container__tab__content">
            <sign-up-form-component id="sign-up-form" class="auth-container__tab__content__sign-up-form"></sign-up-form-component>
            <log-in-form-component id="log-in-form" class="auth-container__tab__content__log-in-form"></log-in-form-component>  
          </div>
        </div> 
      </div>
    `

    welcomeTemplate = `
      <div class="welcome-container">
        <div class="welcome-container__content">
            <div class="welcome-container__content__text" id="welcome-container-text"></div>
            <button-component type="danger" class="welcome-container__content__log-out-button" id="log-out-button">
              Log Out
            </button-component>          
        </div>
      </div>
    `

    constructor(authService, router, params) {
        super(authService, router, params);
    }

    getTemplate() {
        if (this.authService.isAuthenticated()) {
            return this.welcomeTemplate;
        }
        return this.authTemplate;
    }

    onLoginSwitchClick() {
        document.getElementById("sign-up-form").style.display = "none";
        document.getElementById("log-in-form").style.display = "flex";
    }

    onSignUpSwitchClick() {
        document.getElementById("sign-up-form").style.display = "flex";
        document.getElementById("log-in-form").style.display = "none";
    }

    async afterRender() {
        await super.afterRender();
        if (this.authService.isAuthenticated()) {
            document.getElementById('welcome-container-text').innerHTML = `
              Welcome, ${this.authService.user.username}!
            `
            document.getElementById('log-out-button').onclick = () => this.onLogOutClick();
            return;
        }

        document.getElementById('auth-container-tab-list-item-signup').onclick = this.onSignUpSwitchClick;
        document.getElementById('auth-container-tab-list-item-login').onclick = this.onLoginSwitchClick;
    }

    async onLogOutClick() {
        console.log('LOG OUT');
        this.authService.logOut();
        await this.router.reload();
    }
}
