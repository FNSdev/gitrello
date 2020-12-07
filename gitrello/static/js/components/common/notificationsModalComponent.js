const template = document.createElement('template')
template.innerHTML = `
    <style>
      .notifications-modal {
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
      
      .notifications-modal__content {
        background-color: #fefefe;
        margin: 100px auto;
        border: 3px solid var(--primary-dark);
        border-radius: 10px;
        width: 30%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }
    </style>
    
    <div id="notifications-modal" class="notifications-modal">
     <div class="notifications-modal__content" id="notifications-modal-content">
       <errors-list-component id="errors"></errors-list-component> 
     </div>
   </div>
`

export class NotificationsModalComponent extends HTMLElement {
    constructor() {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));
    }

    connectedCallback() {
        if (window.MESSAGES.length === 0) {
            return;
        }

        const modal = this.shadowRoot.getElementById('notifications-modal');
        const errors = this.shadowRoot.getElementById('errors');

        window.MESSAGES.forEach(message => {
            if (message['type'] === 'error') {
                errors.addError(message['text']);
            }
            else if (message['type'] === 'warning') {
                errors.addWarningMessage(message['text']);
            }
            else if (message['type'] === 'success') {
                errors.addSuccessMessage(message['text']);
            }
            else {
                errors.addInfoMessage(message['text']);
            }
        })

        modal.style.display = "block";
        modal.onclick = (event) => {
            if (event.target === modal) {
                modal.style.display = "none";
                window.MESSAGES = [];
            }
        };
    }
}

window.customElements.define('notifications-modal-component', NotificationsModalComponent);
