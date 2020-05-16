import {CreateBoardMembershipFormComponent, } from "./forms/createBoardMembershipFormComponent.js";

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
      }
      
      .container__board-memberships {
        margin-top: 10px;
        border: 2px solid var(--primary-dark);
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        justify-content: center;
      }
      
      .container__board-memberships__list {
        overflow-y: auto;
        height: 175px;
        width: 275px;
        scrollbar-color: var(--primary-dark) var(--primary-light);
      }
      
      .container__board-memberships__list__item {
        margin: 10px;
        text-align: center;
        cursor: pointer;
      }
      
      .container__add-member-button {
        margin-top: 10px;
      }
      
      .add-member-modal {
        display: none;
        position: fixed;
        z-index: 1;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgb(0, 0, 0);
        background-color: rgba(0, 0, 0, 0.7);
      }
      
      .add-member-modal__content {
        background-color: #fefefe;
        margin: 100px auto;
        border: 3px solid var(--primary-dark);
        border-radius: 10px;
        width: 70%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }
      
      @media screen and (min-width: 992px) {
        .add-member-modal__content {
          width: 30%;
        }
      }
    </style>
    <div class="container">
      <a id="name" class="container__name route"></a>
      <div class="container__board-memberships">
        <ul class="container__board-memberships__list" id="board-memberships-list"></ul>
      </div>
      <button-component id="add-member-button" class="container__add-member-button" type="info">
        Add
      </button-component>
    </div>
    
    <div id="add-member-modal" class="add-member-modal">
      <div class="add-member-modal__content" id="add-member-modal-content"></div>
    </div>
`

export class BoardComponent extends HTMLElement {
    constructor(board) {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        this.board = board;
    }

    connectedCallback() {
        this.shadowRoot.getElementById('name').innerHTML = this.board.name;
        this.shadowRoot.getElementById('name').setAttribute(
            'href',
            `/boards/${this.board.id}`,
        );
        this.board.boardMemberships.forEach(boardMembership => {
            this.shadowRoot.getElementById('board-memberships-list').innerHTML += `
              <li class="container__board-memberships__list__item" title="Click to remove">
                ${boardMembership.organizationMembership.user.firstName} ${boardMembership.organizationMembership.user.lastName}
              </li>
            `
        });

        this.shadowRoot.getElementById('add-member-button').addEventListener(
            'click', () => this.onAddMemberButtonClick()
        );

        const addMemberForm = new CreateBoardMembershipFormComponent();
        const organizationMemberships = [];
        this.board.organization.organizationMemberships.forEach(organizationMembership => {
            const boardMembership = this.board.boardMemberships.find(boardMembership => {
                if (boardMembership.organizationMembership.id === organizationMembership.id) {
                    return boardMembership;
                }
            });

            if (boardMembership == null) {
                organizationMemberships.push(organizationMembership);
            }
        });
        addMemberForm.callback = (member) => {
            this.afterMemberAdded(member);
        };
        addMemberForm.boardId = this.board.id;
        addMemberForm.organizationMemberships = organizationMemberships;
        this.shadowRoot.getElementById('add-member-modal-content').appendChild(addMemberForm);
    }

    async onAddMemberButtonClick() {
        this.shadowRoot.getElementById('add-member-modal').style.display = "block";
        const modal = this.shadowRoot.getElementById('add-member-modal');
        modal.onclick = (event) => {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        };
    }

    afterMemberAdded(member) {
        this.shadowRoot.getElementById('board-memberships-list').innerHTML += `
          <li class="container__board-memberships__list__item" title="Click to remove">
            ${member.organizationMembership.user.firstName} ${member.organizationMembership.user.lastName}
          </li>
        `

        member.board = this.board;
        this.board.boardMemberships.push(member);
    }
}

window.customElements.define('board-component', BoardComponent);
