import {AuthService, } from "../services/authService.js";
import {CommentComponent, } from "./commentComponent.js";
import {commentRepository, } from "../repositories/commentRepository.js";
import {ticketAssignmentRepository, } from "../repositories/ticketAssignmentRepository.js";
import {ticketRepository, } from "../repositories/ticketRepository.js";
import {InputComponent, } from "./common/inputComponent.js";

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
        align-items: start;
      }
      
      .container__form, .container__comment-form {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 90%;
      }
           
      .container__form__due-date {
      }
      
      .container__form__body, .container__form__title {
        margin: 5px;
        border: 2px solid var(--primary-dark);
        border-radius: 8px;
        padding: 10px;
        width: 90%;
        resize: none;
        overflow: hidden;
        min-height: 10px;
      }
      
      .container__form__body {
        overflow: auto;
        height: 200px;
      }
      
      .container__comment-form__message {
        overflow: auto;
        height: 200px;
        border: 2px solid var(--primary-dark);
        border-radius: 8px;
        width: 90%;
        resize: none;
        padding: 10px;
      }
      
      .container__form__buttons {
        display: flex;
        flex-direction: row;
        margin-top: 10px;
      }
      
      .container__form__buttons__save-changes, .container__form__buttons__delete {
        padding: 5px;
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
        text-align: center;
      }
      
      .container__assignees {
        margin-top: 10px;
        height: 250px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: start;
      }
      
      .container__assignees__members-list {
        display: flex;
        flex-direction: column;
        overflow-y: auto;
        scrollbar-color: var(--primary-dark) var(--primary-light);
      }
      
      .container__assignees__members-list__item {
        border: 2px solid var(--primary);
        border-radius: 16px;
        font-size: 16px;
        padding: 15px;
        margin: 10px;
        text-align: center;
        cursor: pointer;
      }
     
      .container__assignees__members-list--assigned {
        border: 2px solid var(--green);
      }
          
      .container__comments-list {
        display: flex;
        flex-direction: column;
        justify-content: start;
        align-items: center;
      }
      
      .container__comments-list__item {
        margin-bottom: 10px;
      }
      
      .container__comment-form__button {
        margin-top: 10px;
      }

      @media screen and (min-width: 992px) {
          .container {
            grid-template-columns: 2fr 1fr;
          }      
      }
    </style>
    <div class="container">
      <form id="form" class="container__form">
        <textarea maxlength="100" placeholder="New ticket" id="form-title" class="container__form__title"></textarea>
        <textarea id="form-body" class="container__form__body"></textarea>
        <errors-list-component id="form-errors" class="container__form__errors"></errors-list-component>
        <div class="container__form__buttons">
          <button-component width="175px" type="success" id="save-changes-button" class="container__form__buttons__save-changes"/>
            Save Changes
          </button-component>
          <button-component width="175px" type="danger" id="delete-ticket-button" class="container__form__buttons__delete"/>
            Delete Ticket
          </button-component>        
        </div>
      </form>
      <div class="container__members">
          <div class="container__members__header"><strong>Click on Member to add or remove</strong></div>
          <input type="text" class="container__members__search" id="search" placeholder="Type to search">
          <errors-list-component id="members-errors" class="container__members__errors"></errors-list-component>
          <div class="container__assignees">
            <ul class="container__assignees__members-list" id="members-list"></ul>
          </div>
      </div>
      <div class="container__comments">
        <ul class="container__comments-list" id="comments-list"></ul>
      </div>
      <form id="comment-form" class="container__comment-form">
        <textarea id="comment-form-message" class="container__comment-form__message"></textarea>
        <errors-list-component id="comment-form-errors" class="container__comment-form__errors"></errors-list-component>
        <button-component width="175px" type="success" id="new-comment-button" class="container__comment-form__button"/>
          New Comment
        </button-component>
      </form>
    </div>
