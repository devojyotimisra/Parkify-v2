<template>
    <Navbar role-name="admin" />
    <main class="container py-4">
        <h1 class="mb-4">Registered Users</h1>
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0">User List</h5>
            </div>
            <div class="card-body p-0">
                <div v-if="users.length > 0" class="table-responsive">
                    <table class="table table-hover table-striped mb-0">
                        <thead>
                            <tr>
                                <th>SL</th>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Address</th>
                                <th>Pin Code</th>
                                <th>Active</th>
                                <th>Default Vehicle Number</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(user, index) in users" :key="user.id">
                                <td>{{ index + 1 }}</td>
                                <td>{{ user.name }}</td>
                                <td>{{ user.email }}</td>
                                <td>{{ user.address }}</td>
                                <td>{{ user.pincode }}</td>
                                <td>
                                    <span class="badge" :class="user.active ? 'bg-success' : 'bg-danger'">
                                        {{ user.active ? 'Active' : 'Inactive' }}
                                    </span>
                                </td>
                                <td>{{ user.vehicle_number || 'N/A' }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div v-else class="p-4 text-center">
                    <p class="mb-0">No users registered yet.</p>
                </div>
            </div>
        </div>
    </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useToast } from '@/components/useToast';
import Navbar from '@/components/Navbar.vue';

const API_BASE = import.meta.env.VITE_API_BASE_URL;

const { create } = useToast();
const users = ref([]);

onMounted(() => {
    fetchUsers();
});

const fetchUsers = async () => {
    try {
        const response = await fetch(`${API_BASE}/admin/users`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const data = await response.json();

        if (response.ok) {
            users.value = data.users;
        } else {
            create({ title: data.message || 'Failed to load users', variant: 'danger' });
        }
    } catch (error) {
        create({ title: 'Error fetching users', variant: 'danger' });
    }
};
</script>