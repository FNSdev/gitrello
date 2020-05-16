import {boardRepository, } from "../../repositories/boardRepository.js";

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
      .form {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }
            
      .form__header {
        margin: 10px;
      }
      
      .form__input {
        margin-top: 10px;
      }
      
      .form__button {
        margin: 10px;
      }      
    </style>
    <form class="form">
      <h1 class="form__header">New Board</h1>
      <input-component required minlength="5" maxlength="100" id="form-board-name" type="text" class="form__input" placeholder="Board name"></input-component>
      <errors-list-component id="form-errors" class="form__errors"></errors-list-component>
      <button-component type="success" id="create-board-button" class="form__button"/>
        Create
      </button-component>
    </form>
`

export class CreateBoardFormComponent extends HTMLElement {
    constructor() {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        this._callback = null;
        this._organizationId = null;
    }

    connectedCallback() {
        this.shadowRoot.querySelector('#create-board-button').addEventListener(
            'click', () => this.onCreateBoard()
        );
    }

    async onCreateBoard() {
        const errorsList = this.shadowRoot.getElementById('form-errors');
        errorsList.clear();

        if (!this.shadowRoot.querySelector('#form-board-name').checkValidity()) {
            errorsList.addError(errorsList.defaultErrorMessage);
            return;
        }

        try {
            const board = await boardRepository.create(
                this.shadowRoot.querySelector('#form-board-name').value,
                this._organizationId,
            )

            if (this._callback != null) {
                this._callback(board);
            }
        }
        catch (e) {
            errorsList.addError(e.message);
        }
    }

    set callback(callback) {
        this._callback = callback;
    }

    set organizationId(id) {
        this._organizationId = id;
    }
}

window.customElements.define('create-board-form-component', CreateBoardFormComponent);
