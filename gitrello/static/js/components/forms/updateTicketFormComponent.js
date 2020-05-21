import {ticketAssignmentRepository, } from "../../repositories/ticketAssignmentRepository.js";

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
        padding: 10px;
        display: grid;
        grid-template-columns: 1fr;
        grid-gap: 2em;
        justify-items: center;
        align-items: center;
      }
      
      .container__form {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }
      
      .container__form__button {
        margin-top: 10px;
      }
      
      .container__members {
        display: flex;
        flex-direction: column;
        align-items: center;
      }
      
      .container__members__header {
        font-size: 24px;
        text-align: center;
      }
      
      .container__members__search {
        padding: 6px 10px;
        box-sizing: border-box;
        border: 2px solid var(--primary-dark);
        outline: none;
        border-radius: 6px;
        margin-top: 10px;
      }
      
      .container__assignees__members-list {
        margin-top: 10px;
      }
      
      .container__assignees__members-list__item {
        border: 2px solid;
        border-radius: 16px;
        font-size: 16px;
        padding: 15px;
        margin: 10px;
        text-align: center;
        cursor: pointer;
      }
      
      .container__assignees__members-list--assigned {
        border: 2px solid var(--secondary-dark);
      }
          
      @media screen and (min-width: 992px) {
          .container {
            grid-template-columns: 1fr 1fr;
            grid-gap: 10em;
          }      
      }
    </style>
    <div class="container">
      <form id="form" class="container__form">
        <errors-list-component id="form-errors" class="container__form__errors"></errors-list-component>
        <button-component width="175px" type="success" id="save-changes-button" class="container__form__button"/>
          Save Changes
        </button-component>
      </form>
      <div class="container__members">
          <h1 class="container__members__header">Click on Member to add or remove</h1>
          <input type="text" class="container__members__search" id="search" placeholder="Type to search">
          <errors-list-component id="members-errors" class="container__members__errors"></errors-list-component>
          <ul class="container__assignees__members-list" id="members-list"></ul>
      </div>
    </div>
`

export class UpdateTicketFormComponent extends HTMLElement {
    constructor(ticket, boardMemberships) {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        this._callback = null;
        this._ticket = ticket;

        this._boardMemberships = boardMemberships;
        this._boardMembershipsWithAssignments = this._getBoardMembershipsAndAssignments(boardMemberships);
    }

    connectedCallback() {
        this.shadowRoot.getElementById('search').addEventListener('input', () => this.onSearchInput());
        this.shadowRoot.getElementById('save-changes-button').addEventListener(
            'click',
            () => this.onSaveChangesClick(),
        );
        this._insertMembers(this._boardMembershipsWithAssignments);
    }

    onSearchInput() {
        const search = this.shadowRoot.getElementById('search').value.toLowerCase();

        const boardMemberships = [];
        this._boardMembershipsWithAssignments.forEach(boardMembership => {
            if (boardMembership['membership'].organizationMembership.user.firstName.toLowerCase().includes(search) ||
                boardMembership['membership'].organizationMembership.user.lastName.toLowerCase().includes(search)
            ) {
                boardMemberships.push(boardMembership);
            }
        });
        this._insertMembers(boardMemberships);
    }

    async onSaveChangesClick() {
        const errorsList = this.shadowRoot.getElementById('form-errors');
        errorsList.clear();

        // TODO
        if (false) {
            errorsList.addError(errorsList.defaultErrorMessage);
            return;
        }

        try {
        }
        catch (e) {
            errorsList.addError(e.message);
        }
    }

    async onMemberClick(event) {
        const errorsList = this.shadowRoot.getElementById('members-errors');
        const boardMembershipId = event.target.getAttribute('boardMembershipId');
        const assignmentId = event.target.getAttribute('assignmentId');

        errorsList.clear();
        try {
            if (assignmentId != null) {
                await ticketAssignmentRepository.delete(assignmentId);
                this._ticket.assignments = this._ticket.assignments.filter(assignment => {
                    if (assignment.boardMembership.id !== boardMembershipId) {
                        return assignment;
                    }
                })
            }
            else {
                const ticketAssignment = await ticketAssignmentRepository.create(
                    this._ticket.id,
                    boardMembershipId,
                );

                ticketAssignment.boardMembership = this._boardMemberships.find(boardMembership => {
                    if (boardMembership.id === boardMembershipId) {
                        return boardMembership;
                    }
                })
                this._ticket.assignments.push(ticketAssignment);
            }
            
            this._insertMembers(this._getBoardMembershipsAndAssignments(this._boardMemberships));
            if (this._callback != null) {
                this._callback(this._ticket);
            }
        }
        catch (e) {
            errorsList.addError(e.message);
        }
    }

    set callback(callback) {
        this._callback = callback;
    }

    _insertMembers(boardMembershipsWithAssignments) {
        const membersList = this.shadowRoot.getElementById('members-list');
        membersList.innerHTML = '';

        boardMembershipsWithAssignments.forEach(boardMembership => {
            const member = document.createElement('li');
            member.setAttribute('boardMembershipId', boardMembership['membership'].id);
            member.setAttribute('assign', boardMembership['isAssigned']);
            member.innerHTML = `
                ${boardMembership['membership'].organizationMembership.user.firstName} 
                ${boardMembership['membership'].organizationMembership.user.lastName}
            `;
            member.onclick = async (event) => {
                await this.onMemberClick(event);
            }

            member.classList.add('container__assignees__members-list__item');
            if (boardMembership['assignment'] != null) {
                member.classList.add('container__assignees__members-list--assigned');
                member.setAttribute('assignmentId', boardMembership['assignment'].id);
            }

            membersList.appendChild(member);
        })
    }
    
    _getBoardMembershipsAndAssignments(boardMemberships) {
        const boardMembershipsWithAssignments = [];
        boardMemberships.forEach(boardMembership => {
            const assignment = this._ticket.assignments.find(assignment => {
                if (assignment.boardMembership.id === boardMembership.id) {
                    return assignment;
                }
            });

            boardMembershipsWithAssignments.push({
                'membership': boardMembership,
                'assignment': assignment,
            });
        });
        
        return boardMembershipsWithAssignments;
    }
}

window.customElements.define('update-ticket-form-component', UpdateTicketFormComponent);
