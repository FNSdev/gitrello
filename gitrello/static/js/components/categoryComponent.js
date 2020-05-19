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
        margin-top: 10px;
        border: 2px solid var(--primary-dark);
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        justify-content: start;
        align-items: center;
        width: 90%;
        height: 90%;
      }
      
      .container__tickets__list {
        overflow-y: auto;
        scrollbar-color: var(--primary-dark) var(--primary-light);
      }
      
      .container__tickets__list__item {
        margin: 10px;
        cursor: pointer;
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
      <h1 id="name" class="container__name">Test Category</h1>
      <div class="container__tickets">
        <ul class="container__tickets__list" id="tickets-list"></ul>
      </div>
      <button-component id="add-ticket-button" class="container__add-ticket-button" type="info">
        Add Ticket
      </button-component>
    </div>
`

export class CategoryComponent extends HTMLElement {
    constructor(category) {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        this.category = category;
        this.stateHasChanged = null;
    }

    connectedCallback() {
        this._insertTickets(this.category.tickets);
    }

    _insertTickets(tickets) {
        tickets.forEach(ticket => {
            const ticketComponent = new TicketComponent(ticket);
            this.shadowRoot.getElementById('tickets-list').appendChild(ticketComponent);
        });
    }
}

window.customElements.define('category-component', CategoryComponent);
