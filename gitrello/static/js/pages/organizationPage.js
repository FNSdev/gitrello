import {organizationRepository, } from "../repositories/organizationRepository.js";
import {HttpClientPermissionDeniedError, } from "../errors.js";
import {BoardComponent, } from "../components/boardComponent.js";
import {OrganizationComponent, } from "../components/organizationComponent.js";
import {Page, } from "./page.js";
import {CreateBoardFormComponent} from "../components/forms/createBoardFormComponent.js";

export class OrganizationPage extends Page {
    template = `
      <div class="organization-container">
        <div id="organizations-container-content" class="organization-container__content">
          <div id="boards-list" class="organization-container__content__boards-list"></div>
        </div>
      </div>
    `

    constructor(authService, router, params) {
        super(authService, router, params);

        this.organizationId = params['organizationId'];
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

        // TODO maybe its better to return 403 if member tries to get organization info
        try {
            this.organization = await organizationRepository.get(this.organizationId);
            const membership = this.organization.organizationMemberships.find(organizationMembership => {
                if (organizationMembership.user.id === this.authService.user.id) {
                    return organizationMembership;
                }
            })

            if (membership.role === 'MEMBER') {
                this.hasAccess = false;
            }
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

        const organizationComponent = new OrganizationComponent(this.organization);
        organizationComponent.stateHasChanged = () => this._stateHasChanged();
        document.getElementById('organizations-container-content').prepend(organizationComponent);

        this._insertBoards(this.organization.boards);
    }

    _stateHasChanged() {
        document.getElementById('boards-list').innerHTML = '';
        this._insertBoards(this.organization.boards);
    }

    _newBoardCallback(board) {
        this._insertBoard(board, true);
    }

    _insertBoard(board, prepend=false) {
        board.organization = this.organization;
        const boardComponent = new BoardComponent(board);

        if (prepend) {
            document.getElementById('boards-list').prepend(boardComponent);
        }
        else {
            document.getElementById('boards-list').appendChild(boardComponent);
        }
    }

    _insertBoards(boards) {
        boards.forEach(board => {
            this._insertBoard(board);
        });

        const createBoardFormComponent = new CreateBoardFormComponent();
        createBoardFormComponent.organizationId = this.organizationId;
        createBoardFormComponent.callback = (board) => this._newBoardCallback(board);
        document.getElementById('boards-list').appendChild(createBoardFormComponent);
    }
}
