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

      .container {
        border: 3px solid var(--primary-dark);
        border-radius: 10px;
        box-shadow: var(--default-shadow);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 300px;
        padding: 10px;
      }
      
      .container__name {
        font-size: 24px;
        text-decoration: none;
        text-align: center;
        word-break: break-word;
      }
      
      .container__role {
        font-size: 18px;
        margin-top: 5px;
      }
  
      .container__boards {
        margin-top: 10px;
        border: 2px solid var(--primary-dark);
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        justify-content: center;
      }
      
      .container__boards__list {
        overflow-y: auto;
        height: 175px;
        width: 275px;
        scrollbar-color: var(--primary-dark) var(--primary-light);
      }
      
      .container__boards__list__item {
        margin: 10px;
        text-align: center;
      }
      
      .container__boards__list__item__link {
        text-decoration: none;
      }
    </style>
    <div class="container">
      <a id="name" class="container__name route"></a>
      <div id="role" class="container__role"></div>
      <div class="container__boards">
        <ul class="container__boards__list" id="boards-list"></ul>
      </div>
    </div>
`

export class OrganizationMembershipComponent extends HTMLElement {
    constructor(organizationMembership) {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        this.organizationMembership = organizationMembership;
    }

    connectedCallback() {
        this.shadowRoot.getElementById('name').innerHTML = this.organizationMembership.organization.name;
        this.shadowRoot.getElementById('name').setAttribute(
            'href',
            `/organizations/${this.organizationMembership.organization.id}`,
        );
        this.shadowRoot.getElementById('role').innerHTML = `Role: ${this.organizationMembership.role}`;
        this.organizationMembership.boardMemberships.forEach(boardMembership => {
            this.shadowRoot.getElementById('boards-list').innerHTML += `
              <li class="container__boards__list__item">
                <a class="container__boards__list__item__link route" href="/boards/${boardMembership.board.id}">
                  ${boardMembership.board.name}
                </a>
              </li>
            `
        });
    }
}

window.customElements.define('organization-membership-component', OrganizationMembershipComponent);
