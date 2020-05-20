import {organizationMembershipRepository, } from "../repositories/organizationMembershipRepository.js";
import {SendInviteFormComponent, } from "./forms/sendInviteFormComponent.js";

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
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 300px;
      }
      
      .container__name {
        font-size: 24px;
      }
      
      .container__organization-memberships {
        margin-top: 10px;
        border: 2px solid var(--primary-dark);
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        justify-content: center;
      }
      
      .container__organization-memberships__list {
        overflow-y: auto;
        height: 375px;
        width: 275px;
        scrollbar-color: var(--primary-dark) var(--primary-light);
      }
      
      .container__organization-memberships__list__item {
        margin: 10px;
        text-align: center;
        cursor: pointer;
      }
      
      .container__organization-memberships__list__item--owner {
        border: 2px solid var(--secondary-dark);
        border-radius: 10px;
      }
      
      .container__send-invite-button {
        margin-top: 10px;
      }
      
      .send-invite-modal, .remove-member-modal {
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
      
      .send-invite-modal__content, .remove-member-modal__content {
        background-color: #fefefe;
        margin: 100px auto;
        border: 3px solid var(--primary-dark);
        border-radius: 10px;
        width: 90%;
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
        .send-invite-modal__content, .remove-member-modal__content {
          width: 30%;
        }
      }
    </style>
    <div class="container">
      <h1 id="name" class="container__name"></h1>
      <div class="container__organization-memberships">
        <ul class="container__organization-memberships__list" id="organization-memberships-list"></ul>
      </div>
      <button-component id="send-invite-button" class="container__send-invite-button" type="info">
        Send Invite
      </button-component>
    </div>
    
    <div id="send-invite-modal" class="send-invite-modal">
      <div class="send-invite-modal__content" id="send-invite-modal-content"></div>
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

export class OrganizationComponent extends HTMLElement {
    constructor(organization) {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        this.organization = organization;
        this.stateHasChanged = null;
    }

    connectedCallback() {
        this.shadowRoot.getElementById('name').innerHTML = this.organization.name;
        this._insertMembers(this.organization.organizationMemberships);

        this.shadowRoot.getElementById('cancel-remove-member-button').addEventListener(
            'click', () => {
                this.shadowRoot.getElementById('remove-member-modal').style.display = "none";
            }
        );

        const sendInviteFormComponent = new SendInviteFormComponent();
        sendInviteFormComponent.organizationId = this.organization.id;
        sendInviteFormComponent.callback = () => {
            this.shadowRoot.getElementById('send-invite-modal').style.display = "none";
        };
        this.shadowRoot.getElementById('send-invite-modal-content').appendChild(sendInviteFormComponent);

        this.shadowRoot.getElementById('send-invite-button').addEventListener(
            'click', () => this.onSendInviteClick()
        );
    }

    onSendInviteClick() {
        this.shadowRoot.getElementById('send-invite-modal').style.display = "block";
        const modal = this.shadowRoot.getElementById('send-invite-modal');
        modal.onclick = (event) => {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        };
    }

    onRemoveMemberClick(event) {
        this.shadowRoot.getElementById('remove-member-errors').clear();
        const organizationMembershipId = event.target.getAttribute('id');
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
                await organizationMembershipRepository.delete(organizationMembershipId);
                this.organization.organizationMemberships = this.organization.organizationMemberships.filter(organizationMembership => {
                    if (organizationMembership.id !== organizationMembershipId) {
                        return organizationMembership;
                    }
                });

                this.organization.boards.forEach(board => {
                    board.boardMemberships = board.boardMemberships.filter(boardMembership => {
                        if (boardMembership.organizationMembership.id !== organizationMembershipId) {
                            return organizationMembershipId;
                        }
                    })
                })

                target.remove();
                modal.style.display = "none";

                if (this.stateHasChanged != null) {
                    this.stateHasChanged();
                }
            }
            catch (e) {
                this.shadowRoot.getElementById('remove-member-errors').addError(e.message);
            }
        }
    }

    _insertMembers(organizationMemberships) {
        const membersList = this.shadowRoot.getElementById('organization-memberships-list');

        organizationMemberships.forEach(organizationMembership => {
            const member = document.createElement('li');
            member.setAttribute('title', 'Click to remove');
            member.setAttribute('id', organizationMembership.id);
            member.innerHTML = `${organizationMembership.user.firstName} ${organizationMembership.user.lastName}`;
            member.classList.add('container__organization-memberships__list__item');
            if (organizationMembership.role === 'OWNER') {
                member.classList.add('container__organization-memberships__list__item--owner');
            }

            member.onclick = async (event) => {
                await this.onRemoveMemberClick(event);
            }

            membersList.appendChild(member);
        })
    }
}

window.customElements.define('organization-component', OrganizationComponent);
