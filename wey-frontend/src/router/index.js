import { createRouter, createWebHistory } from 'vue-router'
import FeedView from '../views/FeedView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'
import ChatView from '../views/ChatView.vue'
import SearchView from '../views/SearchView.vue'
import ProfileView from '../views/ProfileView.vue'
import FriendsView from '../views/FriendsView.vue'
import PostDetailView from '../views/PostDetailView.vue'
import TrendDetailView from '../views/TrendDetailView.vue'
import EditProfileView from '../views/EditProfileView.vue'
import EditPasswordView from '../views/EditPasswordView.vue'
import NotificationView from '../views/NotificationView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/feed',
      name: 'feed',
      component: FeedView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/profile/edit/:id',
      name: 'editprofile',
      component: EditProfileView
    },
    {
      path: '/profile/edit/password/:id',
      name: 'editpassword',
      component: EditPasswordView
    },
    {
      path: '/profile/:id/friends',
      name: 'friends',
      component: FriendsView
    },
    {
      path: '/post/:id/',
      name: 'postdetail',
      component: PostDetailView
    },
    {
      path: '/trend/:hashtag/',
      name: 'trenddetail',
      component: TrendDetailView
    },
    {
      path: '/notification/',
      name: 'notification',
      component: NotificationView
    },
  ]
})

export default router
