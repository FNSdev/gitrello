import {BoardPage, } from "./pages/boardPage.js";
import {HomePage, } from "./pages/homePage.js";
import {OrganizationPage, } from "./pages/organizationPage.js";
import {OrganizationsPage, } from "./pages/organizationsPage.js";
import {ProfilePage, } from "./pages/profilePage.js";


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
        path: '/boards/:boardId',
        page: BoardPage,
    },
];
