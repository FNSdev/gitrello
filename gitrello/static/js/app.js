import {Renderer, } from "./renderer.js";
import {Router, } from "./router.js";
import {routes} from "./routes.js";

const renderer = new Renderer();
const router = new Router(renderer, routes);
