import {Page,} from "./page.js";
import {userRepository} from "../repositories/userRepository.js";

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
              <input required id="signup-form-username" type="text" class="auth-container__tab__content__signup-form__input" placeholder="Your Username">
              <input required id="signup-form-email" type="email" class="auth-container__tab__content__signup-form__input" placeholder="Your Email">
              <input required id="signup-form-first-name" type="text" class="auth-container__tab__content__signup-form__input" placeholder="Your First Name">
              <input required id="signup-form-last-name" type="text" class="auth-container__tab__content__signup-form__input" placeholder="Your Last Name">
              <input required id="signup-form-password" type="password" class="auth-container__tab__content__signup-form__input" placeholder="Your Password">  
              <div class="auth-container__tab__content__signup-form__errors">
                <ul id="signup-form-errors-list" class="auth-container__tab__content__signup-form__errors__list"></ul>          
              </div>
              <button type="submit" id="signup-button" class="auth-container__tab__content__signup-form__button btn btn-success"/>
                Get Started
              </button>
            </form>
            <form class="auth-container__tab__content__login-form" id="auth-container-tab-content-login-form">
              <h1 class="auth-container__tab__content__login-form__header">Welcome Back!</h1>
              <input required type="text" class="auth-container__tab__content__login-form__input" placeholder="Your Login">
              <input required type="password" class="auth-container__tab__content__login-form__input" placeholder="Your Password">
              <div class="auth-container__tab__content__login-form__errors">
                <ul id="login-form-errors-list" class="auth-container__tab__content__login-form__errors__list"></ul>          
              </div>
              <button type="submit" id="login-button" class="auth-container__tab__content__login-form__button btn btn-success"/>
                Log In
              </button>
            </form>    
          </div>
        </div> 
      </div>
    `

    constructor(authService, router, params) {
        super(authService, router, params);
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
        document.getElementById('signup-button').onclick = (event) => this.onSignUp(event);
        document.getElementById('login-button').onclick = (event) => this.onLogIn(event);
    }

    onSignUp(event) {
        event.preventDefault();

        const errorsList = document.getElementById('signup-form-errors-list');
        errorsList.innerHTML = '';

        userRepository.createUser(
            document.getElementById('signup-form-username').value,
            document.getElementById('signup-form-email').value,
            document.getElementById('signup-form-first-name').value,
            document.getElementById('signup-form-last-name').value,
            document.getElementById('signup-form-password').value,
        ).then((user) => {
            this.authService.setUser(user);
            this.router.navigate('/profile');
        }).catch((e) => {
            errorsList.innerHTML = `
              <li class="auth-container__tab__content__signup-form__errors__list__item">${e.message}</li>
            `;
        });
    }

    // TODO
    onLogIn(event) {
        event.preventDefault();
    }
}
