import {organizationMembershipRepository, } from "../repositories/organizationMembershipRepository.js";
import {Role, } from "../models/organizationMembership.js"
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
      
      .send-invite-modal, .member-modal {
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
      
      .send-invite-modal__content, .member-modal__content {
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
      
      .member-modal__content__member-name, .member-modal__content__member-role {
        margin: 10px;
        text-align: center;
        font-size: 24px;
      }
      
      .member-modal__content__wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
      }
      
      .member-modal__content__wrapper__remove-member-button, .member-modal__content__wrapper__change-role-button {
        margin: 10px;
      }
      
      @media screen and (min-width: 992px) {
        .send-invite-modal__content, .member-modal__content {
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
    
    <div id="member-modal" class="member-modal">
      <div class="member-modal__content" id="member-modal-content">
        <div class="member-modal__content__member-name" id="member-name"></div>
        <div class="member-modal__content__member-role" id="member-role"></div>
        <div class="member-modal__content__wrapper">
          <button-component type="danger" class="member-modal__content__wrapper__remove-member-button" id="remove-member-button" width="300px">
            Remove member from organization
          </button-component>
          <button-component type="info" class="member-modal__content__wrapper__change-role-button" id="change-role-button" width="300px"></button-component>
        </div>
        <errors-list-component id="member-errors" class="member-modal__content__errors"></errors-list-component>
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

    onMemberClick(event) {
        this.shadowRoot.getElementById('member-errors').clear();

        const eventTarget = event.target;
        const organizationMembershipId = eventTarget.getAttribute('id');
        const role = eventTarget.getAttribute('role');
        const firstName = eventTarget.getAttribute('firstName');
        const lastName = eventTarget.getAttribute('lastName');

        this.shadowRoot.getElementById('member-name').innerHTML = `${firstName} ${lastName}`;
        this.shadowRoot.getElementById('member-role').innerHTML = `Role: ${role}`;

        if (role === Role.ADMIN) {
            this.shadowRoot.getElementById('change-role-button').setInnerHTML('Change Role to MEMBER');
        }
        else if (role === Role.MEMBER) {
            this.shadowRoot.getElementById('change-role-button').setInnerHTML('Change Role to ADMIN');
        }
        else {
            this.shadowRoot.getElementById('change-role-button').style.display = 'none';
        }

        const target = event.composedPath()[0];

        this.shadowRoot.getElementById('member-modal').style.display = "block";
        const modal = this.shadowRoot.getElementById('member-modal');
        modal.onclick = (event) => {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        };

        this.shadowRoot.getElementById('remove-member-button').onclick = async () => {
            await this.onRemoveMemberClick(target, organizationMembershipId);
        };
        this.shadowRoot.getElementById('change-role-button').onclick = async () => {
            await this.onChangeRoleClick(eventTarget, organizationMembershipId);
        };
    }

    async onRemoveMemberClick(target, organizationMembershipId) {
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
            this.shadowRoot.getElementById('member-modal').style.display = "none";

            if (this.stateHasChanged != null) {
                this.stateHasChanged();
            }
        }
        catch (e) {
            this.shadowRoot.getElementById('member-errors').addError(e.message);
        }
    }

    async onChangeRoleClick(eventTarget, organizationMembershipId) {
        try {
            const currentRole = eventTarget.getAttribute('role');

            let newRole;
            if (currentRole === Role.MEMBER) {
                newRole = Role.ADMIN;
            }
            else if (currentRole === Role.ADMIN) {
                newRole = Role.MEMBER;
            }
            else {
                return;
            }

            const role = await organizationMembershipRepository.updateRole(organizationMembershipId, newRole);
            const organizationMembership = this.organization.organizationMemberships.find(organizationMembership => {
                if (organizationMembership.id === organizationMembershipId) {
                    return organizationMembership;
                }
            })
            organizationMembership.role = role;
            eventTarget.setAttribute('role', role);

            this.shadowRoot.getElementById('member-role').innerHTML = `Role: ${role}`;

            if (role === Role.ADMIN) {
                this.shadowRoot.getElementById('change-role-button').setInnerHTML('Change Role to MEMBER');
            }
            else if (role === Role.MEMBER) {
                this.shadowRoot.getElementById('change-role-button').setInnerHTML('Change Role to ADMIN');
            }

            if (this.stateHasChanged != null) {
                this.stateHasChanged();
            }
        }
        catch (e) {
            this.shadowRoot.getElementById('member-errors').addError(e.message);
        }
    }

    _insertMembers(organizationMemberships) {
        const membersList = this.shadowRoot.getElementById('organization-memberships-list');

        organizationMemberships.forEach(organizationMembership => {
            const member = document.createElement('li');
            member.setAttribute('id', organizationMembership.id);
            member.setAttribute('role', organizationMembership.role);
            member.setAttribute('firstName', organizationMembership.user.firstName);
            member.setAttribute('lastName', organizationMembership.user.lastName);
            member.innerHTML = `${organizationMembership.user.firstName} ${organizationMembership.user.lastName}`;
            member.classList.add('container__organization-memberships__list__item');
            if (organizationMembership.role === 'OWNER') {
                member.classList.add('container__organization-memberships__list__item--owner');
            }

            member.onclick = (event) => {
                this.onMemberClick(event);
            }

            membersList.appendChild(member);
        })
    }
}

window.customElements.define('organization-component', OrganizationComponent);
