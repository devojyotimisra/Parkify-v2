import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{ path: '/', component: () => import('@/views/general/home.vue') },
		{ path: '/login', component: () => import('@/views/general/login.vue') },
		{ path: '/signup', component: () => import('@/views/general/signup.vue') },
		
		{ path: '/notfound', component: () => import('@/views/general/error404.vue') },
		{ path: '/notallowed', component: () => import('@/views/general/error403.vue') },
		{ path: "/:pathMatch(.*)*", redirect: '/notfound' },

		{ path: '/dash/admin', component: () => import('@/views/admin/dashboard.vue'), meta: { requiresAuth: true } },
		{ path: '/dash/admin/users', component: () => import('@/views/admin/users.vue'), meta: { requiresAuth: true } },
		{ path: '/dash/admin/search', component: () => import('@/views/admin/search.vue'), meta: { requiresAuth: true } },
		{ path: '/dash/admin/history', component: () => import('@/views/admin/history.vue'), meta: { requiresAuth: true } },
		{ path: '/dash/admin/profile', component: () => import('@/views/admin/profile.vue'), meta: { requiresAuth: true } },
		
		{ path: '/dash/user', component: () => import('@/views/user/dashboard.vue'), meta: { requiresAuth: true } },
		{ path: '/dash/user/search', component: () => import('@/views/user/search.vue'), meta: { requiresAuth: true } },
		{ path: '/dash/user/history', component: () => import('@/views/user/history.vue'), meta: { requiresAuth: true } },
		{ path: '/dash/user/profile', component: () => import('@/views/user/profile.vue'), meta: { requiresAuth: true } },
	],
});

router.beforeEach((to, from, next) => {
	const token = localStorage.getItem('token');
	const role = localStorage.getItem('role');

	if (to.path === '/' && token && role) {
		return router.replace('/dash/' + role);
	}

	if (to.meta.requiresAuth && !token) {
		router.push('/notallowed');
	} else {
		next();
	}
});

export default router;