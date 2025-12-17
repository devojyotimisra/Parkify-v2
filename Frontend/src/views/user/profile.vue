<template>
    <Navbar role-name="user" />
    <main class="container my-auto py-4">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-6">
                <div class="card shadow">
                    <div class="card-header bg-primary text-white">
                        <h2 class="card-title text-center mb-0">User Profile</h2>
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

                        <div class="row mb-3">
                            <div class="col-md-4 fw-bold">Vehicle Number:</div>
                            <div class="col-md-8">{{ currentUser.vehicle_number || 'Not provided' }}</div>
                        </div>

                        <div class="d-grid gap-2 mt-4">
                            <button class="btn btn-warning" @click="showEditModal = true">Edit Profile</button>
                            <button class="btn btn-danger" @click="showDeleteModal = true">Delete Account</button>
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
                    <label for="vehicle_number" class="form-label">Default Vehicle Number</label>
                    <input type="text" class="form-control" id="vehicle_number" v-model="editForm.vehicle_number"
                        placeholder="Enter your vehicle number" pattern="^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$"
                        title="Format: DL01AB1234 (Uppercase)" />
                    <div class="form-text">This will be pre-filled when booking a parking spot.</div>
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
                        minlength="5" title="Password must be at least 5 characters long" 
                        :class="{'is-invalid': confirmPasswordError}" @input="validateConfirmPassword"/>
                    <div class="invalid-feedback" v-if="confirmPasswordError">{{ confirmPasswordError }}</div>
                </div>
                <div class="d-grid gap-2 mt-4">
                    <button type="submit" class="btn btn-success">Update Profile</button>
                    <button type="button" class="btn btn-outline-secondary"
                        @click="showEditModal = false">Cancel</button>
                </div>
            </form>
        </Modal>

        <Modal v-model="showDeleteModal" title="Delete Account" no-footer centered>
            <div class="text-center">
                <p class="text-danger fw-bold">Warning: This action is irreversible!</p>
                <p>Are you sure you want to delete your account? All your data will be permanently removed.</p>
                <div class="d-grid gap-2 mt-4">
                    <button class="btn btn-danger" @click="deleteAccount">Yes, Delete My Account</button>
                    <button class="btn btn-outline-secondary" @click="showDeleteModal = false">Cancel</button>
                </div>
            </div>
        </Modal>
    </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Modal from '@/components/Modal.vue';
import { useToast } from '@/components/useToast';
import Navbar from '@/components/Navbar.vue';

const API_BASE = import.meta.env.VITE_API_BASE_URL;
const router = useRouter();

const { create } = useToast();
const currentUser = ref({
    name: '',
    email: '',
    address: '',
    pincode: '',
    vehicle_number: ''
});

const editForm = ref({
    email: '',
    name: '',
    address: '',
    pincode: '',
    vehicle_number: '',
    password: '',
    confirm_password: ''
});

const showEditModal = ref(false);
const showDeleteModal = ref(false);
const confirmPasswordError = ref('');

onMounted(() => {
    fetchProfile();
});

const validateConfirmPassword = () => {
    if(editForm.value.confirm_password.length===0){
        confirmPasswordError.value='';
        return;        
    }
    
    if (editForm.value.password != editForm.value.confirm_password)
    {
        confirmPasswordError.value="Password do not match";
    }else{
        confirmPasswordError.value='';
    }
}

const fetchProfile = async () => {
    try {
        const response = await fetch(`${API_BASE}/user/profile`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Failed to fetch profile');
        }

        const data = await response.json();
        currentUser.value = {
            name: data.name || '',
            email: data.email || '',
            address: data.address || '',
            pincode: data.pincode || '',
            vehicle_number: data.vehicle_number || ''
        };
        editForm.value = { ...currentUser.value, password: '', confirm_password: '' };
        localStorage.setItem('name', data.name);
    } catch (error) {
        console.error('Error fetching profile:', error);
        create({ title: error.message || 'Failed to fetch profile', variant: 'danger' });
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
            pincode: editForm.value.pincode,
            vehicle_number: editForm.value.vehicle_number
        };

        if (editForm.value.password) {
            payload.password = editForm.value.password;
        }

        const response = await fetch(`${API_BASE}/user/edit_profile`, {
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

const deleteAccount = async () => {
    try {
        const response = await fetch(`${API_BASE}/user/delete_account`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });


        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to delete account');
        }

        const data = await response.json();
        create({ title: data.message, variant: 'success' });

        localStorage.clear();

        router.replace('/');
    } catch (error) {
        console.error('Error deleting profile:', error);
        create({ title: error.message || 'Failed to delete account', variant: 'danger' });
    }
};
</script>