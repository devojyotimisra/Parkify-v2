<template>
    <Navbar role-name="general" />
    <main class="container my-auto py-4">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-6">
                <div class="mb-4"></div>
                <div class="card shadow">
                    <div class="card-body p-4">
                        <h2 class="card-title text-center mb-4">Login to Your Account</h2>
                        <form @submit.prevent="handleLogin">
                            <div class="mb-3">
                                <label for="email" class="form-label">Email Address</label>
                                <input type="text" class="form-control" id="email" v-model="email"
                                    placeholder="Enter your email" value="" required
                                    pattern="^[^@ \t\r\n]+@[^@ \t\r\n]+$" title="Please enter a valid email address" />
                            </div>
                            <div class="mb-3">
                                <label for="password" class="form-label">Password</label>
                                <input type="password" class="form-control" id="password" v-model="password"
                                    placeholder="Enter password" required minlength="5"
                                    title="Password must be at least 5 characters long" />
                            </div>
                            <div class="d-grid gap-2 mt-4">
                                <button type="submit" class="btn btn-success">Login</button>
                            </div>
                            <div class="text-center mt-3">
                                <p class="mb-0">
                                    Don't have an account?
                                    <router-link to="/signup" class="link-primary">Sign up</router-link>
                                </p>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from '@/components/useToast';
import Navbar from '@/components/Navbar.vue';

const router = useRouter();
const { create } = useToast();
const API_BASE = import.meta.env.VITE_API_BASE_URL;
const email = ref('');
const password = ref('');

onMounted(async () => {
    if (localStorage.getItem('token')) {
        const redirect = '/dash/' + localStorage.getItem('role');
        router.push({ path: redirect });
    }
});

const handleLogin = async () => {
    try {
        const response = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email.value,
                password: password.value
            })
        });
        const data = await response.json();
        if (response.ok) {
            create({ title: data.message, variant: 'success' });
            localStorage.clear();
            localStorage.setItem('token', data.token);
            localStorage.setItem('id', data.user.id);
            localStorage.setItem('email', data.user.email);
            localStorage.setItem('name', data.user.name);
            localStorage.setItem('role', data.user.role);
            const goto = '/dash/' + data.user.role;
            router.push({ path: goto });
        } else {
            create({ title: data.error, variant: 'danger' });
        }
    } catch (error) {
        console.error('Error during login:', error);
    }
};
</script>