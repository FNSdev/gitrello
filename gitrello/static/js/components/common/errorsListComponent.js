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

    addError(errorMessage) {
        this.errorsList.innerHTML += `
          <li class="errors-container__list__item">${errorMessage}</li>
        `;
    }

    clear() {
        this.errorsList.innerHTML = '';
    }
}

window.customElements.define('errors-list-component', ErrorListComponent);
