<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary sticky-top">
        <div class="container-fluid">
            <router-link class="navbar-brand" to="/">
                <img src="/favicon.png" alt="Logo" width="30" height="30" class="d-inline-block align-text-top me-2" />
                Parkify
            </router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <template v-if="roleName == 'admin'">
                        <li class="nav-item">
                            <router-link to="/dash/admin" class="btn btn-outline-success m-1">Home</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/dash/admin/users" class="btn btn-outline-success m-1">Users</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/dash/admin/search"
                                class="btn btn-outline-success m-1">Search</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/dash/admin/history"
                                class="btn btn-outline-success m-1">History</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/dash/admin/profile"
                                class="btn btn-outline-success m-1">Profile</router-link>
                        </li>
                        <li class="nav-item">
                            <button class="btn btn-outline-danger m-1"
                                @click="logoutModal = !logoutModal">Logout</button>
                            <Modal v-model="logoutModal" title="Logout Confirmation" header-bg-variant="danger"
                                ok-variant="danger" ok-title="Logout" @ok="handleLogout" centered>
                                Are you sure you want to log out?
                            </Modal>
                        </li>
                    </template>
                    <template v-else-if="roleName == 'user'">
                        <li class="nav-item">
                            <router-link to="/dash/user" class="btn btn-outline-success m-1">Home</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/dash/user/search" class="btn btn-outline-success m-1">Search</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/dash/user/history"
                                class="btn btn-outline-success m-1">History</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/dash/user/profile"
                                class="btn btn-outline-success m-1">Profile</router-link>
                        </li>
                        <li class="nav-item">
                            <button class="btn btn-outline-danger m-1"
                                @click="logoutModal = !logoutModal">Logout</button>
                            <Modal v-model="logoutModal" title="Logout Confirmation" header-bg-variant="danger"
                                ok-variant="danger" ok-title="Logout" @ok="handleLogout" centered>
                                Are you sure you want to log out?
                            </Modal>
                        </li>
                    </template>
                    <template v-else>
                        <li class="nav-item">
                            <router-link to="/login" class="btn btn-outline-success m-1">Login</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/signup" class="btn btn-outline-success m-1">Sign Up</router-link>
                        </li>
                    </template>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from '@/components/useToast';
import Modal from '@/components/Modal.vue';

const { create } = useToast();

const props = defineProps({
    roleName: {
        type: String,
        required: true
    }
});

const logoutModal = ref(false);
const router = useRouter();
const handleLogout = () => {
    localStorage.clear();
    router.replace('/');
    create({ title: 'Logged out successfully', variant: 'success', modelValue: 3000 });
};
</script>