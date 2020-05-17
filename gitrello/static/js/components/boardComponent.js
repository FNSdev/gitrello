import {boardMembershipRepository, } from "../repositories/boardMembershipRepository.js";
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
      
      .add-member-modal, .remove-member-modal {
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
      
      .add-member-modal__content, .remove-member-modal__content {
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
      
      .remove-member-modal__content__header {
        margin: 10px;
        text-align: center;
      }
      
      .remove-member-modal__content__wrapper {
        display: flex;
        align-items: center;
        padding: 10px;
      }
      
      .remove-member-modal__content__wrapper__yes-button, .remove-member-modal__content__wrapper__cancel-button {
        margin: 10px;
      }
      
      @media screen and (min-width: 992px) {
        .add-member-modal__content, .remove-member-modal__content {
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
    
    <div id="remove-member-modal" class="remove-member-modal">
      <div class="remove-member-modal__content" id="remove-member-modal-content">
        <h1 class="remove-member-modal__content__header">Are you sure?</h1>
        <errors-list-component id="remove-member-errors" class="remove-member-modal__content__errors"></errors-list-component>
        <div class="remove-member-modal__content__wrapper">
          <button-component type="success" class="remove-member-modal__content__wrapper__yes-button" id="remove-member-button">
            Yes
          </button-component>
          <button-component type="danger" class="remove-member-modal__content__wrapper__cancel-button" id="cancel-remove-member-button">
            Cancel
          </button-component>
        </div>
      </div>
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
        this._insertMembers(this.board.boardMemberships);

        this.shadowRoot.getElementById('add-member-button').addEventListener(
            'click', () => this.onAddMemberButtonClick()
        );
        this.shadowRoot.getElementById('cancel-remove-member-button').addEventListener(
            'click', () => {
                this.shadowRoot.getElementById('remove-member-modal').style.display = "none";
            }
        )

        const addMemberForm = new CreateBoardMembershipFormComponent();
        addMemberForm.setAttribute('id', 'add-member-form');
        addMemberForm.callback = (member) => {
            this.afterMemberAdded(member);
        };
        addMemberForm.boardId = this.board.id;
        addMemberForm.organizationMemberships = this._getMembershipsDiff();
        this.shadowRoot.getElementById('add-member-modal-content').appendChild(addMemberForm);
    }

    onAddMemberButtonClick() {
        this.shadowRoot.getElementById('add-member-modal').style.display = "block";
        const modal = this.shadowRoot.getElementById('add-member-modal');
        modal.onclick = (event) => {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        };
    }

    onRemoveMemberClick(event) {
        this.shadowRoot.getElementById('remove-member-errors').clear();
        const boardMembershipId = event.target.getAttribute('id');
        const target = event.composedPath()[0];

        this.shadowRoot.getElementById('remove-member-modal').style.display = "block";
        const modal = this.shadowRoot.getElementById('remove-member-modal');
        modal.onclick = (event) => {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        };
        this.shadowRoot.getElementById('remove-member-button').onclick = async () => {
            try {
                await boardMembershipRepository.delete(boardMembershipId);
                this.board.boardMemberships = this.board.boardMemberships.filter(boardMembership => {
                    if (boardMembership.id !== boardMembershipId) {
                        return boardMembership;
                    }
                });
                target.remove();
                modal.style.display = "none";
                this.shadowRoot.getElementById('add-member-form').organizationMemberships = this._getMembershipsDiff();
            }
            catch (e) {
                this.shadowRoot.getElementById('remove-member-errors').addError(e.message);
            }
        }
    }

    afterMemberAdded(member) {
        member.board = this.board;
        this.board.boardMemberships.push(member);
        this._insertMembers([member, ]);
    }

    _insertMembers(boardMemberships) {
        const membersList = this.shadowRoot.getElementById('board-memberships-list');

        boardMemberships.forEach(boardMembership => {
            const member = document.createElement('li');
            member.setAttribute('title', 'Click to remove');
            member.setAttribute('id', boardMembership.id);
            member.innerHTML = `${boardMembership.organizationMembership.user.firstName} ${boardMembership.organizationMembership.user.lastName}`;
            member.classList.add('container__board-memberships__list__item');
            member.onclick = async (event) => {
                await this.onRemoveMemberClick(event);
            }

            membersList.appendChild(member);
        })
    }

    _getMembershipsDiff() {
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
        return organizationMemberships;
    }
}

window.customElements.define('board-component', BoardComponent);
