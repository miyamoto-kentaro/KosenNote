import {createRouter, createWebHistory, RouteRecordRaw} from "vue-router";
import {useStore} from "vuex";

import {store} from "../store";

import Home from "../views/Home.vue";
import Sample from "../views/user_auth/Sample.vue";

import SignInWithEmail from "../views/user_auth/SignInWithEmail.vue";
import WaitingEmail from "../views/user_auth/WaitingEmail.vue";
import EmailAuthentication from "../views/user_auth/EmailAuthentication.vue";
import ResetPassword from "../views/user_auth/ResetPassword.vue";
import ResetPasswordSendMail from "../views/user_auth/ResetPasswordSendMail.vue";
import ResetEmail from "../views/user_auth/ResetEmail.vue";
import ResetEmailSendMail from "../views/user_auth/ResetEmailSendMail.vue";
import LogIn from "../views/user_auth/LogIn.vue";
import Profile from "../views/user_auth/Profile.vue";
import CreateArticle from "../views/articles/CreateArticle.vue";
import ArticleDetail from "../views/articles/ArticleDetail.vue";
import EditArticle from "../views/articles/EditArticle.vue";
import Search from "../views/articles/Search.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Home",
    component: Home
  }, {
    path: "/sign-in/email/send-mail/",
    name: "SignInWithEmail",
    component: SignInWithEmail
  }, {
    path: "/sign-in/email/waiting-email/",
    name: "WaitingEmail",
    component: WaitingEmail
  }, {
    path: "/sign-in/email/authentication/:email/:code/",
    name: "EmailAuthentication",
    component: EmailAuthentication
  }, {
    path: "/reset-password/reset/:uid/:token/",
    name: "ResetPassword",
    component: ResetPassword
  }, {
    path: "/reset-password/send-mail/",
    name: "ResetPasswordSendMail",
    component: ResetPasswordSendMail
  }, {
    path: "/change/email/authentication/:email/:code/",
    name: "ResetEmail",
    component: ResetEmail
  }, {
    path: "/reset-email/send-mail/",
    name: "ResetEmailSendMail",
    component: ResetEmailSendMail
  }, {
    path: "/log-in/",
    name: "LogIn",
    component: LogIn
  }, {
    path: "/profile/:username/",
    name: "Profile",
    component: Profile,
    meta: {
      requireLogin: true
    }
  }, {
    path: "/create-article/",
    name: "CreateArticle",
    component: CreateArticle,
    meta: {
      requireLogin: true
    }
  }, {
    path: "/article-detail/:article_id/",
    name: "ArticleDetail",
    component: ArticleDetail
  }, {
    path: "/edit-article/:article_id/",
    name: "EditArticle",
    component: EditArticle,
    meta: {
      requireLogin: true
    }
  }, {
    path: "/search-article/:query/",
    name: "Search",
    component: Search
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next({
      name: "LogIn",
      query: {
        to: to.path
      }
    });
  } else {
    next();
  }
});

export default router;
