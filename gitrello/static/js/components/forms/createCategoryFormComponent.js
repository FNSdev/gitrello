import {categoryRepository, } from "../../repositories/categoryRepository.js";

const template = document.createElement('template')
template.innerHTML = `
    <style>
      .form {
        width: 100vw;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }
            
      .form__header {
        text-align: center;
        font-size: 24px;
      }
            
      .form__button {
        margin: 10px;
      }
      
      @media screen and (min-width: 992px) {
        .form {
          width: 20vw;
        }
      }   
    </style>
    <form class="form">
      <h1 class="form__header">New Category</h1>
      <input-component required minlength="3" maxlength="100" id="form-category-name" type="text" class="form__input" placeholder="Category name">
      </input-component>
      <errors-list-component id="form-errors" class="form__errors"></errors-list-component>
      <button-component type="success" id="create-category-button" class="form__button"/>
        Create
      </button-component>
    </form>
`

export class CreateCategoryFormComponent extends HTMLElement {
    constructor() {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        this._callback = null;
        this._boardId = null;
    }

    connectedCallback() {
        this.shadowRoot.getElementById('create-category-button').addEventListener(
            'click', () => this.onCreateCategory()
        );
    }

    async onCreateCategory() {
        const errorsList = this.shadowRoot.getElementById('form-errors');
        errorsList.clear();

        if (!this.shadowRoot.querySelector('#form-category-name').checkValidity()) {
            errorsList.addError(errorsList.defaultErrorMessage);
            return;
        }

        try {
            const category = await categoryRepository.create(
                this.shadowRoot.querySelector('#form-category-name').value,
                this._boardId,
            )

            if (this._callback != null) {
                this._callback(category);
            }
        }
        catch (e) {
            errorsList.addError(e.message);
        }
    }

    set boardId(value) {
        this._boardId = value;
    }

    set callback(callback) {
        this._callback = callback;
    }
}

window.customElements.define('create-category-form-component', CreateCategoryFormComponent);
