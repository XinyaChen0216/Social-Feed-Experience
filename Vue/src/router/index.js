import { createRouter, createWebHistory } from 'vue-router'

import CreatePostView from "../views/CreatePostView.vue";
import FeedView from "../views/FeedView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/create",
      component: CreatePostView
    },
    {
      path: "/",
      component: FeedView
    },
  ],
})

export default router
