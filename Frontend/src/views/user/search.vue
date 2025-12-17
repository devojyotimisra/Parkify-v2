<template>
    <Navbar role-name="user" />
    <main class="container py-4">
        <h1 class="mb-4">Search Available Parking Spaces</h1>
        <div class="card mb-4">
            <div class="card-body">
                <form @submit.prevent="performSearch" class="row g-3 align-items-end">
                    <div class="col-md-12">
                        <label for="location" class="form-label">Location</label>
                        <input type="text" class="form-control" id="location" v-model="searchLocation"
                            placeholder="Enter location name or address" />
                    </div>
                </form>
            </div>
        </div>

        <div class="card">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0">Results for "{{ searchLocation }}"</h5>
            </div>
            <div class="card-body p-0">
                <div v-if="availableLots.length > 0" class="table-responsive">
                    <table class="table table-hover table-striped mb-0">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Location</th>
                                <th>Address</th>
                                <th>Price/Hour</th>
                                <th>Availability</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="lot in availableLots" :key="lot.id">
                                <td>{{ lot.id }}</td>
                                <td>{{ lot.prime_location_name }}</td>
                                <td>{{ lot.address }}</td>
                                <td>₹{{ lot.price.toFixed(2) }}</td>
                                <td>{{ lot.available_spots_count }}/{{ lot.maximum_number_of_spots }}</td>
                                <td>
                                    <button class="btn btn-sm btn-primary" @click="selectSlot(lot)">Book</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div v-else class="p-4 text-center">
                    <p class="mb-0">No parking lots found matching your criteria or with available spots.</p>
                </div>
            </div>
        </div>

        <Modal v-model="showSelectSlotModal" title="Select Parking Space" size="lg" no-footer centered>
            <div class="text-center my-4">
                <div class="d-flex justify-content-center gap-3">
                    <span class="badge bg-success">Available</span>
                    <span class="badge bg-danger">Occupied</span>
                </div>
            </div>

            <form @submit.prevent="bookSlot">
                <div class="d-flex flex-wrap justify-content-center gap-2 mb-4">
                    <div v-for="(spot, index) in selectedLotSpots" :key="spot.id"
                        class="d-flex justify-content-center align-items-center border rounded fw-bold text-white"
                        :class="[spot.status === 'A' ? 'bg-success' : 'bg-danger', selectedSpotId === spot.id ? 'selected-glow' : '']"
                        style="width: 70px; height: 70px"
                        :style="{ cursor: spot.status === 'A' ? 'pointer' : 'not-allowed' }"
                        @click="spot.status === 'A' ? selectSpotId(spot.id) : null">
                        {{ index + 1 }}
                    </div>
                </div>

                <div class="mb-3">
                    <label for="vehicle_number" class="form-label">Vehicle Number</label>
                    <input type="text" class="form-control" id="vehicle_number" v-model="bookingForm.vehicle_number"
                        placeholder="Enter vehicle number" required
                        pattern="^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$" title="Format: DL01AB1234 (Uppercase)" />
                </div>

                <div class="mb-3">
                    <label for="parking_time" class="form-label">Parking Time</label>
                    <input type="text" class="form-control" id="parking_time" :value="formatDateTime(currentTime)"
                        disabled readonly />
                </div>

                <div class="d-grid gap-2 mt-4">
                    <button type="submit" class="btn btn-success" :disabled="!selectedSpotId || !bookingForm.vehicle_number">Book Selected
                        Space</button>
                    <button type="button" class="btn btn-outline-secondary"
                        @click="showSelectSlotModal = false">Cancel</button>
                </div>
            </form>
        </Modal>
    </main>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import Modal from '@/components/Modal.vue';
import { useToast } from '@/components/useToast';
import Navbar from '@/components/Navbar.vue';

const API_BASE = import.meta.env.VITE_API_BASE_URL;

const { create } = useToast();
const searchLocation = ref('');
const availableLots = ref([]);
const showSelectSlotModal = ref(false);
const selectedLot = ref(null);
const selectedLotSpots = ref([]);
const selectedSpotId = ref(null);
const currentTime = computed(() => new Date());

const bookingForm = ref({
    vehicle_number: ''
});

watch(searchLocation, () => {
    performSearch();
});

const performSearch = async () => {
    if (!searchLocation.value.trim()) {
        availableLots.value = [];
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/user/search`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                location: searchLocation.value
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Failed to search parking lots');
        }

        const data = await response.json();
        availableLots.value = data.results || [];
    } catch (error) {
        console.error('Error searching parking lots:', error);
        availableLots.value = [];
    }
};

const selectSpotId = (spotId) => {
    if (selectedSpotId.value === spotId) {
        selectedSpotId.value = null;
    } else {
        selectedSpotId.value = spotId;
    }
};

const selectSlot = async (lot) => {
    selectedLot.value = lot;
    selectedSpotId.value = null;

    const defaultVN = localStorage.getItem('vehicle_number');
    if (defaultVN) {
        bookingForm.value.vehicle_number = defaultVN;
    } else {
        bookingForm.value.vehicle_number = '';
    }

    try {
        const response = await fetch(`${API_BASE}/user/select_slot/${lot.id}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (!response.ok) throw new Error('Failed to fetch parking spots');

        const data = await response.json();
        selectedLotSpots.value = data.spots || [];
        showSelectSlotModal.value = true;
    } catch (error) {
        console.error('Error fetching spots:', error);
        create({ title: 'Failed to load parking spots', variant: 'danger' });
    }
};

const bookSlot = async () => {
    try {
        const response = await fetch(`${API_BASE}/user/book_slot/${selectedLot.value.id}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                spot_id: selectedSpotId.value,
                vehicle_number: bookingForm.value.vehicle_number
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Failed to book spot');
        }

        const data = await response.json();
        create({ title: data.message || 'Spot booked successfully', variant: 'success' });
        showSelectSlotModal.value = false;
        performSearch();
    } catch (error) {
        console.error('Error booking spot:', error);
        create({ title: error.message || 'Failed to book spot', variant: 'danger' });
    }
};

const formatDateTime = (timestamp) => {
    const date = new Date(timestamp);
    if (isNaN(date)) {
        return null;
    }
    return date.toLocaleString('en-IN');
};
</script>

<style scoped>
.selected-glow {
    box-shadow: 0 0 15px 5px rgba(25, 135, 84, 0.7);
    border: 2px solid white !important;
}
</style>