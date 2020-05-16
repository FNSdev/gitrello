import {HomePage, } from "./pages/homePage.js";
import {NotFoundPage, } from "./pages/notFoundPage.js";
import {OrganizationPage, } from "./pages/organizationPage.js";
import {OrganizationsPage, } from "./pages/organizationsPage.js";


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
        page: OrganizationsPage,
    },
    {
        path: '/organizations/:organizationId',
        page: OrganizationPage,
    },
    {
        path: '/boards',
        page: NotFoundPage,
    },
];
