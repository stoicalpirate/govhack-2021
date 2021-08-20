import Vue from 'vue'
import VueRouter from 'vue-router'

// Import our views
import Home from "@/views/Home.vue"

// Use the router
Vue.use(VueRouter)

// Create our app routes
const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/about',
        name: 'About',
        component: () => import ("@/views/About")
    },
    {
        path: '/documentation',
        name: 'Documentation',
        component: () => import ("@/views/Documentation")
    },
    {
        path: '/privacy',
        name: 'Privacy',
        component: () => import ("@/views/Privacy")
    },
    {
        path: '/terms',
        name: 'Terms',
        component: () => import ("@/views/Terms")
    },
    {
        path: '/profile',
        name: 'Profile',
        component: () => import ("@/views/Profile")
    },
    {
        path: '/404',
        name: '404',
        component: () => import ("@/views/404")
    },
    // Redirect any unmatched routes to the 404 page.
    {
        path: '*',
        redirect: '404',
    },
]

// Create the router object
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
