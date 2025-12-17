<template>
    <Navbar role-name="admin" />
    <main class="container my-auto py-4">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-6">
                <div class="card shadow">
                    <div class="card-header bg-primary text-white">
                        <h2 class="card-title text-center mb-0">Admin Profile</h2>
                    </div>
                    <div class="card-body p-4">
                        <div class="row mb-3">
                            <div class="col-md-4 fw-bold">Full Name:</div>
                            <div class="col-md-8">{{ currentUser.name }}</div>
                        </div>

                        <div class="row mb-3">
                            <div class="col-md-4 fw-bold">Email Address:</div>
                            <div class="col-md-8">{{ currentUser.email }}</div>
                        </div>

                        <div class="row mb-3">
                            <div class="col-md-4 fw-bold">Address:</div>
                            <div class="col-md-8">{{ currentUser.address }}</div>
                        </div>

                        <div class="row mb-3">
                            <div class="col-md-4 fw-bold">Pin Code:</div>
                            <div class="col-md-8">{{ currentUser.pincode }}</div>
                        </div>

                        <div class="d-grid gap-2 mt-4">
                            <button class="btn btn-warning" @click="showEditModal = true">Edit Profile</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <Modal v-model="showEditModal" title="Edit Your Profile" no-footer centered>
            <form @submit.prevent="updateProfile">
                <div class="mb-3">
                    <label for="email" class="form-label">Email Address</label>
                    <input type="email" class="form-control" id="email" v-model="editForm.email" required
                        pattern="^[^@ \t\r\n]+@[^@ \t\r\n]+$" title="Please enter a valid email address" />
                </div>
                <div class="mb-3">
                    <label for="name" class="form-label">Full Name</label>
                    <input type="text" class="form-control" id="name" v-model="editForm.name"
                        placeholder="Enter your full name" required minlength="2"
                        title="Name must be at least 2 characters long" />
                </div>
                <div class="mb-3">
                    <label for="address" class="form-label">Address</label>
                    <input type="text" class="form-control" id="address" v-model="editForm.address"
                        placeholder="Your complete address" required minlength="5"
                        title="Address must be at least 5 characters long" />
                </div>
                <div class="mb-3">
                    <label for="pincode" class="form-label">Pincode</label>
                    <input type="text" class="form-control" id="pincode" v-model="editForm.pincode"
                        placeholder="6-digit pincode" maxlength="6" minlength="6" pattern="\d{6}" required
                        title="Pincode must be a 6-digit number" />
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">New Password (optional)</label>
                    <input type="password" class="form-control" id="password" v-model="editForm.password"
                        placeholder="Leave blank to keep current password" minlength="5"
                        title="Password must be at least 5 characters long" />
                </div>
                <div class="mb-3">
                    <label for="confirm_password" class="form-label">Confirm New Password (optional)</label>
                    <input type="password" class="form-control" id="confirm_password"
                        v-model="editForm.confirm_password" placeholder="Leave blank to keep current password"
                        minlength="5" title="Password must be at least 5 characters long" />
                </div>
                <div class="d-grid gap-2 mt-4">
                    <button type="submit" class="btn btn-success">Update Profile</button>
                    <button type="button" class="btn btn-outline-secondary"
                        @click="showEditModal = false">Cancel</button>
                </div>
            </form>
        </Modal>
    </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Modal from '@/components/Modal.vue';
import { useToast } from '@/components/useToast';
import Navbar from '@/components/Navbar.vue';

const API_BASE = import.meta.env.VITE_API_BASE_URL;

const { create } = useToast();

const currentUser = ref({
    name: '',
    email: '',
    address: '',
    pincode: ''
});

const showEditModal = ref(false);

const editForm = ref({
    email: '',
    name: '',
    address: '',
    pincode: '',
    password: '',
    confirm_password: ''
});

onMounted(() => {
    fetchProfile();
});

const fetchProfile = async () => {
    try {
        const response = await fetch(`${API_BASE}/admin/profile`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch profile');
        }

        const data = await response.json();
        currentUser.value = {
            name: data.name || '',
            email: data.email || '',
            address: data.address || '',
            pincode: data.pincode || ''
        };
        editForm.value = { ...currentUser.value, password: '', confirm_password: '' };
    } catch (error) {
        console.error('Error fetching profile:', error);
        create({ title: 'Failed to load profile', variant: 'danger' });
    }
};

const updateProfile = async () => {
    if (editForm.value.password && editForm.value.password !== editForm.value.confirm_password) {
        create({ title: 'Passwords do not match', variant: 'danger' });
        return;
    }

    try {
        const payload = {
            name: editForm.value.name,
            email: editForm.value.email,
            address: editForm.value.address,
            pincode: editForm.value.pincode
        };

        if (editForm.value.password) {
            payload.password = editForm.value.password;
        }

        const response = await fetch(`${API_BASE}/admin/edit_profile`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error('Failed to update profile');
        }

        const data = await response.json();
        showEditModal.value = false;
        create({ title: data.message, variant: 'success' });
        fetchProfile();
    } catch (error) {
        console.error('Error updating profile:', error);
        create({ title: 'Failed to update profile', variant: 'danger' });
    }
};
</script>