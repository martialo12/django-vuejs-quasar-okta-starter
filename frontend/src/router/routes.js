
const routes = [
  { path: '/login', component: () => import('pages/LoginPage.vue') },
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', 
        component: () => import('pages/IndexPage.vue') ,
        meta: { requiresAuth: true }
      },
      // Example of a secure route
      { 
        path: '/protected', 
        component: () => import('pages/ProtectedPage.vue'),
        meta: { requiresAuth: true }
      }
    ]
  },

  // The callback route for Okta
  {
    path: '/authorization-code/callback',
    component: () => import('pages/LoginCallback.vue') ,
  },

  // Fallback route
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
];


export default routes
