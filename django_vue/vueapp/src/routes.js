import Vue from 'vue'
import VueRouter from 'vue-router'
import Posts from './views/Posts'
import Posts from './views/Login'
import Posts from './views/Logout'

Vue.use(VueRouter)

export default new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'posts',
            component: Posts,
        }, 
        {
            path: '/login',
            name: 'login',
            component: Login,
        }, 
        {
            path: '/logout',
            name: 'logout',
            component: Logout,
        }, 
    ]
})