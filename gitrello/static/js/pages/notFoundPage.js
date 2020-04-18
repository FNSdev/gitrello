import {Page, } from "./page.js";


export class NotFoundPage extends Page {
    notFoundTemplate = `
      <div class="not-found-container"></div>
    `

    getTemplate() {
        return this.notFoundTemplate;
    }
}