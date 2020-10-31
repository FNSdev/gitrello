import {githubProfileRepository, } from "../repositories/githubProfileRepository.js";
import {oauthStateRepository, } from "../repositories/oauthStateRepository.js";

const template = document.createElement('template')
template.innerHTML = `
    <style>
      .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        box-shadow: var(--default-shadow);
        border: 2px solid var(--primary-dark);
        border-radius: 16px;
        width: 350px;
        padding: 10px;
      }
      
      .container__connect {
        display: none;
      }
      
      .container__disconnect {
        display: none;
        flex-direction: column;
        align-items: center;
      }
      
      .container__disconnect__user-login {
        text-align: center;
        font-size: 18px;
      }
      
      .container__disconnect__button {
        margin-top: 10px;
      }
      
    </style>
    <div class="container" id="container">
      <div id="connect" class="container__connect">
        <button-component id="connect-button" class="container__connect__button" width="200px" type="success">Connect to GitHub</button-component>
      </div>
      <div id="disconnect" class="container__disconnect">
        <div id="github-login" class="container__disconnect__user-login"></div>
        <button-component id="disconnect-button" class="container__disconnect__button" width="200px" type="danger">Disconnect from GitHub</button-component>
      </div>
      <errors-list-component id="errors-list" class="container__errors-list"></errors-list-component>
    </div>
`

export class GithubConnectionComponent extends HTMLElement {
    GITHUB_OAUTH_URL = 'https://github.com/login/oauth/authorize';

    constructor() {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));
    }

    async connectedCallback() {
        const errorsList = this.shadowRoot.getElementById('errors-list');

        try {
            const githubProfile = await githubProfileRepository.get();
            if (githubProfile == null) {
                this.shadowRoot.getElementById('connect').style.display = "flex";
            }
            else {
                this.shadowRoot.getElementById('github-login').innerHTML = `Connected to <strong>${githubProfile.githubLogin}</strong> GitHub account`;
                this.shadowRoot.getElementById('disconnect').style.display = "flex";
            }

            this.shadowRoot.getElementById('connect-button').onclick = async () => this.onConnectButtonClick();
            this.shadowRoot.getElementById('disconnect-button').onclick = async () => this.onDisconnectButtonClick();
        }
        catch (e) {
            errorsList.addError(e);
        }
    }

    async onConnectButtonClick() {
        const errorsList = this.shadowRoot.getElementById('errors-list');
        errorsList.clear();

        let state = null;
        try {
            const oauthState = await oauthStateRepository.create(oauthStateRepository.GITHUB_PROVIDER);
            state = oauthState.state;
        }
        catch (e) {
            errorsList.addError(e);
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

    async onDisconnectButtonClick() {
        const errorsList = this.shadowRoot.getElementById('errors-list');
        errorsList.clear();

        try {
            await githubProfileRepository.delete();
            this.shadowRoot.getElementById('connect').style.display = "flex";
            this.shadowRoot.getElementById('disconnect').style.display = "none";
        }
        catch (e) {
            errorsList.addError(e);
        }
    }
}

window.customElements.define('github-connection-component', GithubConnectionComponent);
