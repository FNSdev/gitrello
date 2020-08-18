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
        box-shadow: var(--default-shadow);
        border: 2px solid var(--primary-dark);
        border-radius: 16px;
        width: 300px;
      }
        
      .container__author {
        margin-top: 10px;
        font-size: 14px;
        text-align: center;      
      }  
        
      .container__date {
        margin-top: 10px;
        font-size: 12px;
        text-align: center;
      }
     
      .container__line {
        width: 90%;
      }
     
      .container__message {
        padding-right: 5px;
        padding-left: 5px;
        font-size: 18px;
        margin-top: 6px;
        margin-bottom: 6px;
        text-align: center;
        color: var(--primary-dark);
        border: none;
        overflow: hidden;
        resize: none;
        width: 90%;
      }
      
      @media screen and (min-width: 992px) {
        .container {
          width: 400px;
        }
      }
    </style>
    <div class="container" id="container">
      <div class="container__author"><strong id="author"></strong></div>
      <div class="container__date"><strong id="date"></strong></div>
      <hr class="container__line">
      <textarea readonly id="message" class="container__message"></textarea>
    </div>
`

export class CommentComponent extends HTMLElement {
    constructor(comment) {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        this.comment = comment;
    }

    connectedCallback() {
        this._insertComment(this.comment);
    }

    _insertComment(comment) {
        const messageTextArea = this.shadowRoot.getElementById('message');
        messageTextArea.value = comment.message;
        messageTextArea.style.height = `${messageTextArea.scrollHeight}px`;

        this.shadowRoot.getElementById('date').innerHTML = new Date(this.comment.addedAt).toUTCString();
        this.shadowRoot.getElementById('author').innerHTML = `
            ${comment.authorFirstName} ${comment.authorLastName}
        `
    }
}

window.customElements.define('comment-component', CommentComponent);
