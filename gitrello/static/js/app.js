import {Router, } from "./router.js";

import {BoardComponent, } from "./components/boardComponent.js";
import {ButtonComponent, } from "./components/common/buttonComponent.js";
import {CategoryComponent, } from "./components/categoryComponent.js";
import {CommentComponent, } from "./components/commentComponent.js";
import {CreateBoardFormComponent, } from "./components/forms/createBoardFormComponent.js";
import {CreateBoardMembershipFormComponent, } from "./components/forms/createBoardMembershipFormComponent.js";
import {CreateCategoryFormComponent, } from "./components/forms/createCategoryFormComponent.js";
import {CreateOrganizationFormComponent, } from "./components/forms/createOrganizationFormComponent.js";
import {ErrorListComponent, } from "./components/common/errorsListComponent.js";
import {GithubConnectionComponent, } from "./components/githubConnectionComponent.js";
import {InputComponent, } from "./components/common/inputComponent.js";
import {LogInFormComponent, } from "./components/forms/logInFormComponent.js";
import {NotificationsModalComponent, } from "./components/common/notificationsModalComponent.js";
import {OrganizationComponent, } from "./components/organizationComponent.js";
import {OrganizationInviteComponent, } from "./components/organizationInviteComponent.js";
import {OrganizationMembershipComponent, } from "./components/organizationMembershipComponent.js";
import {ProfileComponent, } from "./components/profileComponent.js";
import {SendInviteFormComponent, } from "./components/forms/sendInviteFormComponent.js";
import {SignUpFormComponent, } from "./components/forms/signUpFormComponent.js";
import {TicketComponent, } from "./components/ticketComponents.js";
import {TicketDetailsComponent, } from "./components/ticketDetailsComponent.js";

(async () => await Router.build())();
