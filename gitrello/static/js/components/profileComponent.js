import {oauthStateRepository, } from "../repositories/oauthStateRepository.js";

const template = document.createElement('template')
template.innerHTML = `
    <style>
      .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 90vw;
      }
      
      .container__full-name {
        text-align: center;
        font-size: 32px;
      }
      
      .container__email {
        text-align: center;
        margin-top: 10px;
        font-size: 24px;
      }
      
      .container__username {
        text-align: center;
        margin-top: 10px;
        font-size: 24px;
      }
      
      .container__github-button {
        margin-top: 10px;
      }
      
      @media screen and (min-width: 992px) {
        .container {
          width: 20vw;
        }
      }
    </style>
    <div class="container">
      <div id="full-name" class="container__full-name"></div>
      <div id="email" class="container__email"></div>
      <div id="username" class="container__username"></div>
      <button-component id="github-button" class="container__github-button" width="200px">Connect to GitHub</button-component>
    </div>
`

export class ProfileComponent extends HTMLElement {
    GITHUB_OAUTH_URL = 'https://github.com/login/oauth/authorize';

    constructor(user) {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        this.user = user;
        this.stateHasChanged = null;
    }

    // TODO check if user is already connected to GitHub
    connectedCallback() {
        this.shadowRoot.getElementById('full-name').innerHTML = `${this.user.firstName} ${this.user.lastName}`;
        this.shadowRoot.getElementById('email').innerHTML = this.user.email;
        this.shadowRoot.getElementById('username').innerHTML = this.user.username;
        this.shadowRoot.getElementById('github-button').onclick = async () => await this.onGithubButtonClick();
    }

    async onGithubButtonClick() {
        let state = null;
        try {
            const oauthState = await oauthStateRepository.create(oauthStateRepository.GITHUB_PROVIDER);
            state = oauthState.state;
        }
        catch (e) {
            // TODO
            console.log(e);
            return
        }

        const params = {
            'client_id': window.GITHUB_CLIENT_ID,
            'redirect_uri': window.GITHUB_REDIRECT_URL,
            'state': state,
        }

        let paramsQuery = '?'
        for (let [key, value] of Object.entries(params)) {
            paramsQuery += `${key}=${encodeURIComponent(value.toString())}&`
        }

        location.href = `${this.GITHUB_OAUTH_URL}${paramsQuery}&scope=${window.GITHUB_DEFAULT_SCOPES}`;
    }
}

window.customElements.define('profile-component', ProfileComponent);