`

export class TicketDetailsComponent extends HTMLElement {
    constructor(ticket, boardMemberships) {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        this._ticket = ticket;
        this._ticketUpdated = null;
        this._ticketDeleted = null;

        this._boardMemberships = boardMemberships;
        this._boardMembershipsWithAssignments = this._getBoardMembershipsAndAssignments(boardMemberships);
    }

    async connectedCallback() {
        this.shadowRoot.getElementById('search').addEventListener('input', () => this.onSearchInput());
        this.shadowRoot.getElementById('save-changes-button').addEventListener(
            'click',
            () => this.onSaveChangesClick(),
        );
        this.shadowRoot.getElementById('delete-ticket-button').addEventListener(
            'click',
            () => this.onDeleteTicketClick(),
        );
        this.shadowRoot.getElementById('new-comment-button').addEventListener(
            'click',
            () => this.onNewCommentClick(),
        )

        const dateInput = new InputComponent();
        dateInput.setAttribute('id', 'form-due-date');
        dateInput.setAttribute('type', 'date');
        dateInput.value = this._ticket.dueDate;
        dateInput.classList.add('container__form__due-date');
        this.shadowRoot.getElementById('form').prepend(dateInput);

        const title = this.shadowRoot.getElementById('form-title');
        title.addEventListener('input', () => {
            title.style.height = "10px";
            title.style.height = title.scrollHeight + "px";
        })
        title.value = this._ticket.title;

        const ticketDetails = await ticketRepository.getTicketDetails(this._ticket.id);
        this._ticket.body = ticketDetails.body;
        this._ticket.comments = ticketDetails.comments;

        const body = this.shadowRoot.getElementById('form-body');
        body.addEventListener('input', () => {
            body.style.height = "10px";
            body.style.height = body.scrollHeight + "px";
        })
        body.value = this._ticket.body;

        this._insertMembers(this._boardMembershipsWithAssignments);
        this._insertComments(this._ticket.comments);
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

        if (!this.shadowRoot.getElementById('form-title').checkValidity() ||
            !this.shadowRoot.getElementById('form-due-date').checkValidity()
        ) {
            errorsList.addError(errorsList.defaultErrorMessage);
            return;
        }

        try {
            let title = this.shadowRoot.getElementById('form-title').value.trim();
            title = title === '' ? null : title;

            let body = this.shadowRoot.getElementById('form-body').value.trim();
            body = body === '' ? null : body;

            let date = this.shadowRoot.getElementById('form-due-date').value;
            date = date === '' ? null : date;

            this._ticket = await ticketRepository.update(
                this._ticket,
                {
                    title: title,
                    body: body,
                    dueDate: date,
                },
            );

            if (this._ticketUpdated != null) {
                this._ticketDeleted(this._ticket);
            }

            errorsList.addSuccessMessage('Success');
        }
        catch (e) {
            errorsList.addError(e.message);
        }
    }

    async onDeleteTicketClick() {
        const errorsList = this.shadowRoot.getElementById('form-errors');
        errorsList.clear();

        try {
            await ticketRepository.delete(this._ticket.id);

            if (this._ticketDeleted != null) {
                this._ticketDeleted();
            }
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
            if (this._ticketUpdated != null) {
                this._ticketUpdated(this._ticket);
            }
        }
        catch (e) {
            errorsList.addError(e.message);
        }
    }

    async onNewCommentClick() {
        const errorsList = this.shadowRoot.getElementById('comment-form-errors');
        errorsList.clear();

        try {
            let message = this.shadowRoot.getElementById('comment-form-message').value.trim();
            message = message === '' ? null : message;

            const comment = await commentRepository.create(this._ticket, message);
            const authService = await AuthService.build();
            comment.authorFirstName = authService.user.firstName;
            comment.authorLastName = authService.user.lastName;

            this._ticket.comments.push(comment);
            this._insertComment(comment, true);
        }
        catch (e) {
            errorsList.addError(e.message);
        }
    }

    set ticketUpdated(callback) {
        this._ticketUpdated = callback;
    }

    set ticketDeleted(callback) {
        this._ticketDeleted = callback;
    }

    _insertComment(comment, prepend=false) {
        const commentsList = this.shadowRoot.getElementById('comments-list');

        const commentComponent = new CommentComponent(comment);
        commentComponent.classList.add('container__comments-list__item');

        if (prepend) {
            commentsList.prepend(commentComponent);
        }
        else {
            commentsList.appendChild(commentComponent);
        }
    }

    _insertComments(comments) {
        comments.forEach(comment => {
            this._insertComment(comment);
        })
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

window.customElements.define('update-ticket-form-component', TicketDetailsComponent);
