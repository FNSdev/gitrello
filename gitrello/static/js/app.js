import {Router, } from "./router.js";

import {ButtonComponent, } from "./components/common/buttonComponent.js";
import {InputComponent, } from "./components/common/inputComponent.js";
import {LogInFormComponent, } from "./components/forms/logInFormComponent.js";
import {SignUpFormComponent, } from "./components/forms/signUpFormComponent.js";

(async () => await Router.build())();
