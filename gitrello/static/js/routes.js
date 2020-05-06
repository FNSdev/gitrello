import {HomePage, } from "./pages/homePage.js";
import {NotFoundPage, } from "./pages/notFoundPage.js";


// TODO
export const routes = [
    {
        path: '/',
        page: HomePage,
    },
    {
        path: '/profile',
        page: NotFoundPage,
    },
    {
        path: '/organizations',
        page: NotFoundPage,
    },
    {
        path: '/boards',
        page: NotFoundPage,
    },
];
