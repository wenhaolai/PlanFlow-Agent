import { createRouter, createWebHistory } from 'vue-router'
import http from '@/utils/http'

import Login from '../views/LoginView.vue'
import Register from '../views/RegisterView.vue'
import Home from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { guestOnly: true }
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      meta: { guestOnly: true }
    }
  ],
})

// 全局前置守卫
router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('token')

  // 1. 如果访问的是游客页面（登录/注册）
  if (to.meta.guestOnly) {
    if (token) {
      try {
        // 验证 token 是否有效
        await http.get('/user/profile')
        // 如果有效，跳转到首页
        return next({ name: 'home' })
      } catch (error) {
        // 如果无效，清除 token 并允许访问登录页
        localStorage.removeItem('token')
        return next()
      }
    }
    return next()
  }

  // 2. 如果访问的是需要登录的页面
  if (!token) {
    // 如果没有 token，跳转到登录页
    return next({ name: 'login' })
  }

  // 3. 有 token，验证有效性
  try {
    // 这里可以优化：如果已经验证过（例如在 store 中有用户信息），可以跳过
    // 但根据需求，每次都调用接口验证
    await http.get('/user/profile')
    next()
  } catch (error) {
    // 验证失败，清除 token 并跳转到登录页
    localStorage.removeItem('token')
    next({ name: 'login' })
  }
})

export default router
