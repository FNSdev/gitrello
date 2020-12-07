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
      .errors-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
      }
      
      .errors-container__list {
        overflow-y: auto;
        max-height: 300px;
      }
      
      .errors-container__list__item {
        margin: 10px;
        padding: 10px;
        border: 3px solid var(--red);
        border-radius: 15px;
        font-size: 16px;
        text-align: center;
        min-width: 175px;
      }
      
      .errors-container__list__item--success {
        border: 3px solid var(--green);
      }
      
      .errors-container__list__item--info {
        border: 3px solid var(--primary-dark);
      }
      
      .errors-container__list__item--warning {
        border: 3px solid var(--orange);
      }
    </style>
    <div class="errors-container">
      <ul id="errors-container-list" class="errors-container__list"></ul>          
    </div>
`

export class ErrorListComponent extends HTMLElement {
    defaultErrorMessage = 'Please, fill out required fields with correct data'

    constructor() {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));
        this.errorsList = this.shadowRoot.getElementById('errors-container-list');
    }

    addError(message) {
        this.errorsList.innerHTML += `
          <li class="errors-container__list__item">${message}</li>
        `;
    }

    addSuccessMessage(message) {
        this.errorsList.innerHTML += `
          <li class="errors-container__list__item errors-container__list__item--success">${message}</li>
        `;
    }

    addInfoMessage(message) {
        this.errorsList.innerHTML += `
          <li class="errors-container__list__item errors-container__list__item--info">${message}</li>
        `;
    }

    addWarningMessage(message) {
        this.errorsList.innerHTML += `
          <li class="errors-container__list__item errors-container__list__item--warning">${message}</li>
        `;
    }

    clear() {
        this.errorsList.innerHTML = '';
    }
}

window.customElements.define('errors-list-component', ErrorListComponent);
