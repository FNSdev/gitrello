import {ticketRepository, } from "../repositories/ticketRepository.js";
import {TicketComponent, } from "./ticketComponents.js";

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
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 90vw;
        height: 90vh;
        cursor: pointer;
      }
      
      .container__name {
        font-size: 24px;
        text-align: center;
      }
      
      .container__tickets {
        border: 2px solid var(--primary-dark);
        border-radius: 6px;
        box-shadow: var(--default-shadow);
        width: 100%;
        height: 90%;
        overflow-y: auto;
        scrollbar-color: var(--primary-dark) var(--primary-light);
      }
      
      .container__tickets__list {
        display: flex;
        flex-direction: column;
        justify-content: start;
        align-items: center;
      }
      
      .container__tickets__list__item {
        margin: 10px;
      }
           
      .container__add-ticket-button {
        margin-top: 10px;
      }
      
      @media screen and (min-width: 992px) {
        .container {
          width: 18vw;
        }
      }
    </style>
    <div draggable="true" class="container" id="container">
      <h1 id="name" class="container__name"></h1>
      <div class="container__tickets" id="tickets-list-container">
        <ul class="container__tickets__list" id="tickets-list"></ul>
      </div>
      <button-component id="add-ticket-button" class="container__add-ticket-button" type="success">
        Add Ticket
      </button-component>
    </div>
`

export class CategoryComponent extends HTMLElement {
    constructor(category, boardMemberships) {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        this.category = category;
        this.boardMemberships = boardMemberships;
        this.stateHasChanged = null;
        this._ticketMoved = null;
        this._ticketDeleted = null;
    }

    connectedCallback() {
        this.shadowRoot.getElementById('name').innerHTML = this.category.name;
        this.shadowRoot.getElementById('add-ticket-button').addEventListener(
            'click',
            () => this.onAddTicketClick(),
        );
        this.shadowRoot.getElementById('tickets-list-container').addEventListener(
            'dragover', (event) => this.onDragOver(event),
        )
        this.shadowRoot.getElementById('tickets-list-container').addEventListener(
            'drop', (event) => this.onDrop(event),
        )
        this.shadowRoot.getElementById('container').addEventListener(
            'dragstart',
            (event) => this.onDragStart(event),
        );
        this._insertTickets(this.category.tickets);
    }

    async onAddTicketClick() {
        try {
            const ticket = await ticketRepository.create(this.category.id);
            this.category.tickets.push(ticket);
            this._insertTicket(ticket);
        }
        catch (e) {
            console.log(e);
            // TODO show error in modal?
        }
    }

    onDragStart(event) {
        event.dataTransfer.setData("category", JSON.stringify(this.category));
    }

    onDragOver(event) {
        if (event.dataTransfer.getData("ticket") === "") {
            return;
        }

        if (event.target.id === 'tickets-list-container' || event.target.id === 'tickets-list') {
            event.preventDefault();
        }
    }

    async onDrop(event) {
        event.stopPropagation();
        event.preventDefault();

        const ticket = JSON.parse(event.dataTransfer.getData("ticket"));
        const categoryId = event.dataTransfer.getData('categoryId');

        // Find ticket that dragged ticket should be inserted after
        let ticketComponentBefore = null;
        let insertAfterTicketId = null;
        this.shadowRoot.querySelectorAll('.container__tickets__list__item').forEach(ticketComponent => {
            if (ticketComponent.getBoundingClientRect().top < event.clientY) {
                ticketComponentBefore = ticketComponent;
                insertAfterTicketId = ticketComponent.ticket.id;
            }
        })

        if (
            (ticketComponentBefore == null && ticket.priority === 0 && categoryId === this.category.id) ||
            (ticketComponentBefore != null && ticket.priority === ticketComponentBefore.ticket.priority + 1
                && categoryId === this.category.id) ||
            (ticketComponentBefore != null && ticket.id === ticketComponentBefore.ticket.id)
        ) {
            // We don`t need to do anything if user tries to drag ticket exactly before/after itself
            return;
        }

        await ticketRepository.move(ticket, insertAfterTicketId, this.category.id)

        if (this._ticketMoved != null) {
            await this._ticketMoved();
        }
    }

    onTicketDeleted() {
        if (this._ticketDeleted != null) {
            this._ticketDeleted();
        }
    }

    set ticketMoved(callback) {
        this._ticketMoved = callback;
    }

    set ticketDeleted(callback) {
        this._ticketDeleted = callback;
    }

    _insertTicket(ticket) {
        const ticketComponent = new TicketComponent(ticket, this.category.id, this.boardMemberships);
        ticketComponent.classList.add('container__tickets__list__item');
        ticketComponent.ticketDeleted = () => this.onTicketDeleted();
        this.shadowRoot.getElementById('tickets-list').appendChild(ticketComponent);
    }

    _insertTickets(tickets) {
        tickets.forEach(ticket => this._insertTicket(ticket));
    }
}

window.customElements.define('category-component', CategoryComponent);
