<template>
    <Navbar role-name="user" />
    <main class="container py-4">
        <h1 class="mb-4">Welcome {{ userName }} !!!</h1>

        <div class="row mb-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header bg-primary text-white">Active Reservations</div>
                    <div class="card-body pb-0">
                        <div v-if="activeReservations.length > 0" class="row">
                            <div v-for="reservation in activeReservations" :key="reservation.id" class="col-md-6 mb-3">
                                <div class="p-3 border rounded h-100">
                                    <h5 class="card-title">{{ reservation.lot.prime_location_name }}</h5>
                                    <p class="card-text">
                                        <strong>Spot ID:</strong> {{ reservation.spot.id }}<br />
                                        <strong>Vehicle Number:</strong> {{ reservation.vehicle_number }}<br />
                                        <strong>Parking Time:</strong> {{ formatDateTime(reservation.parking_timestamp)
                                        }}<br />
                                        <strong>Price:</strong> ₹{{ reservation.parking_cost_per_unit_time.toFixed(2) }}
                                        per hour
                                    </p>
                                    <button class="btn btn-sm btn-danger" @click="releaseSpot(reservation)">Release
                                        Spot</button>
                                </div>
                            </div>
                        </div>
                        <div v-else>
                            <p class="card-text">You don't have any active parking reservations.</p>
                            <button class="btn btn-success mb-3" @click="$router.push('/dash/user/search')">Find
                                Parking</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header bg-success text-white">Available Parking Lots</div>
                    <div class="card-body">
                        <div v-if="availableLots.length > 0" class="table-responsive">
                            <table class="table table-hover table-striped mb-0">
                                <thead>
                                    <tr>
                                        <th>Location</th>
                                        <th>Address</th>
                                        <th>Price/Hour</th>
                                        <th>Available Spots</th>
                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="lot in availableLots" :key="lot.id">
                                        <td>{{ lot.prime_location_name }}</td>
                                        <td>{{ lot.address }}</td>
                                        <td>₹{{ lot.price.toFixed(2) }}</td>
                                        <td>{{ lot.available_spots_count }}/{{ lot.maximum_number_of_spots }}</td>
                                        <td>
                                            <button class="btn btn-sm btn-primary"
                                                @click="selectSlot(lot)">Book</button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <p v-else class="card-text">No parking lots with available spots at the moment.</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="d-grid gap-2 mt-4">
            <button type="submit" class="btn btn-lg btn-success" @click="exportCSV">Export CSV</button>
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
                        class="parking-space d-flex justify-content-center align-items-center border rounded fw-bold text-white"
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
                        placeholder="Enter vehicle number" required pattern="^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$"
                        title="Format: DL01AB1234 (Uppercase)" />
                </div>

                <div class="mb-3">
                    <label for="parking_time" class="form-label">Parking Time</label>
                    <input type="text" class="form-control" id="parking_time" :value="formatDateTime(currentTime)"
                        disabled readonly />
                </div>

                <div class="d-grid gap-2 mt-4">
                    <button type="submit" class="btn btn-success"
                        :disabled="!selectedSpotId || !bookingForm.vehicle_number">Book Selected
                        Space</button>
                    <button type="button" class="btn btn-outline-secondary"
                        @click="showSelectSlotModal = false">Cancel</button>
                </div>
            </form>
        </Modal>

        <Modal v-model="showReleaseModal" title="Release Parking Spot" no-footer centered>
            <form @submit.prevent="confirmRelease">
                <div class="mb-3">
                    <label for="release_vehicle_number" class="form-label">Vehicle Number</label>
                    <input type="text" class="form-control" id="release_vehicle_number"
                        :value="releaseForm.vehicle_number" disabled readonly />
                </div>
                <div class="mb-3">
                    <label for="parking_time" class="form-label">Parking Time</label>
                    <input type="text" class="form-control" id="parking_time"
                        :value="formatDateTime(releaseForm.parking_timestamp)" disabled readonly />
                </div>
                <div class="mb-3">
                    <label for="release_time" class="form-label">Release Time</label>
                    <input type="text" class="form-control" id="release_time" :value="formatDateTime(currentTime)"
                        disabled readonly />
                </div>
                <div class="mb-3">
                    <label for="duration" class="form-label">Duration</label>
                    <input type="text" class="form-control" id="duration"
                        :value="`${releaseForm.duration_hours.toFixed(2)} hours`" disabled readonly />
                </div>
                <div class="mb-3">
                    <label for="cost" class="form-label">Total Cost</label>
                    <input type="text" class="form-control" id="cost" :value="`₹${releaseForm.total_cost.toFixed(2)}`"
                        disabled readonly />
                </div>
                <div class="d-grid gap-2 mt-4">
                    <button type="submit" class="btn btn-danger">Release Spot</button>
                    <button type="button" class="btn btn-outline-secondary"
                        @click="showReleaseModal = false">Cancel</button>
                </div>
            </form>
        </Modal>
    </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import Modal from '@/components/Modal.vue';
