import {Renderer, } from "./renderer.js";
import {Router, } from "./router.js";
import {routes} from "./routes.js";

class App {
    constructor(router) {
        this.router = router;
    }
}


const renderer = new Renderer();
const app = new App(new Router(renderer, routes));
