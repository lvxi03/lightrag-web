import { createRouter, createWebHistory } from 'vue-router';
import { unauthorized } from "@/net";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/login' // 默认跳转到登录页面
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('@/views/login/App1.vue') // 登录页面
        },
        {
            path: '/register',
            name: 'register',
            component: () => import('@/views/register/App2.vue') // 注册页面
        },
        {
            path: '/forget',
            name: 'forget',
            component: () => import('@/views/forget/App3.vue') // 忘记密码页面
        },
        {
            path: '/reset_password',
            name: 'reset_password',
            component: () => import('@/views/welcome/ResetPassword.vue') // 重置密码页面
        },
        {
            path: '/index',
            name: 'index',
            component: () => import('@/views/index.vue') // 主页
        },
        {
            path: '/about',
            name: 'about',
            component: () => import('@/views/About.vue')
        },
        {
            path: '/main',
            name: 'main',
            component: () => import('@/views/ChatView.vue') // 聊天页面
        },
        {
            path: '/knowledge',
            name: 'knowledge',
            component: () => import('@/views/KnowledgeManagement.vue') // 聊天页面
        },
        {
            path: '/graph',
            name: 'graph',
            component: () => import('@/views/KnowledgeGraph.vue') // 聊天页面
        }
    ]
});

router.beforeEach((to, from, next) => {
    const isUnauthorized = unauthorized(); // 检查用户是否未授权
    if (to.name === 'index' && isUnauthorized) {
        next('/login'); // 如果用户未登录，跳转到登录页面
    } else if (['login', 'register', 'forget', 'reset_password'].includes(to.name) && !isUnauthorized) {
        next('/index'); // 如果用户已登录，跳转到主页
    } else {
        next(); // 其他情况下直接放行
    }
});

export default router;