
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('src/pages/PageHome.vue'),
        name: 'Home'
      },
      {
        path: '/about',
        component: () => import('src/pages/PageAbout.vue'),
        name: 'About'
      },
      {
        path: '/account',
        component: () => import('src/pages/Account.vue'),
        name: 'Account'
      },
    ]
  },
  {
    path: '/login',
    component: () => import('layouts/LoginLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('src/pages/Login.vue'),
        name: 'Login'
      },
      {
        path: '/register',
        component: () => import('src/pages/Register.vue'),
        name: 'Register'
      },
      {
        path: '/logout',
        component: () => import('src/pages/Logout.vue'),
        name: 'Logout'
      },
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
