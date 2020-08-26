const template = document.createElement('template')
template.innerHTML = `
    <style>
      .btn {
        background-color: var(--primary-dark);
        border: none;
        border-radius: 12px;
        color: white;
        padding: 16px 32px;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
        cursor: pointer;
        width: 150px;
      }
      
      .btn-success {
        background-color: var(--green);
      }
      
      .btn-warning {
        background-color: var(--orange);
      }
      
      .btn-danger {
        background-color: var(--red);
      }
    </style>
    <button id="button" class="btn"></button>
`

export class ButtonComponent extends HTMLElement {
    constructor() {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));
    }

    connectedCallback() {
        const button = this.shadowRoot.querySelector('#button');

        if (this.getAttribute('type') === 'success') {
            button.classList.add('btn-success');
        }
        else if (this.getAttribute('type') === 'warning') {
            button.classList.add('btn-warning');
        }
        else if (this.getAttribute('type') === 'danger') {
            button.classList.add('btn-danger');
        }

        if (this.getAttribute('width') !== undefined) {
            button.style.width = this.getAttribute('width');
        }
        if (this.getAttribute('text') != null) {
            button.innerHTML = this.getAttribute('text');
        }
        else {
            button.innerHTML = this.innerHTML;
        }
    }
}

window.customElements.define('button-component', ButtonComponent);
