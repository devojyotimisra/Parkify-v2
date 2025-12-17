<template>
    <Navbar role-name="general" />
    <main class="container my-auto py-4">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-6">
                <div class="card shadow">
                    <div class="card-body p-4">
                        <h2 class="card-title text-center mb-4">Create Your Account</h2>
                        <form @submit.prevent="handleSignup">
                            <div class="mb-3">
                                <label for="email" class="form-label">Email Address</label>
                                <input type="email" class="form-control" id="email" v-model="email"
                                    placeholder="Enter your email" required pattern="^[^@ \t\r\n]+@[^@ \t\r\n]+$"
                                    title="Please enter a valid email address" />
                            </div>
                            <div class="mb-3">
                                <label for="password" class="form-label">Password</label>
                                <input type="password" class="form-control" id="password" v-model="password"
                                    placeholder="Create a password" required minlength="5"
                                    title="Password must be at least 5 characters long" />
                            </div>
                            <div class="mb-3">
                                <label for="confirm_password" class="form-label">Confirm Password</label>
                                <input type="password" class="form-control"
                                    :class="{ 'is-invalid': confirmPasswordError }" id="confirm_password"
                                    v-model="confirm_password" @input="validateConfirmPassword"
                                    placeholder="Re-enter your password" required minlength="5"
                                    title="Password must be at least 5 characters long" />
                                <div class="invalid-feedback" v-if="confirmPasswordError">
                                    {{ confirmPasswordError }}
                                </div>
                            </div>
                            <div class="mb-3">
                                <label for="name" class="form-label">Full Name</label>
                                <input type="text" class="form-control" id="name" v-model="name"
                                    placeholder="Enter your full name" required minlength="2"
                                    title="Name must be at least 2 characters long" />
                            </div>
                            <div class="mb-3">
                                <label for="address" class="form-label">Address</label>
                                <input type="text" class="form-control" id="address" v-model="address"
                                    placeholder="Your complete address" required minlength="5"
                                    title="Address must be at least 5 characters long" />
                            </div>
                            <div class="mb-3">
                                <label for="pincode" class="form-label">Pincode</label>
                                <input type="text" class="form-control" id="pincode" v-model="pincode"
                                    placeholder="6-digit pincode" pattern="\d{6}" maxlength="6" minlength="6" required
                                    title="Pincode must be a 6-digit number" />
                            </div>
                            <div class="mb-3">
                                <label for="vehicle_number" class="form-label">Vehicle Number</label>
                                <input type="text" class="form-control" id="vehicle_number" v-model="vehicle_number"
                                    placeholder="Enter vehicle number (Eg: DL01AB1234)"
                                    pattern="^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$"
                                    title="Format: DL01AB1234 (Uppercase)" />
                                <div class="form-text">
                                    This will be pre-filled when booking a parking spot.
                                </div>
                            </div>
                            <div class="d-grid gap-2 mt-4">
                                <button type="submit" class="btn btn-success" :disabled="!isFormValid">Sign Up</button>
                            </div>
                            <div class="text-center mt-3">
                                <p class="mb-0">
                                    Already have an account?
                                    <router-link to="/login" class="link-primary">Log in</router-link>
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
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from '@/components/useToast';
import Navbar from '@/components/Navbar.vue';

const router = useRouter();
const { create } = useToast();
const API_BASE = import.meta.env.VITE_API_BASE_URL;
const email = ref('');
const password = ref('');
const confirm_password = ref('');
const name = ref('');
const address = ref('');
const pincode = ref('');
const vehicle_number = ref('');
const confirmPasswordError = ref('');

const validateConfirmPassword = () => {
    if (confirm_password.value.length === 0) {
        confirmPasswordError.value = '';
        return;
    }

    if (password.value !== confirm_password.value) {
        confirmPasswordError.value = 'Passwords do not match';
    } else {
        confirmPasswordError.value = '';
    }
};

const isFormValid = computed(() => {
    return email.value.trim() !== '' &&
        password.value !== '' &&
        confirm_password.value !== '' &&
        name.value.trim() !== '' &&
        address.value.trim() !== '' &&
        pincode.value.trim() !== '' &&
        !confirmPasswordError.value;
});

const handleSignup = async () => {
    validateConfirmPassword();
    try {
        const response = await fetch(`${API_BASE}/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email.value.trim(),
                password: password.value,
                name: name.value.trim(),
                address: address.value.trim(),
                pincode: pincode.value.trim(),
                vehicle_number: vehicle_number.value.trim()
            })
        });
        const data = await response.json();
        if (response.ok) {
            create({ title: data.message, variant: 'success' });
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
        console.error('Error during signup:', error);
        create({ title: 'An error occurred during signup', variant: 'danger' });
    }
};
</script>