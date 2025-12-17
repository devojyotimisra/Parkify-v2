<template>
    <Navbar role-name="admin" />
    <main class="container py-4">
        <h1 class="mb-4">Search Results</h1>

        <div class="card mb-4">
            <div class="card-body">
                <form @submit.prevent="performSearch" class="row g-3 align-items-end">
                    <div class="col-md-8">
                        <label for="query" class="form-label">Search Query</label>
                        <input type="text" class="form-control" id="query" v-model="searchQuery"
                            placeholder="Enter search query" />
                    </div>
                    <div class="col-md-4">
                        <label for="type" class="form-label">Search Type</label>
                        <select class="form-select" id="type" v-model="searchType">
                            <option value="lot">Parking Lot</option>
                            <option value="user">User</option>
                            <option value="vehicle">Vehicle Number</option>
                        </select>
                    </div>
                </form>
            </div>
        </div>

        <div class="card">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0">Results for "{{ searchQuery }}"</h5>
            </div>
            <div class="card-body">
                <div v-if="results.length > 0">
                    <div v-if="searchType === 'lot'" class="table-responsive">
                        <table class="table table-hover table-striped mb-0">
                            <thead>
                                <tr>
                                    <th>Lot ID</th>
                                    <th>Location Name</th>
                                    <th>Address</th>
                                    <th>Price/Hour</th>
                                    <th>Total Spots</th>
                                    <th>Available</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="lot in results" :key="lot.id">
                                    <td>{{ lot.id }}</td>
                                    <td>{{ lot.prime_location_name }}</td>
                                    <td>{{ lot.address }}</td>
                                    <td>₹{{ lot.price?.toFixed(2) || '0.00' }}</td>
                                    <td>{{ lot.maximum_number_of_spots }}</td>
                                    <td>{{ lot.available_spots_count }}</td>
                                    <td>
                                        <button class="btn btn-sm btn-primary" @click="viewSpots(lot.id)">View
                                            Spots</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div v-else-if="searchType === 'user'" class="table-responsive">
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
                                <tr v-for="(user, index) in results" :key="user.id">
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

                    <div v-else-if="searchType === 'vehicle'" class="table-responsive">
                        <table class="table table-hover table-striped mb-0">
                            <thead>
                                <tr>
                                    <th>Vehicle Number</th>
                                    <th>User ID (Last Booked)</th>
                                    <th>User Email (Last Booked)</th>
                                    <th>User Name (Last Booked)</th>
                                    <th>User Active (Last Booked)</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="result in results" :key="result.vehicle_number">
                                    <td>{{ result.vehicle_number }}</td>
                                    <td>{{ result.user_id }}</td>
                                    <td>{{ result.user_email }}</td>
                                    <td>{{ result.user_name }}</td>
                                    <td>
                                        <span class="badge" :class="result.user_active ? 'bg-success' : 'bg-danger'">
                                            {{ result.user_active ? 'Active' : 'Inactive' }}
                                        </span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <p v-else class="text-center mb-0">No results found for your query.</p>
            </div>
        </div>
        <Modal v-model="showSpotsModal" :title="`Parking Lot: ${selectedLot?.prime_location_name || ''}`" size="xl"
            no-footer centered>
            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Lot Information</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <p><strong>Address:</strong> {{ selectedLot?.address }}</p>
                            <p><strong>Pin Code:</strong> {{ selectedLot?.pin_code }}</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Price per Hour:</strong> ₹{{ selectedLot?.price?.toFixed(2) || '0.00' }}</p>
                            <p><strong>Total Spots:</strong> {{ selectedLot?.maximum_number_of_spots }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Current Parking Lot Situation</h5>
                </div>
                <div class="card-body">
                    <div class="d-flex flex-wrap">
                        <div v-for="(spot, index) in spotDetails" :key="spot.id"
                            class="rounded d-flex align-items-center justify-content-center text-white fw-bold"
                            :class="spot.status === 'A' ? 'bg-success' : 'bg-danger'"
                            style="width: 40px; height: 40px; margin: 3px; cursor: pointer"
                            :title="`Spot #${spot.id} - ${spot.status}`"
                            @click="spot.status === 'O' ? viewSpotDetails(spot.id) : null">
                            {{ index + 1 }}
                        </div>
                    </div>
                    <div class="mt-3">
                        <span class="badge bg-success p-2 me-2">Available</span>
                        <span class="badge bg-danger p-2">Occupied</span>
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Parking Spots Details</h5>
                </div>
                <div class="card-body p-0">
                    <div class="table-responsive">
                        <table class="table table-striped mb-0">
                            <thead>
                                <tr>
                                    <th>Spot ID</th>
                                    <th>Status</th>
                                    <th>User</th>
                                    <th>Vehicle Number</th>
                                    <th>Parking Time</th>
                                    <th>Details</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="detail in spotDetails" :key="detail.id">
                                    <td>{{ detail.id }}</td>
                                    <td>
                                        <span class="badge" :class="detail.status === 'A' ? 'bg-success' : 'bg-danger'">
                                            {{ detail.status }}
                                        </span>
                                    </td>
                                    <td>{{ detail.reservation?.name || '-' }}</td>
                                    <td>{{ detail.reservation?.vehicle_number || '-' }}</td>
                                    <td>{{ formatDateTime(detail.reservation?.parking_timestamp) || '-' }}</td>
                                    <td>
                                        <button v-if="detail.status === 'O'" class="btn btn-sm btn-info"
                                            @click="viewSpotDetails(detail.id)">View Details</button>
                                        <span v-else>-</span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </Modal>

        <Modal v-model="showSpotDetailsModal" title="Occupied Parking Spot Details" size="lg" no-footer centered>
            <div class="card">
                <div class="card-header bg-danger text-white">
                    <h5 class="mb-0">Spot #{{ selectedSpot?.id }}</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <p><strong>User:</strong> {{ selectedSpot?.reservation?.name }}</p>
                            <p><strong>Email:</strong> {{ selectedSpot?.reservation?.email }}</p>
                            <p><strong>Address:</strong> {{ selectedSpot?.reservation?.address }}</p>
                            <p><strong>Pin code:</strong> {{ selectedSpot?.reservation?.pincode }}</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Vehicle Number:</strong> {{ selectedSpot?.reservation?.vehicle_number }}</p>
                            <p><strong>Parking Time:</strong> {{ formatDateTime(selectedSpot?.reservation?.parking_timestamp) || '-' }}</p>
                            <p><strong>Hours Parked:</strong> {{ selectedSpot?.reservation?.hours_parked?.toFixed(2) }} hours</p>
                            <p><strong>Estimated Cost:</strong> ₹{{ selectedSpot?.reservation?.estimated_cost?.toFixed(2) }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </Modal>
    </main>
</template>

<script setup>
import { ref, watch } from 'vue';
import Modal from '@/components/Modal.vue';
import { useToast } from '@/components/useToast';
import Navbar from '@/components/Navbar.vue';

const API_BASE = import.meta.env.VITE_API_BASE_URL;

const { create } = useToast();
const searchQuery = ref('');
const searchType = ref('lot');
const results = ref([]);
const showSpotsModal = ref(false);
const showSpotDetailsModal = ref(false);
const spotDetails = ref([]);
const selectedLot = ref(null);
const selectedSpot = ref(null);

watch([searchQuery, searchType], () => {
    performSearch();
});

const performSearch = async () => {
    if (!searchQuery.value.trim()) {
        results.value = [];
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/admin/search`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                search_type: searchType.value,
                query: searchQuery.value
            })
        });

        const data = await response.json();

        if (response.ok) {
            results.value = data.results;
            if (data.message) {
                create({ title: data.message, variant: 'success' });
            }
        } else {
            results.value = [];
        }
    } catch (error) {
        results.value = [];
    }
};

const viewSpots = async (lotId) => {
    try {
        const response = await fetch(`${API_BASE}/admin/view_spots/${lotId}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const data = await response.json();

        if (response.ok) {
            selectedLot.value = data.lot;
            spotDetails.value = data.spots;
            showSpotsModal.value = true;
        } else {
            create({ title: data.message || 'Failed to fetch spots', variant: 'danger' });
        }
    } catch (error) {
        create({ title: 'Error fetching spots', variant: 'danger' });
    }
};

const viewSpotDetails = async (spotId) => {
    try {
        const response = await fetch(`${API_BASE}/admin/spot_details/${spotId}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const data = await response.json();

        if (response.ok) {
            selectedSpot.value = data;
            showSpotDetailsModal.value = true;
        } else {
            create({ title: data.message || 'Failed to fetch spot details', variant: 'danger' });
        }
    } catch (error) {
        create({ title: 'Error fetching spot details', variant: 'danger' });
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