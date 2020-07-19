import {boardRepository, } from "../repositories/boardRepository.js";
import {CategoryComponent, } from "../components/categoryComponent.js";
import {HttpClientPermissionDeniedError, } from "../errors.js";
import {Page, } from "./page.js";

export class BoardPage extends Page {
    template = `
      <div class="board-container">
        <div id="board-container-content" class="board-container__content">
          <div id="categories-list" class="board-container__content__categories-list">
            <create-category-form-component id="create-category-form"></create-category-form-component>
          </div>
        </div>
      </div>
    `

    constructor(authService, router, params) {
        super(authService, router, params);

        this.boardId = params['boardId'];
        this.hasAccess = true;
    }

    getTemplate() {
        if (!this.authService.isAuthenticated()) {
            return this.notAuthenticatedTemplate;
        }

        if (!this.hasAccess) {
            return this.accessDeniedTemplate;
        }

        return this.template;
    }

    async beforeRender() {
        await super.beforeRender();

        try {
            this.board = await boardRepository.get(this.boardId);
        }
        catch (e) {
            if (e instanceof HttpClientPermissionDeniedError) {
                this.hasAccess = false;
            }

            console.log(e);
        }
    }

    async afterRender() {
        await super.afterRender();

        if (!this.authService.isAuthenticated() || !this.hasAccess) {
            return;
        }

        const createCategoryForm = document.getElementById('create-category-form');
        createCategoryForm.boardId = this.board.id;
        createCategoryForm.callback = (category) => this._insertCategory(category);
        this._insertCategories(this.board.categories);
    }

    _insertCategories(categories) {
        categories.forEach(category => this._insertCategory(category));
    }

    _insertCategory(category) {
        const categoryComponent = new CategoryComponent(category, this.board.boardMemberships);
        categoryComponent.ticketMoved = async () => {
            await this.router.reload();
        }
        categoryComponent.classList.add('board-container__content__categories-list__item');
        document.getElementById('categories-list').insertBefore(
            categoryComponent,
            document.getElementById('create-category-form'),
        );
    }
}
