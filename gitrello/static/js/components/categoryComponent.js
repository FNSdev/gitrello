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
        width: 100vw;
        height: 90vh;
      }
      
      .container__name {
        font-size: 24px;
        text-align: center;
      }
      
      .container__tickets {
        border: 2px solid var(--primary-dark);
        border-radius: 6px;
        box-shadow: var(--default-shadow);
        width: 90%;
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
          width: 20vw;
        }
      }
    </style>
    <div class="container">
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
        this.ticketMovedFromAnotherCategory = null;
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

    removeTicket(ticketToRemove, oldPriority) {
        this.category.tickets = this.category.tickets.filter(ticket => {
            if (ticket.priority > oldPriority) {
                ticket.priority -= 1;
            }

            if (ticket.id !== ticketToRemove.id) {
                return ticket;
            }
        })

        // TODO It is a bit lazy, but much easier
        this.shadowRoot.getElementById('tickets-list').innerHTML = '';
        this._insertTickets(this.category.tickets);
    }

    onDragOver(event) {
        if (event.target.id === 'tickets-list-container' || event.target.id === 'tickets-list') {
            event.preventDefault();
        }
    }

    async onDrop(event) {
        event.preventDefault();

        const ticket = JSON.parse(event.dataTransfer.getData("ticket"));
        const categoryId = event.dataTransfer.getData('categoryId');

        // Find ticket that draggedTicket should be insert after
        let ticketComponentBefore = null;
        this.shadowRoot.querySelectorAll('.container__tickets__list__item').forEach(ticket => {
            if (ticket.getBoundingClientRect().top < event.clientY) {
                ticketComponentBefore = ticket;
            }
        })

        if (categoryId !== this.category.id) {
            const oldPriority = ticket.priority;
            await this._moveTicketFromAnotherCategory(ticket, this.category.id, ticketComponentBefore);
            if (this.ticketMovedFromAnotherCategory != null ) {
                this.ticketMovedFromAnotherCategory(ticket, oldPriority, categoryId);
            }
            return;
        }

        await this._moveTicket(ticket, ticketComponentBefore);
    }

    async _moveTicket(ticketToDrag, ticketComponentBefore) {
        if (
            (ticketComponentBefore == null && ticketToDrag.priority === 0) ||
            (ticketComponentBefore != null && ticketToDrag.id === ticketComponentBefore.ticket.id)
        ) {
            // We don`t need to do anything if user tries to drag ticket exactly before itself
            return;
        }

        // Find new priority for draggedTicket
        let newPriority = 0;
        if (ticketComponentBefore != null) {
            if (ticketToDrag.priority > ticketComponentBefore.ticket.priority) {
                newPriority = ticketComponentBefore.ticket.priority + 1;
            }
            else {
                newPriority = ticketComponentBefore.ticket.priority;
            }
        }

        if (newPriority === ticketToDrag.priority) {
            // We don`t need to do anything if user tries to drag ticket exactly after itself
            return;
        }

        console.log(newPriority);

        try {
            const oldPriority = ticketToDrag.priority;
            await ticketRepository.update(
                ticketToDrag,
                {
                    title: ticketToDrag.title,
                    dueDate: ticketToDrag.dueDate,
                    body: ticketToDrag.body,
                    priority: newPriority,
                    categoryId: this.category.id,
                }
            )

            // Update other ticket's priority
            if (oldPriority < newPriority) {
                // Ticket is being dragged down (its priority will be lowered)
                this.category.tickets.forEach(ticket => {
                    if (ticket.priority > oldPriority && ticket.priority <= newPriority) {
                        ticket.priority -= 1;
                    }
                });
            }
            else {
                // Ticket is being dragged up (its priority will be increased)
                this.category.tickets.forEach(ticket => {
                    if (ticket.priority < oldPriority && ticket.priority >= newPriority) {
                        ticket.priority += 1;
                    }
                });
            }

            // Remove draggedTicket from old index
            this.category.tickets = this.category.tickets.filter(ticket => {
                if (ticket.id !== ticketToDrag.id) {
                    return ticket;
                }
            });

            // Insert draggedTicket at new index
            this.category.tickets.splice(newPriority, 0, ticketToDrag);

            // TODO It is a bit lazy, but much easier
            this.shadowRoot.getElementById('tickets-list').innerHTML = '';
            this._insertTickets(this.category.tickets);
        }
        catch (e) {
            // TODO show alert or smth
            console.log(e);
        }
    }

    async _moveTicketFromAnotherCategory(ticketToDrag, categoryId, ticketComponentBefore) {
        let newPriority = 0;
        if (ticketComponentBefore != null) {
            newPriority = ticketComponentBefore.ticket.priority + 1;
        }

        try {
            await ticketRepository.update(
                ticketToDrag,
                {
                    title: ticketToDrag.title,
                    dueDate: ticketToDrag.dueDate,
                    body: ticketToDrag.body,
                    priority: newPriority,
                    categoryId: categoryId,
                }
            )

            this.category.tickets.forEach(ticket => {
                if (ticket.priority >= newPriority) {
                    ticket.priority += 1;
                }
            })

            this.category.tickets.splice(newPriority, 0, ticketToDrag);

            // TODO It is a bit lazy, but much easier
            this.shadowRoot.getElementById('tickets-list').innerHTML = '';
            this._insertTickets(this.category.tickets);
        }
        catch (e) {
            // TODO show alert or smth
            console.log(e);
        }
    }

    _insertTicket(ticket) {
        const ticketComponent = new TicketComponent(ticket, this.category.id, this.boardMemberships);
        ticketComponent.classList.add('container__tickets__list__item');
        this.shadowRoot.getElementById('tickets-list').appendChild(ticketComponent);
    }

    _insertTickets(tickets) {
        tickets.forEach(ticket => this._insertTicket(ticket));
    }
}

window.customElements.define('category-component', CategoryComponent);
