import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import Home from "../views/Home.vue";
import CreateReport from "../views/CreateReport.vue";
import MdEditor from "../views/MdEditor.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/create-report",
    name: "CreateReport",
    component: CreateReport,
  },
  {
    path: "/md-editor",
    name: "MdEditor",
    component: MdEditor,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
