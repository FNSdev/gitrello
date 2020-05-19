import {routes, } from "./routes.js";
import {AuthService, } from "./services/authService.js";
import {NotFoundPage, } from "./pages/notFoundPage.js";

export class Router {
    static _instance = null;

    constructor(routes) {
        this.frame = window["main"]
        this.routes = routes
        this._page = null;

        window.addEventListener('popstate', event => this._onPopState(event));
        document.addEventListener("click", event => this._onPushState(event));
    }

    static async build() {
        if (Router._instance != null) {
            return Router._instance;
        }

        const router = new Router(routes);

        const path = window.location.pathname;
        window.history.replaceState({path}, path, path);
        router.path = path;

        await router._loadContent(path);

        Router._instance = router;
        return router;
    }

    async navigate(path) {
        if (this.path === path) {
            return;
        }

        window.history.pushState({path}, path, path);
        this.path = path;
        await this._loadContent(path);
    }

    async reload() {
        await this._page.beforeRender()
        this.frame.innerHTML = this._page.getTemplate()
        await this._page.afterRender()
    }

    async _onPopState(event) {
        this.path = window.location.pathname
        await this._loadContent(this.path);
    }

    async _onPushState(event) {
        const originalTarget = event.composedPath()[0];
        if (!originalTarget.classList.contains('route')) {
            return;
        }

        event.preventDefault();

        const path = originalTarget.pathname;
        await this.navigate(path);
    }

    async _loadContent(path) {
        console.log(path);

        const page = await this._getPage(path);

        await page.beforeRender()
        this.frame.innerHTML = page.getTemplate()
        await page.afterRender()

        this._page = page;
    }

    // TODO consider allowing search parameters and/or hash. I don`t think I need it
    async _getPage(path) {
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
        const authService = await AuthService.build();

        if (!matchedRoute) {
            return new NotFoundPage(authService, this, routeParams);
        }
        return new matchedRoute.page(authService, this, routeParams);
    }
}
