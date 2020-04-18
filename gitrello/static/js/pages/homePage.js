import {Page, } from "./page.js";

export class HomePage extends Page {
    signUpTemplate = `
      <div class="signup-container">
        <div class="tab">
          <ul class="tab-group">
            <li class="tab active" id="signup-switch"><a class="tab-link">Sign Up</a></li>
            <li class="tab" id="login-switch"><a class="tab-link">Log In</a></li>
          </ul>
          <div class="tab-content">
            <form class="signup" id="signup">
              <h1>Create New Account</h1>
              <input type="text" class="input-box" placeholder="Your Login">
              <input type="email" class="input-box" placeholder="Your Email">
              <input type="password" class="input-box" placeholder="Your Password">  
              <button type="submit" class="signup-btn"/>Get Started</button>
            </form>
            <form class="login" id="login">
              <h1>Welcome Back!</h1>
              <input type="text" class="input-box" placeholder="Your Login">
              <input type="password" class="input-box" placeholder="Your Password">
              <button type="submit" class="login-btn"/>Log In</button>
            </form>    
          </div>
        </div> 
      </div>
    `

    constructor(params) {
        super(params);
    }

    getTemplate() {
        return this.signUpTemplate;
    }

    onLoginSwitchClick() {
        document.getElementById("signup").style.display = "none";
        document.getElementById("login").style.display = "flex";
    }

    onSignUpSwitchClick() {
        document.getElementById("signup").style.display = "flex";
        document.getElementById("login").style.display = "none"
    }

    afterRender() {
        super.afterRender();

        document.getElementById('signup-switch').onclick = this.onSignUpSwitchClick;
        document.getElementById('login-switch').onclick = this.onLoginSwitchClick;
    }
}