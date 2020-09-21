import {TicketDetailsComponent, } from "./ticketDetailsComponent.js";

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
        box-shadow: var(--default-shadow);
        border: 2px solid var(--primary-dark);
        border-radius: 16px;
        width: 70vw;
        cursor: pointer;
      }
         
      .container__assignees {
        width: 90%;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: end;
      }
      
      .container__assignees__list {
        display: flex;
        flex-direction: row;
        overflow-x: auto;
        scrollbar-color: var(--primary-dark) var(--primary-light);
      }
      
      .container__assignees__list__item {
        padding: 5px;
        border: 2px solid var(--green);
        border-radius: 50%;
        margin: 10px;
        cursor: pointer;
        font-size: 24px;
      }
         
      .container__line {
        width: 90%;
      }
      
      .container__due-date {
        margin-top: 10px;
        font-size: 12px;
        text-align: center;
      }
     
      .container__title {
        padding-right: 5px;
        padding-left: 5px;
        font-size: 24px;
        margin-top: 6px;
        margin-bottom: 6px;
        text-align: center;
        color: var(--primary-dark);
      }
      
      .ticket-modal {
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
      
      .ticket-modal__content {
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
      
      @media screen and (min-width: 992px) {
        .container {
          width: 16vw;
        }
        
        .ticket-modal__content {
          width: 50%;
        }
      }
    </style>
    <div draggable="true" class="container" id="container">
      <div class="container__assignees" id="assignees-list-container">
        <ul class="container__assignees__list" id="assignees-list"></ul>
      </div>
      <div id="due-date" class="container__due-date"></div>
      <hr class="container__line">
      <div id="title" class="container__title"></div>
    </div>
    
    <div id="ticket-modal" class="ticket-modal">
      <div class="ticket-modal__content" id="ticket-modal-content"></div>
    </div>
`

export class TicketComponent extends HTMLElement {
    constructor(ticket, categoryId, boardMemberships) {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        this.ticket = ticket;
        this.categoryId = categoryId;
        this.boardMemberships = boardMemberships;
        this.stateHasChanged = null;
    }

    connectedCallback() {
        this.shadowRoot.getElementById('container').addEventListener(
            'click',
            () => this.onClick(),
        );
        this.shadowRoot.getElementById('container').addEventListener(
            'dragstart',
            (event) => this.onDragStart(event),
        );
        this._insertTicket(this.ticket);
    }

    onClick() {
        this.shadowRoot.getElementById('ticket-modal').style.display = "block";
        const modal = this.shadowRoot.getElementById('ticket-modal');
        modal.onclick = (event) => {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        };

        const ticketDetailsComponent = new TicketDetailsComponent(this.ticket, this.boardMemberships);
        ticketDetailsComponent.callback = (ticket) => this.onTicketUpdated(ticket);
        this.shadowRoot.getElementById('ticket-modal-content').innerHTML = '';
        this.shadowRoot.getElementById('ticket-modal-content').appendChild(ticketDetailsComponent);
    }

    onTicketUpdated(ticket) {
        this.shadowRoot.getElementById('assignees-list').innerHTML = '';
        this.shadowRoot.getElementById('assignees-list-container').style.display = 'flex';
        this._insertTicket(ticket);
    }

    onDragStart(event) {
        event.dataTransfer.setData("ticket", JSON.stringify(this.ticket));
        event.dataTransfer.setData('categoryId', this.categoryId);
    }

    _insertTicket(ticket) {
        if (ticket.title !== null) {
            this.shadowRoot.getElementById('title').innerHTML = `${ticket.title}`;
        }
        else {
            this.shadowRoot.getElementById('title').innerHTML = `New Ticket`;
        }
        if (ticket.dueDate !== null) {
            this.shadowRoot.getElementById('due-date').innerHTML = `
                Should be done before <strong>${new Date(this.ticket.dueDate).toDateString()}</strong>
            `;
        }
        else {
            this.shadowRoot.getElementById('due-date').innerHTML = 'Ticket has no due date';
        }

        if (ticket.assignments.length === 0){
            this.shadowRoot.getElementById('assignees-list-container').style.display = 'none';
            return;
        }

        ticket.assignments.forEach(assignment => {
            const assigneeElement = document.createElement('li');
            assigneeElement.classList.add('container__assignees__list__item');
            assigneeElement.innerHTML = `
                ${assignment.boardMembership.organizationMembership.user.firstName[0]}${assignment.boardMembership.organizationMembership.user.lastName[0]}
            `;
            assigneeElement.setAttribute(
                'title',
                `${assignment.boardMembership.organizationMembership.user.firstName} ${assignment.boardMembership.organizationMembership.user.lastName}`,
            );
            this.shadowRoot.getElementById('assignees-list').appendChild(assigneeElement);
        });
    }
}

window.customElements.define('ticket-component', TicketComponent);
