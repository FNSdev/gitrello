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
      <div class="container__tickets">
        <ul class="container__tickets__list" id="tickets-list"></ul>
      </div>
      <button-component id="add-ticket-button" class="container__add-ticket-button" type="info">
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
    }

    connectedCallback() {
        this.shadowRoot.getElementById('name').innerHTML = this.category.name;
        this.shadowRoot.getElementById('add-ticket-button').addEventListener(
            'click',
            () => this.onAddTicketClick(),
        );
        this._insertTickets(this.category.tickets);
    }

    async onAddTicketClick() {
        try {
            const ticket = await ticketRepository.create(this.category.id);
            this._insertTicket(ticket);
        }
        catch (e) {
            console.log(e);
            // TODO show error in modal?
        }
    }

    _insertTickets(tickets) {
        tickets.forEach(ticket => this._insertTicket(ticket));
    }

    _insertTicket(ticket) {
        const ticketComponent = new TicketComponent(ticket, this.boardMemberships);
        ticketComponent.classList.add('container__tickets__list__item');
        this.shadowRoot.getElementById('tickets-list').appendChild(ticketComponent);
    }
}

window.customElements.define('category-component', CategoryComponent);
