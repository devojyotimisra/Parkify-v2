<template>
    <Navbar role-name="admin" />
    <main class="container py-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1>Welcome {{ userName }} !!!</h1>
            <button class="btn btn-success me-2" @click="showAddLotModal = true">+ Add Lot</button>
        </div>

        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
            <div v-for="lot in parkingLots" :key="lot.id" class="col">
                <div class="card h-100">
                    <div class="card-header bg-primary text-white">
                        {{ lot.prime_location_name }}
                    </div>
                    <div class="card-body">
                        <h5 class="card-title">
                            Price: ₹{{ lot.price.toFixed(2) }} per hour
                        </h5>
                        <p class="card-text">
                            Address: {{ lot.address }}<br />
                            Pin Code: {{ lot.pin_code }}
                        </p>

                        <div class="mb-3">
                            <strong>Spots Status:</strong>
                            <div class="d-flex flex-wrap mt-2">
                                <div v-for="spot in lot.parking_spots" :key="spot.id"
                                    class="rounded border border-primary"
                                    :class="spot.status === 'A' ? 'bg-success' : 'bg-danger'"
                                    style="width: 30px; height: 30px; margin: 2px"
                                    :title="`Spot #${spot.id} - ${spot.status === 'A' ? 'Available' : 'Occupied'}`">
                                </div>
                            </div>
                        </div>

                        <div class="d-flex justify-content-between">
                            <div>
                                Total spots:
                                <span class="badge bg-primary">{{ lot.maximum_number_of_spots }}</span>
                            </div>
                            <div>
                                Available:
                                <span class="badge bg-success">{{ lot.available_spots_count }}</span>
                            </div>
                        </div>
                    </div>

                    <div class="card-footer d-flex justify-content-between">
                        <button class="btn btn-primary" @click="viewSpots(lot.id)">View Details</button>
                        <button class="btn btn-warning" @click="editLot(lot)">Edit</button>
                        <button class="btn btn-danger" @click="showdeleteLotModal = !showdeleteLotModal">Delete</button>
                    </div>
                    <Modal v-model="showdeleteLotModal" title="Delete Lot Confirmation" header-bg-variant="danger"
                        ok-variant="danger" ok-title="Delete" @ok="deleteLot(lot.id)" centered>
                        Are you sure you want to delete this parking lot?
                    </Modal>
                </div>
            </div>
        </div>

        <Modal v-model="showAddLotModal" title="New Parking Lot" no-footer centered>
            <form @submit.prevent="addLot">
                <div class="mb-3">
                    <label for="location" class="form-label">Prime Location Name</label>
                    <input type="text" class="form-control" id="location" v-model="lotForm.location"
                        placeholder="Enter location name" required minlength="2"
                        title="Location name must be at least 2 characters long" />
                </div>
                <div class="mb-3">
                    <label for="address" class="form-label">Address</label>
                    <input type="text" class="form-control" id="address" v-model="lotForm.address"
                        placeholder="Enter complete address" required minlength="5"
                        title="Address must be at least 5 characters long" />
                </div>
                <div class="mb-3">
                    <label for="pincode" class="form-label">Pin code</label>
                    <input type="text" class="form-control" id="pincode" v-model="lotForm.pincode"
                        placeholder="Enter 6-digit pincode" required minlength="6" maxlength="6" pattern="\d{6}"
                        title="Pincode must be a 6-digit number" />
                </div>
                <div class="mb-3">
                    <label for="price" class="form-label">Price (per hour)</label>
                    <input type="number" class="form-control" id="price" v-model="lotForm.price"
                        placeholder="Enter price per hour" step="0.01" min="0.01" required
                        title="Price must be greater than 0" />
                </div>
                <div class="mb-3">
                    <label for="spots" class="form-label">Maximum spots</label>
                    <input type="number" class="form-control" id="spots" v-model="lotForm.spots"
                        placeholder="Enter maximum spots" required min="1" title="Spot count must be greater than 0" />
                </div>
                <div class="d-grid gap-2 mt-4">
                    <button type="submit" class="btn btn-success">Add</button>
                    <button type="button" class="btn btn-outline-secondary"
                        @click="showAddLotModal = false">Cancel</button>
                </div>
            </form>
        </Modal>

        <Modal v-model="showEditLotModal" title="Edit Parking Lot" no-footer centered>
            <form @submit.prevent="updateLot">
                <div class="mb-3">
                    <label for="edit-location" class="form-label">Prime Location Name</label>
                    <input type="text" class="form-control" id="edit-location" v-model="editLotForm.location"
                        placeholder="Enter location name" required minlength="2"
                        title="Location name must be at least 2 characters long" />
                </div>
                <div class="mb-3">
                    <label for="edit-address" class="form-label">Address</label>
                    <input type="text" class="form-control" id="edit-address" v-model="editLotForm.address"
                        placeholder="Enter complete address" required minlength="5"
                        title="Address must be at least 5 characters long" />
                </div>
                <div class="mb-3">
                    <label for="edit-pincode" class="form-label">Pin code</label>
                    <input type="text" class="form-control" id="edit-pincode" v-model="editLotForm.pincode"
                        placeholder="Enter 6-digit pincode" required minlength="6" maxlength="6" pattern="\d{6}"
                        title="Pincode must be a 6-digit number" />
                </div>
                <div class="mb-3">
                    <label for="edit-price" class="form-label">Price (per hour)</label>
                    <input type="number" class="form-control" id="edit-price" v-model="editLotForm.price"
                        placeholder="Enter price per hour" step="0.01" min="0.01" required
                        title="Price must be greater than 0" />
                </div>
                <div class="mb-3">
                    <label for="edit-spots" class="form-label">Maximum spots</label>
                    <input type="number" class="form-control" id="edit-spots" v-model="editLotForm.spots"
                        placeholder="Enter maximum spots" required min="1" title="Spot count must be greater than 0" />
                </div>
                <div class="d-grid gap-2 mt-4">
                    <button type="submit" class="btn btn-success">Update</button>
                    <button type="button" class="btn btn-outline-secondary"
                        @click="showEditLotModal = false">Cancel</button>
                </div>
            </form>
        </Modal>

        <Modal v-model="showSpotsModal" :title="`Parking Lot: ${selectedLot?.prime_location_name}`" size="xl" no-footer
            centered>
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
                            <p><strong>Price per Hour:</strong> ₹{{ selectedLot?.price?.toFixed(2) }}</p>
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
                            <p><strong>Parking Time:</strong> {{
                                formatDateTime(selectedSpot?.reservation?.parking_timestamp) }}</p>
                            <p><strong>Hours Parked:</strong> {{ selectedSpot?.reservation.hours_parked?.toFixed(2) }}
                                hours</p>
                            <p><strong>Estimated Cost:</strong> ₹{{ selectedSpot?.reservation.estimated_cost?.toFixed(2)
                                }}</p>
                        </div>
                    </div>
                </div>
            </div>
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
const userName = ref('');
const parkingLots = ref([]);
const showAddLotModal = ref(false);
const showEditLotModal = ref(false);
const showdeleteLotModal = ref(false);
const showSpotsModal = ref(false);
const showSpotDetailsModal = ref(false);
const selectedLot = ref(null);
const spotDetails = ref([]);
const selectedSpot = ref(null);

