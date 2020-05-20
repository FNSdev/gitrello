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
        border: 2px solid var(--primary-dark);
        border-radius: 50%;
        margin: 10px;
        cursor: pointer;
        font-size: 24px;
      }
         
      .container__line {
        width: 90%;
      }
      
      .container__due-date {
        font-size: 12px;
        text-align: center;
      }
     
      .container__title {
        font-size: 24px;
        margin-top: 6px;
        margin-bottom: 6px;
        text-align: center;
      }
      
      @media screen and (min-width: 992px) {
        .container {
          width: 16vw;
        }
      }
    </style>
    <div class="container">
      <div class="container__assignees" id="assignees-list-container">
        <ul class="container__assignees__list" id="assignees-list"></ul>
      </div>
      <div id="due-date" class="container__due-date"></div>
      <hr class="container__line">
      <div id="title" class="container__title"></div>
    </div>
`

export class TicketComponent extends HTMLElement {
    constructor(ticket) {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        this.ticket = ticket;
        this.stateHasChanged = null;
    }

    connectedCallback() {
        this._insertTicket(this.ticket);
    }

    _insertTicket(ticket) {
        this.shadowRoot.getElementById('title').innerHTML = ticket.title;
        if (ticket.dueDate !== undefined) {
            this.shadowRoot.getElementById('due-date').innerHTML = `
                Should be done before <strong>${new Date(this.ticket.dueDate).toDateString()}</strong>
            `;
        }
        if (ticket.assignees.length === 0){
            this.shadowRoot.getElementById('assignees-list-container').style.display = 'none';
        }
        ticket.assignees.forEach(assignee => {
            const assigneeElement = document.createElement('li');
            assigneeElement.classList.add('container__assignees__list__item');
            assigneeElement.innerHTML = `
                ${assignee.organizationMembership.user.firstName[0]}${assignee.organizationMembership.user.lastName[0]}
            `;
            assigneeElement.setAttribute(
                'title',
                `${assignee.organizationMembership.user.firstName} ${assignee.organizationMembership.user.lastName}`,
            );
            this.shadowRoot.getElementById('assignees-list').appendChild(assigneeElement);
        });
    }
}

window.customElements.define('ticket-component', TicketComponent);
