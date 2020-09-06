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
      
      .container__github-connection {
        margin-top: 10px;
      }
      
      @media screen and (min-width: 992px) {
        .container {
          width: 20vw;
        }
      }
    </style>
    <div id="container" class="container">
      <div id="full-name" class="container__full-name"></div>
      <div id="email" class="container__email"></div>
      <div id="username" class="container__username"></div>
      <github-connection-component class="container__github-connection"></github-connection-component>
    </div>
`

export class ProfileComponent extends HTMLElement {
    constructor(user) {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        this.user = user;
        this.stateHasChanged = null;
    }

    async connectedCallback() {
        this.shadowRoot.getElementById('full-name').innerHTML = `${this.user.firstName} ${this.user.lastName}`;
        this.shadowRoot.getElementById('email').innerHTML = this.user.email;
        this.shadowRoot.getElementById('username').innerHTML = this.user.username;

    }
}

window.customElements.define('profile-component', ProfileComponent);