const lotForm = ref({
    location: '',
    address: '',
    pincode: '',
    price: '',
    spots: ''
});

const editLotForm = ref({
    id: null,
    location: '',
    address: '',
    pincode: '',
    price: '',
    spots: ''
});

onMounted(() => {
    userName.value = localStorage.getItem('name') || 'Admin';
    fetchParkingLots();
});

const fetchParkingLots = async () => {
    try {
        const response = await fetch(`${API_BASE}/admin/dash`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const data = await response.json();

        if (response.ok) {
            parkingLots.value = data.parking_lots;
        } else {
            create({ title: data.message || 'Failed to fetch parking lots', variant: 'danger' });
        }
    } catch (error) {
        create({ title: 'Error fetching parking lots', variant: 'danger' });
    }
};

const addLot = async () => {
    try {
        const response = await fetch(`${API_BASE}/admin/add_lot`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                prime_location_name: lotForm.value.location,
                address: lotForm.value.address,
                pin_code: lotForm.value.pincode,
                price: parseFloat(lotForm.value.price),
                maximum_number_of_spots: parseInt(lotForm.value.spots)
            })
        });

        const data = await response.json();

        if (response.ok) {
            create({ title: data.message, variant: 'success' });
            showAddLotModal.value = false;
            lotForm.value = { location: '', address: '', pincode: '', price: '', spots: '' };
            await fetchParkingLots();
        } else {
            create({ title: data.message || 'Failed to add parking lot', variant: 'danger' });
        }
    } catch (error) {
        create({ title: 'Error adding parking lot', variant: 'danger' });
    }
};

const editLot = (lot) => {
    editLotForm.value = {
        id: lot.id,
        location: lot.prime_location_name,
        address: lot.address,
        pincode: lot.pin_code,
        price: lot.price,
        spots: lot.maximum_number_of_spots
    };
    showEditLotModal.value = true;
};

const updateLot = async () => {
    try {
        const response = await fetch(`${API_BASE}/admin/edit_lot/${editLotForm.value.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                prime_location_name: editLotForm.value.location,
                address: editLotForm.value.address,
                pin_code: editLotForm.value.pincode,
                price: parseFloat(editLotForm.value.price),
                maximum_number_of_spots: parseInt(editLotForm.value.spots)
            })
        });

        const data = await response.json();

        if (response.ok) {
            create({ title: data.message, variant: 'success' });
            showEditLotModal.value = false;
            await fetchParkingLots();
        } else {
            create({ title: data.error || 'Failed to update parking lot', variant: 'danger' });
        }
    } catch (error) {
        create({ title: 'Error updating parking lot', variant: 'danger' });
    }
};

const deleteLot = async (lotId) => {
    try {
        const response = await fetch(`${API_BASE}/admin/delete_lot/${lotId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        const data = await response.json();

        if (response.ok) {
            create({ title: data.message, variant: 'success' });
            await fetchParkingLots();
        } else {
            create({ title: data.message || 'Failed to delete parking lot', variant: 'danger' });
        }
    } catch (error) {
        create({ title: 'Error deleting parking lot', variant: 'danger' });
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