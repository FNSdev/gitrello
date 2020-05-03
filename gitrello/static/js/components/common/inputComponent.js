const template = document.createElement('template')
template.innerHTML = `
    <style>
      :invalid {
        box-shadow: none;
      }
    
      input[type=text], input[type=email], input[type=password] {
        padding: 6px 10px;
        box-sizing: border-box;
        border: 2px solid var(--primary-dark);
        -webkit-transition: 0.5s;
        transition: 0.5s;
        outline: none;
        border-radius: 6px;
      }
           
      input[type=text]:invalid, input[type=email]:invalid, input[type=password]:invalid {
        border: 2px solid var(--red);
      }
      
      input[type=text]:valid, input[type=email]:valid, input[type=password]:valid {
        border: 2px solid var(--green);
      }
      
      input[type=text]:placeholder-shown, input[type=email]:placeholder-shown, input[type=password]:placeholder-shown {
        border: 2px solid var(--primary-dark);
      }
      
      .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 300px;
      }
      
      .error-message {
        margin-top: 10px;
        color: var(--red);
        font-size: 12px;
        text-align: center;
      }
    </style>
    <div class="container">
      <input id="input" class="input">
      <div id="error-message" class="error-message"></div>
    </div>
`

export class InputComponent extends HTMLElement {
    constructor() {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        this.input = this.shadowRoot.querySelector('#input');
        this.errorMessage = this.shadowRoot.querySelector('#error-message');
        this.input.setAttribute('required', this.getAttribute('required'));
        this.input.setAttribute('type', this.getAttribute('type'));
        this.input.setAttribute('placeholder', this.getAttribute('placeholder'));
        this.input.setAttribute('minlength', this.getAttribute('minlength'));
        this.input.setAttribute('maxlength', this.getAttribute('maxlength'));
        this.input.setAttribute('min', this.getAttribute('min'));
        this.input.setAttribute('max', this.getAttribute('max'));

        this.input.addEventListener('input', () => {
            if (!this.checkValidity()) {
                this.errorMessage.innerHTML = this.validationMessage;
            }
            else {
                this.errorMessage.innerHTML = '';
            }
        });
    }

    get value() {
        return this.shadowRoot.querySelector("#input").value;
    }

    set value(newValue) {
        this.shadowRoot.querySelector("#input").value = newValue;
    }

    checkValidity() {
        return this.shadowRoot.querySelector('#input').checkValidity();
    }

    get validationMessage() {
        return this.shadowRoot.querySelector('#input').validationMessage;
    }
}

window.customElements.define('input-component', InputComponent);
