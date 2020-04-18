import {NotFoundPage, } from "./pages/notFoundPage.js";

export class Router {
    constructor(renderer, routes) {
        this.frame = window["wrapper"]
        this.renderer = renderer
        this.routes = routes

        window.addEventListener('popstate', event => this.onPopState(event));
        window.addEventListener('load', event => {
                window["home"].addEventListener("click", event => this.pushState(event));
                window["profile"].addEventListener("click", event => this.pushState(event));
                window["organizations"].addEventListener("click", event => this.pushState(event));
                window["boards"].addEventListener("click", event => this.pushState(event));
            }
        )

        const href = window.location.pathname;
        window.history.replaceState({href}, href, href);
        this.href = window.location.href;
        this.loadContent(href);
    }

    onPopState(event) {
        this.href = window.location.href;
        this.loadContent(window.location.pathname);
    }

    pushState(event) {
        event.preventDefault();
        let href = event.target.href;

        if (this.href === href) {
            return;
        }

        window.history.pushState({href}, href, href);
        this.href = window.location.href;
        this.loadContent(window.location.pathname);
    }

    loadContent(href) {
        console.log(href);

        const page = this._getPage(href);

        page.beforeRender()
        this.renderer.render(this.frame, page.getTemplate())
        page.afterRender()
    }

    _getPage(href) {
        const pathNameSplit = href.split('/');
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
            return new NotFoundPage();
        }

        return new matchedRoute.page(routeParams);
    }
}