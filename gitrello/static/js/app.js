import {Router, } from "./router.js";

import {ButtonComponent, } from "./components/common/buttonComponent.js";
import {CreateBoardFormComponent, } from "./components/forms/createBoardFormComponent.js";
import {CreateOrganizationFormComponent, } from "./components/forms/createOrganizationFormComponent.js";
import {ErrorListComponent, } from "./components/common/errorsListComponent.js";
import {InputComponent, } from "./components/common/inputComponent.js";
import {LogInFormComponent, } from "./components/forms/logInFormComponent.js";
import {OrganizationMembershipComponent, } from "./components/organizationMembershipComponent.js";
import {SignUpFormComponent, } from "./components/forms/signUpFormComponent.js";

(async () => await Router.build())();
