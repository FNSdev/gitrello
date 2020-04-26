import {authService, } from "./services/authService.js";
import {NotFoundPage, } from "./pages/notFoundPage.js";

export class Router {
    constructor(renderer, routes) {
        this.frame = window["main-content"]
        this.renderer = renderer
        this.routes = routes

        window.addEventListener('popstate', event => this._onPopState(event));
        document.addEventListener("click", event => this._onPushState(event));

        const path = window.location.pathname;
        window.history.replaceState({path}, path, path);
        this.path = path;
        this._loadContent(path);
    }

    navigate(path) {
        if (this.path === path) {
            return;
        }

        window.history.pushState({path}, path, path);
        this.path = path;
        this._loadContent(path);
    }

    _onPopState(event) {
        this.href = window.location.href;
        this._loadContent(window.location.pathname);
    }

    _onPushState(event) {
        if (!event.target.classList.contains('route')) {
            return;
        }

        event.preventDefault();

        const path = event.target.pathname;
        this.navigate(path);
    }

    _loadContent(path) {
        console.log(path);

        const page = this._getPage(path);

        page.beforeRender()
        this.renderer.render(this.frame, page.getTemplate())
        page.afterRender()
    }

    // TODO consider allowing search parameters and/or hash. I don`t think I need it
    _getPage(path) {
        const pathNameSplit = path.split('/');
        const urlSegments = pathNameSplit.length > 1 ? pathNameSplit.slice(1) : '';
        const routeParams = {};

        const matchedRoute = this.routes.find(route => {
            const routePathSegments = route.path.split('/').slice(1);
            if (routePathSegments.length !== urlSegments.length) {
                return false;
            }

            const match = routePathSegments.every((routePathSegment, i) => {
                return routePathSegment === urlSegments[i] || routePathSegment[0] === ':';
            });

            if (!match) {
                return false;
            }

            routePathSegments.forEach((segment, i) => {
                if (segment[0] === ':') {
                    const propName = segment.slice(1);
                    routeParams[propName] = decodeURIComponent(urlSegments[i]);
                }
            });
            return true;
        });

        if (!matchedRoute) {
            return new NotFoundPage(authService, this, routeParams);
        }

        return new matchedRoute.page(authService, this, routeParams);
    }
}
