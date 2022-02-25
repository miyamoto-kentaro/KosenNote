import {createRouter, createWebHistory, RouteRecordRaw} from "vue-router";
import Home from "../views/Home.vue";
import SignInWithEmail from "../views/user_auth/SignInWithEmail.vue";
import WaitingEmail from "../views/user_auth/WaitingEmail.vue";
import EmailAuthentication from "../views/user_auth/EmailAuthentication.vue";
import LogIn from "../views/user_auth/LogIn.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Home",
    component: Home
  }, {
    path: "/sign-in/email/send-mail",
    name: "SignInWithEmail",
    component: SignInWithEmail
  }, {
    path: "/sign-in/email/waiting-email",
    name: "WaitingEmail",
    component: WaitingEmail
  }, {
    path: "/sign-in/email/authentication/:email/:code",
    name: "EmailAuthentication",
    component: EmailAuthentication
  }, {
    path: "/log-in",
    name: "LogIn",
    component: LogIn
  }, {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import (
    /* webpackChunkName: "about" */
    "../views/About.vue")
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