import { useToast } from '@/components/useToast';
import Navbar from '@/components/Navbar.vue';

const API_BASE = import.meta.env.VITE_API_BASE_URL;

const { create } = useToast();
const userName = ref('');
const activeReservations = ref([]);
const availableLots = ref([]);
const showSelectSlotModal = ref(false);
const showReleaseModal = ref(false);
const selectedLot = ref(null);
const selectedLotSpots = ref([]);
const selectedSpotId = ref(null);
const currentTime = ref(new Date());
const bookingForm = ref({
    vehicle_number: ''
});
const releaseForm = ref({
    reservation_id: null,
    vehicle_number: '',
    parking_timestamp: '',
    duration_hours: 0,
    total_cost: 0
});

onMounted(() => {
    userName.value = localStorage.getItem('name') || 'User';
    fetchDashboardData();
});

const fetchDashboardData = async () => {
    try {
        const response = await fetch(`${API_BASE}/user/dash`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (!response.ok) throw new Error('Failed to fetch dashboard data');

        const data = await response.json();
        if (data.vehicle_number) {
            localStorage.setItem("vehicle_number", data.vehicle_number);
        } else {
            localStorage.removeItem("vehicle_number");
        }

        activeReservations.value = data.active_reservations.map(res => ({
            id: res.id,
            spot: { id: res.spot_id },
            lot: { prime_location_name: res.lot_name },
            vehicle_number: res.vehicle_number,
            parking_timestamp: new Date(res.parking_timestamp),
            parking_cost_per_unit_time: res.parking_cost_per_unit_time
        }));
        availableLots.value = data.available_lots || [];
    } catch (error) {
        console.error('Error fetching dashboard:', error);
        create({ title: 'Failed to load dashboard data', variant: 'danger' });
    }
};

const selectSlot = async (lot) => {
    selectedLot.value = lot;
    selectedSpotId.value = null;
    currentTime.value = new Date();

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

const selectSpotId = (spotId) => {
    if (selectedSpotId.value === spotId) {
        selectedSpotId.value = null;
    } else {
        selectedSpotId.value = spotId;
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
            create({ title: errorData.error || 'Failed to book spot', variant: 'danger' });
            throw new Error(errorData.message || 'Failed to book spot');
        }

        const data = await response.json();
        create({ title: data.message || 'Spot booked successfully', variant: 'success' });
        showSelectSlotModal.value = false;
        await fetchDashboardData();
    } catch (error) {
        console.error('Error booking spot:', error);
    }
};

const releaseSpot = (reservation) => {
    const parkingTime = new Date(reservation.parking_timestamp);
    const now = new Date();
    const durationHours = (now - parkingTime) / (1000 * 60 * 60);

    const totalCost = durationHours * reservation.parking_cost_per_unit_time;

    releaseForm.value = {
        reservation_id: reservation.id,
        vehicle_number: reservation.vehicle_number,
        parking_timestamp: reservation.parking_timestamp,
        duration_hours: durationHours,
        total_cost: totalCost
    };
    showReleaseModal.value = true;
};

const confirmRelease = async () => {
    try {
        const response = await fetch(`${API_BASE}/user/release_slot/${releaseForm.value.reservation_id}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Failed to release spot');
        }

        const data = await response.json();
        create({ title: data.message || 'Spot released successfully', variant: 'success' });
        showReleaseModal.value = false;
        await fetchDashboardData();
    } catch (error) {
        console.error('Error releasing spot:', error);
        create({ title: error.message || 'Failed to release spot', variant: 'danger' });
    }
};

const exportCSV = async () => {
    try {
        const response = await fetch(`${API_BASE}/user/export`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (!response.ok) throw new Error('Failed to export CSV');

        const data = await response.json();
        create({ title: data.message, variant: 'success' });
    } catch (error) {
        console.error('Error exporting CSV:', error);
        create({ title: 'Failed to export CSV', variant: 'danger' });
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