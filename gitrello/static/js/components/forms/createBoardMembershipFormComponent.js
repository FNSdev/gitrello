import {boardMembershipRepository, } from "../../repositories/boardMembershipRepository.js";

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
      .form {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }
            
      .form__header {
        margin: 10px;
        text-align: center;
      }
      
      .form__search {
        padding: 6px 10px;
        box-sizing: border-box;
        border: 2px solid var(--primary-dark);
        outline: none;
        border-radius: 6px;
        margin-top: 10px;
      }
      
      .form__members-list {
        margin: 10px;
      }
      
      .form__members-list__item {
        border: 2px solid var(--secondary-dark);
        border-radius: 16px;
        font-size: 24px;
        padding: 15px;
        margin: 10px;
        text-align: center;
        cursor: pointer;
      }
    </style>
    <form class="form">
      <h1 class="form__header">Click on Member to add</h1>
      <input type="text" class="form__search" id="search" placeholder="Type to search">
      <ul class="form__members-list" id="members-list"></ul>     
      <errors-list-component id="form-errors" class="form__errors"></errors-list-component>
    </form>
`

export class CreateBoardMembershipFormComponent extends HTMLElement {
    constructor() {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        this._callback = null;
        this._boardId = null;
        this._organizationMemberships = null;
    }

    connectedCallback() {
        this._insertMembers(this._organizationMemberships);
        this.shadowRoot.getElementById('search').addEventListener('input', () => {
            this.onSearchInput();
        })
    }

    onSearchInput() {
        const search = this.shadowRoot.getElementById('search').value;
        this.shadowRoot.getElementById('members-list').innerHTML = '';

        const organizationMemberships = [];
        this._organizationMemberships.forEach(organizationMembership => {
            if (organizationMembership.user.firstName.toLowerCase().includes(search) ||
                organizationMembership.user.lastName.toLowerCase().includes(search)
            ) {
                organizationMemberships.push(organizationMembership);
            }
        });
        this._insertMembers(organizationMemberships);
    }

    async onAddMemberClick(event) {
        this.shadowRoot.getElementById('form-errors').clear();
        const organizationMembership = this._organizationMemberships.find(organizationMembership => {
            if (organizationMembership.id === event.target.getAttribute('id')) {
                return organizationMembership;
            }
        })

        try {
            const boardMembership = await boardMembershipRepository.create(
                this._boardId,
                organizationMembership.id,
            );
            boardMembership.organizationMembership = organizationMembership;

            this._organizationMemberships = this._organizationMemberships.filter(membership => {
                if (membership.id !== organizationMembership.id) {
                    return organizationMembership;
                }
            });

            this.onSearchInput();

            if (this._callback != null) {
                this._callback(boardMembership);
            }
        }
        catch (e) {
            this.shadowRoot.getElementById('form-errors').addError(e);
        }
    }

    set callback(callback) {
        this._callback = callback;
    }

    set boardId(id) {
        this._boardId = id;
    }

    set organizationMemberships(memberships) {
        this._organizationMemberships = memberships;
    }

    _insertMembers(organizationMemberships) {
        const membersList = this.shadowRoot.getElementById('members-list');

        organizationMemberships.forEach(organizationMembership => {
            const member = document.createElement('li');
            member.setAttribute('title', 'Click to add');
            member.setAttribute('id', organizationMembership.id);
            member.innerHTML = `${organizationMembership.user.firstName} ${organizationMembership.user.lastName}`;
            member.classList.add('form__members-list__item');
            member.onclick = async (event) => {
                await this.onAddMemberClick(event);
            }

            membersList.appendChild(member);
        })
    }
}

window.customElements.define('create-board-membership-form-component', CreateBoardMembershipFormComponent);
