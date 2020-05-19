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
        width: 70vw;
      }
         
      .container__assignees {
        margin-top: 10px;
        border: 2px solid var(--primary-dark);
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        justify-content: center;
      }
      
      .container__assignees__list {
        overflow-y: auto;
        scrollbar-color: var(--primary-dark) var(--primary-light);
      }
      
      .container__tickets__list__item {
        margin: 10px;
        cursor: pointer;
      }
     
      .container__title {
        font-size: 24px;
        margin-top: 10px;
        text-align: center;
      }
      
      .container__due-date {
        font-size: 12px;
        margin-top: 10px;
      }
      
      @media screen and (min-width: 992px) {
        .container {
          width: 16vw;
        }
      }
    </style>
    <div class="container">
      <div class="container__assignees">
        <ul class="container__assignees__list" id="assignees-list"></ul>
      </div>
      <div id="due-date" class="container__due-date">Test Date</div>
      <div id="name" class="container__title">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Cupiditate, libero!</div>
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
    }
}

window.customElements.define('ticket-component', TicketComponent);
