import {Page, } from "./page.js";

export class HomePage extends Page {
    authTemplate = `
      <div class="auth-container">
        <div class="auth-container__tab">
          <ul class="auth-container__tab__list">
            <li class="auth-container__tab__list__item active" id="auth-container-tab-list-item-signup">
              <a class="auth-container__tab__list__item__link">Sign Up</a>
            </li>
            <li class="auth-container__tab__list__item" id="auth-container-tab-list-item-login">
              <a class="auth-container__tab__list__item__link">Log In</a>
            </li>
          </ul>
          <div class="auth-container__tab__content">
            <form class="auth-container__tab__content__signup-form" id="auth-container-tab-content-signup-form">
              <h1 class="auth-container__tab__content__signup-form__header">New Account</h1>
              <input required type="text" class="auth-container__tab__content__signup-form__input" placeholder="Your Login">
              <input required type="email" class="auth-container__tab__content__signup-form__input" placeholder="Your Email">
              <input required type="password" class="auth-container__tab__content__signup-form__input" placeholder="Your Password">  
              <button type="submit" id="signup-button" class="auth-container__tab__content__signup-form__button btn btn-success"/>
                Get Started
              </button>
            </form>
            <form class="auth-container__tab__content__login-form" id="auth-container-tab-content-login-form">
              <h1 class="auth-container__tab__content__login-form__header">Welcome Back!</h1>
              <input required type="text" class="auth-container__tab__content__login-form__input" placeholder="Your Login">
              <input required type="password" class="auth-container__tab__content__login-form__input" placeholder="Your Password">
              <button type="submit" id="login-button" class="auth-container__tab__content__login-form__button btn btn-success"/>
                Log In
              </button>
            </form>    
          </div>
        </div> 
      </div>
    `

    constructor(params) {
        super(params);
    }

    getTemplate() {
        return this.authTemplate;
    }

    onLoginSwitchClick() {
        document.getElementById("auth-container-tab-content-signup-form").style.display = "none";
        document.getElementById("auth-container-tab-content-login-form").style.display = "flex";
    }

    onSignUpSwitchClick() {
        document.getElementById("auth-container-tab-content-signup-form").style.display = "flex";
        document.getElementById("auth-container-tab-content-login-form").style.display = "none"
    }

    afterRender() {
        super.afterRender();

        document.getElementById('auth-container-tab-list-item-signup').onclick = this.onSignUpSwitchClick;
        document.getElementById('auth-container-tab-list-item-login').onclick = this.onLoginSwitchClick
        document.getElementById('signup-button').onclick = this.onSignUp;
        document.getElementById('login-button').onclick = this.onLogIn;
    }

    onSignUp(event) {
        event.preventDefault();
    }

    onLogIn(event) {
        event.preventDefault();
    }
}
