import {boardMembershipRepository, } from "../repositories/boardMembershipRepository.js";
import {boardRepositoryRepository, } from "../repositories/boardRepositoryRepository.js";
import {githubRepositoryRepository, } from "../repositories/githubRepositoryRepository.js";
import {CreateBoardMembershipFormComponent, } from "./forms/createBoardMembershipFormComponent.js";

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
        border: 3px solid var(--primary-dark);
        border-radius: 10px;
        box-shadow: var(--default-shadow);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 300px;
        padding: 10px;
        position: relative;
      }
      
      .container__name {
        font-size: 24px;
        text-decoration: none;
        width: 60%;
        word-break: break-word;
        text-align: center;
      }
      
      .container__settings-button {
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 80%;
        margin-top: 5px;
      }
      
      .container__board-memberships {
        margin-top: 10px;
        border: 2px solid var(--primary-dark);
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        justify-content: center;
      }
      
      .container__board-memberships__list {
        overflow-y: auto;
        height: 175px;
        width: 275px;
        scrollbar-color: var(--primary-dark) var(--primary-light);
      }
      
      .container__board-memberships__list__item {
        margin: 10px;
        text-align: center;
        cursor: pointer;
      }
      
      .container__add-member-button {
        margin-top: 10px;
      }
      
      .add-member-modal, .remove-member-modal, .settings-modal {
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
      
      .add-member-modal__content, .remove-member-modal__content, .settings-modal__content {
        background-color: #fefefe;
        margin: 100px auto;
        border: 3px solid var(--primary-dark);
        border-radius: 10px;
        width: 70%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }
      
      .remove-member-modal__content__header {
        margin: 10px;
        text-align: center;
      }
      
      .remove-member-modal__content__wrapper {
        display: flex;
        align-items: center;
        padding: 10px;
      }
      
      .remove-member-modal__content__wrapper__yes-button, .remove-member-modal__content__wrapper__cancel-button {
        margin: 10px;
      }
      
      .settings-modal__content {
        padding: 10px;
      }
      
      .settings-modal__content__repositories {
        border: 2px solid var(--primary-dark);
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        width: 90%;
      }
      
      .settings-modal__content__repositories__list {
        overflow-y: auto;
        height: 400px;
        scrollbar-color: var(--primary-dark) var(--primary-light);
      }
      
      .settings-modal__content__repositories__list__element {
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        padding: 5px;
        cursor: pointer;
      }
      
      .settings-modal__content__repositories__list__element--selected {
        color: var(--green);
      }
      
      @media screen and (min-width: 992px) {
        .add-member-modal__content, .remove-member-modal__content, .settings-modal__content {
          width: 30%;
        }
      }
    </style>
    <div class="container">
      <a id="name" class="container__name route"></a>
      <svg
        id="settings-button"
        class="container__settings-button" 
        xmlns="http://www.w3.org/2000/svg" x="0px" y="0px"
        width="42" height="42"
        viewBox="0 0 172 172"
        style=" fill:#000000;"><g fill="none" fill-rule="nonzero" stroke="none" stroke-width="1" stroke-linecap="butt" stroke-linejoin="miter" stroke-miterlimit="10" stroke-dasharray="" stroke-dashoffset="0" font-family="none" font-weight="none" font-size="none" text-anchor="none" style="mix-blend-mode: normal"><path d="M0,172v-172h172v172z" fill="none"></path><g><path d="M169.34609,86c0,-46.02344 -37.32266,-83.34609 -83.34609,-83.34609c-46.02344,0 -83.34609,37.32266 -83.34609,83.34609c0,46.02344 37.32266,83.34609 83.34609,83.34609c46.02344,0 83.34609,-37.32266 83.34609,-83.34609z" fill="#3498db"></path><path d="M139.81719,92.48359v-12.96719l-12.29531,-3.86328c-1.04141,-4.16563 -2.6875,-8.09609 -4.87109,-11.69062l5.97969,-11.45547l-9.17109,-9.17109l-11.48906,5.97969c-3.56094,-2.15 -7.45781,-3.7625 -11.62344,-4.80391l-3.89687,-12.3625h-13.00078l-3.89687,12.3625c-4.13203,1.04141 -8.0625,2.65391 -11.62344,4.80391l-11.38828,-5.97969l-9.20469,9.20469l5.97969,11.45547c-2.15,3.59453 -3.82969,7.49141 -4.87109,11.69062l-12.29531,3.86328v12.96719l12.22813,3.86328c1.04141,4.19922 2.6875,8.16328 4.87109,11.79141l-5.9125,11.2875l9.17109,9.17109l11.32109,-5.9125c3.62812,2.18359 7.62578,3.86328 11.85859,4.90469l3.82969,12.16094h13.00078l3.82969,-12.16094c4.23281,-1.04141 8.19688,-2.72109 11.85859,-4.90469l11.32109,5.9125l9.17109,-9.17109l-5.9125,-11.35469c2.18359,-3.62812 3.82969,-7.59219 4.87109,-11.79141zM86,114.4875c-15.68828,0 -28.42031,-12.73203 -28.42031,-28.42031c0,-15.68828 12.73203,-28.42031 28.42031,-28.42031c15.68828,0 28.38672,12.73203 28.38672,28.42031c0,15.72187 -12.69844,28.42031 -28.38672,28.42031z" fill="#ffffff"></path></g></g>
      </svg>
      <div class="container__board-memberships">
        <ul class="container__board-memberships__list" id="board-memberships-list"></ul>
      </div>
      <button-component id="add-member-button" class="container__add-member-button" type="info">
        Add
      </button-component>
    </div>
    
    <div id="add-member-modal" class="add-member-modal">
      <div class="add-member-modal__content" id="add-member-modal-content"></div>
    </div>
    
    <div id="remove-member-modal" class="remove-member-modal">
      <div class="remove-member-modal__content" id="remove-member-modal-content">
        <h1 class="remove-member-modal__content__header">Are you sure?</h1>
        <errors-list-component id="remove-member-errors" class="remove-member-modal__content__errors"></errors-list-component>
        <div class="remove-member-modal__content__wrapper">
          <button-component type="success" class="remove-member-modal__content__wrapper__yes-button" id="remove-member-button">
            Yes
          </button-component>
          <button-component type="danger" class="remove-member-modal__content__wrapper__cancel-button" id="cancel-remove-member-button">
            Cancel
          </button-component>
        </div>
      </div>
    </div>

    <div id="settings-modal" class="settings-modal">
      <div class="settings-modal__content" id="settings-modal-content">
        <div class="settings-modal__content__repositories">
          <ul class="settings-modal__content__repositories__list" id="repositories-list"></ul>
        </div>
        <errors-list-component id="repositories-errors" class="settings-modal__content__errors"></errors-list-component>
      </div>
    </div>
`

export class BoardComponent extends HTMLElement {
    constructor(board) {
        super();

        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        this.board = board;
    }

    connectedCallback() {
        this.shadowRoot.getElementById('name').innerHTML = this.board.name;
        this.shadowRoot.getElementById('name').setAttribute(
            'href',
            `/boards/${this.board.id}`,
        );
        this._insertMembers(this.board.boardMemberships);

        this.shadowRoot.getElementById('add-member-button').addEventListener(
            'click', () => this.onAddMemberButtonClick()
        );
        this.shadowRoot.getElementById('cancel-remove-member-button').addEventListener(
            'click', () => {
                this.shadowRoot.getElementById('remove-member-modal').style.display = "none";
            }
        )

        const addMemberForm = new CreateBoardMembershipFormComponent();
        addMemberForm.setAttribute('id', 'add-member-form');
        addMemberForm.callback = (member) => {
            this.afterMemberAdded(member);
        };
        addMemberForm.boardId = this.board.id;
        addMemberForm.organizationMemberships = this._getMembershipsDiff();
        this.shadowRoot.getElementById('add-member-modal-content').appendChild(addMemberForm);

        this.shadowRoot.getElementById('settings-button').onclick = async () => await this.onSettingsButtonClick();
    }

    onAddMemberButtonClick() {
        this.shadowRoot.getElementById('add-member-modal').style.display = "block";
        const modal = this.shadowRoot.getElementById('add-member-modal');
        modal.onclick = (event) => {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        };
    }

    onRemoveMemberClick(event) {
        this.shadowRoot.getElementById('remove-member-errors').clear();
        const boardMembershipId = event.target.getAttribute('id');
        const target = event.composedPath()[0];

        this.shadowRoot.getElementById('remove-member-modal').style.display = "block";
        const modal = this.shadowRoot.getElementById('remove-member-modal');
        modal.onclick = (event) => {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        };
        this.shadowRoot.getElementById('remove-member-button').onclick = async () => {
            try {
                await boardMembershipRepository.delete(boardMembershipId);
                this.board.boardMemberships = this.board.boardMemberships.filter(boardMembership => {
                    if (boardMembership.id !== boardMembershipId) {
                        return boardMembership;
                    }
                });
                target.remove();
                modal.style.display = "none";
                this.shadowRoot.getElementById('add-member-form').organizationMemberships = this._getMembershipsDiff();
            }
            catch (e) {
                this.shadowRoot.getElementById('remove-member-errors').addError(e.message);
            }
        }
    }

    async onSettingsButtonClick() {
        this.shadowRoot.getElementById('settings-modal').style.display = "block";

        try {
            const githubRepositories = await githubRepositoryRepository.getAll();
            const boardRepository = await boardRepositoryRepository.getByBoardId(this.board.id);
            this._insertGithubRepositories(githubRepositories, boardRepository);
        }
        catch (e) {
            console.log(e);
        }

        const modal = this.shadowRoot.getElementById('settings-modal');
        modal.onclick = (event) => {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        };
    }

    afterMemberAdded(member) {
        member.board = this.board;
        this.board.boardMemberships.push(member);
        this._insertMembers([member, ]);
    }

    async onGithubRepositoryClick(repositoryName, repositoryOwner) {
        try {
            const githubRepositories = await githubRepositoryRepository.getAll();
            const boardRepository = await boardRepositoryRepository.createOrUpdate(
                this.board.id,
                repositoryName,
                repositoryOwner,
            );
            this._insertGithubRepositories(githubRepositories, boardRepository);
        }
        catch (e) {
            console.log(e);
        }
    }

    _insertMembers(boardMemberships) {
        const membersList = this.shadowRoot.getElementById('board-memberships-list');

        boardMemberships.forEach(boardMembership => {
            const member = document.createElement('li');
            member.setAttribute('title', 'Click to remove');
            member.setAttribute('id', boardMembership.id);
            member.innerHTML = `${boardMembership.organizationMembership.user.firstName} ${boardMembership.organizationMembership.user.lastName}`;
            member.classList.add('container__board-memberships__list__item');
            member.onclick = (event) => {
                this.onRemoveMemberClick(event);
            }

            membersList.appendChild(member);
        })
    }

    _insertGithubRepositories(githubRepositories, boardRepository) {
        const repositoriesList = this.shadowRoot.getElementById('repositories-list');
        repositoriesList.innerHTML = "";

        const errors = this.shadowRoot.getElementById('repositories-errors');
        errors.clear();

        let wrongRepositorySelected = true;
        if (boardRepository == null) {
            wrongRepositorySelected = false;
        }

        githubRepositories.forEach(repository => {
            const li = document.createElement('li');
            li.innerHTML = `${repository.owner}/${repository.name}`;

            li.classList.add("settings-modal__content__repositories__list__element");
            if (boardRepository != null
                    && repository.name === boardRepository.repositoryName
                    && repository.owner === boardRepository.repositoryOwner) {
                li.classList.add("settings-modal__content__repositories__list__element--selected");
                wrongRepositorySelected = false;
            }

            li.onclick = async () => await this.onGithubRepositoryClick(repository.name, repository.owner);

            repositoriesList.appendChild(li);
        });

        if (wrongRepositorySelected) {
            errors.addWarningMessage(
                `Repository <strong>${boardRepository.repositoryOwner}/${boardRepository.repositoryName}</strong>
                 is selected for this board, but it is not present in your repositories. 
                 Perhaps it was renamed or deleted?`
            );
        }
    }

    _getMembershipsDiff() {
        const organizationMemberships = [];
        this.board.organization.organizationMemberships.forEach(organizationMembership => {
            const boardMembership = this.board.boardMemberships.find(boardMembership => {
                if (boardMembership.organizationMembership.id === organizationMembership.id) {
                    return boardMembership;
                }
            });

            if (boardMembership == null) {
                organizationMemberships.push(organizationMembership);
            }
        });
        return organizationMemberships;
    }
}

window.customElements.define('board-component', BoardComponent);
