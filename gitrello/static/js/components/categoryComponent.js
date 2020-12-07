import {categoryRepository} from "../repositories/categoryRepository.js";
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
        position: relative;
      }
      
      .container__name {
        font-size: 24px;
        text-align: center;
      }

      .container__settings-button {
        position: absolute;
        cursor: pointer;
        top: 90%;
        left: 82.5%;
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
      
      .settings-modal {
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
      
      .settings-modal__content {
        background-color: #fefefe;
        margin: 100px auto;
        border: 3px solid var(--primary-dark);
        border-radius: 10px;
        width: 70%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 10px;
      }
      
      .settings-modal__content__buttons-wrapper {
        margin-top: 10px;
      }
      
      @media screen and (min-width: 992px) {
        .container {
          width: 18vw;
        }
        
        .settings-modal__content {
          width: 30%;
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
      <svg
        id="settings-button"
        class="container__settings-button" 
        xmlns="http://www.w3.org/2000/svg" x="0px" y="0px"
        width="42" height="42"
        viewBox="0 0 172 172"
        style=" fill:#000000;"><g fill="none" fill-rule="nonzero" stroke="none" stroke-width="1" stroke-linecap="butt" stroke-linejoin="miter" stroke-miterlimit="10" stroke-dasharray="" stroke-dashoffset="0" font-family="none" font-weight="none" font-size="none" text-anchor="none" style="mix-blend-mode: normal"><path d="M0,172v-172h172v172z" fill="none"></path><g><path d="M169.34609,86c0,-46.02344 -37.32266,-83.34609 -83.34609,-83.34609c-46.02344,0 -83.34609,37.32266 -83.34609,83.34609c0,46.02344 37.32266,83.34609 83.34609,83.34609c46.02344,0 83.34609,-37.32266 83.34609,-83.34609z" fill="#3498db"></path><path d="M139.81719,92.48359v-12.96719l-12.29531,-3.86328c-1.04141,-4.16563 -2.6875,-8.09609 -4.87109,-11.69062l5.97969,-11.45547l-9.17109,-9.17109l-11.48906,5.97969c-3.56094,-2.15 -7.45781,-3.7625 -11.62344,-4.80391l-3.89687,-12.3625h-13.00078l-3.89687,12.3625c-4.13203,1.04141 -8.0625,2.65391 -11.62344,4.80391l-11.38828,-5.97969l-9.20469,9.20469l5.97969,11.45547c-2.15,3.59453 -3.82969,7.49141 -4.87109,11.69062l-12.29531,3.86328v12.96719l12.22813,3.86328c1.04141,4.19922 2.6875,8.16328 4.87109,11.79141l-5.9125,11.2875l9.17109,9.17109l11.32109,-5.9125c3.62812,2.18359 7.62578,3.86328 11.85859,4.90469l3.82969,12.16094h13.00078l3.82969,-12.16094c4.23281,-1.04141 8.19688,-2.72109 11.85859,-4.90469l11.32109,5.9125l9.17109,-9.17109l-5.9125,-11.35469c2.18359,-3.62812 3.82969,-7.59219 4.87109,-11.79141zM86,114.4875c-15.68828,0 -28.42031,-12.73203 -28.42031,-28.42031c0,-15.68828 12.73203,-28.42031 28.42031,-28.42031c15.68828,0 28.38672,12.73203 28.38672,28.42031c0,15.72187 -12.69844,28.42031 -28.38672,28.42031z" fill="#ffffff"></path></g></g>
      </svg>
    </div>
    
    <div id="settings-modal" class="settings-modal">
      <div class="settings-modal__content" id="settings-modal-content">
        <input-component required minlength="5" maxlength="100" placeholder="New name" id="category-name-input">
        </input-component>
        <div class="settings-modal__content__buttons-wrapper">
          <button-component id="update-category-button" type="success">Save</button-component>
          <button-component id="delete-category-button" type="danger">Delete</button-component>
        </div>
        <errors-list-component id="settings-errors" class="settings-modal__content__errors"></errors-list-component>
      </div>
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
        this._categoryDeleted = null;
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
        this.shadowRoot.getElementById('settings-button').onclick = () => this.onSettingsButtonClick();
        this.shadowRoot.getElementById('update-category-button').onclick = async () => {
            await this.onUpdateCategoryButtonClick();
        }
        this.shadowRoot.getElementById('delete-category-button').onclick = async () => {
            await this.onDeleteCategoryButtonClick();
        }
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
        if (!event.dataTransfer.types.includes("ticket")) {
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

    set categoryDeleted(callback) {
        this._categoryDeleted = callback;
    }

    onSettingsButtonClick() {
        this.shadowRoot.getElementById('settings-modal').style.display = "block";
        const modal = this.shadowRoot.getElementById('settings-modal');
        modal.onclick = (event) => {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        };
    }

    async onUpdateCategoryButtonClick() {
        const errorsList = this.shadowRoot.getElementById('settings-errors');
        errorsList.clear();

        if (!this.shadowRoot.getElementById('category-name-input').checkValidity()) {
            errorsList.addError(errorsList.defaultErrorMessage);
            return;
        }

        try {
            const newName = this.shadowRoot.getElementById('category-name-input').value;
            const category = await categoryRepository.updateName(this.category, newName);
            this.shadowRoot.getElementById('name').innerHTML = category.name;
        }
        catch (e) {
            console.log(e);
            errorsList.addError(e);
        }
    }

    async onDeleteCategoryButtonClick() {
        const errorsList = this.shadowRoot.getElementById('settings-errors');
        errorsList.clear();

        try {
            await categoryRepository.delete(this.category);
            this.shadowRoot.getElementById('settings-modal').style.display = "none";
            if (this._categoryDeleted != null) {
                this._categoryDeleted();
            }
        }
        catch (e) {
            console.log(e);
            errorsList.addError(e);
        }
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
