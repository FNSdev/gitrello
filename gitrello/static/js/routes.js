import {BoardPage, } from "./pages/boardPage.js";
import {HomePage, } from "./pages/homePage.js";
import {NotFoundPage, } from "./pages/notFoundPage.js";
import {OrganizationPage, } from "./pages/organizationPage.js";
import {OrganizationsPage, } from "./pages/organizationsPage.js";
import {ProfilePage, } from "./pages/profilePage.js";


// TODO
export const routes = [
    {
        path: '/',
        page: HomePage,
    },
    {
        path: '/profile',
        page: ProfilePage,
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
    {
        path: '/boards/:boardId',
        page: BoardPage,
    },
];
