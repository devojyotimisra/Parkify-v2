<template>
    <Navbar role-name="user" />
    <main class="container py-4">
        <h1 class="mb-4">Parking History & Analytics</h1>
        <div class="row mb-4">
            <div class="col-md-6 mb-4">
                <div class="card h-100">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">Parking Costs</h5>
                    </div>
                    <div class="card-body">
                        <canvas v-if="hasChartData" ref="costChart"></canvas>
                        <div v-else class="d-flex justify-content-center align-items-center text-muted"
                            style="min-height: 300px">
                            <p class="mb-0">No data found</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-6 mb-4">
                <div class="card h-100">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">Parking Duration</h5>
                    </div>
                    <div class="card-body">
                        <canvas v-if="hasChartData" ref="durationChart"></canvas>
                        <div v-else class="d-flex justify-content-center align-items-center text-muted"
                            style="min-height: 300px">
                            <p class="mb-0">No data found</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0">Parking Records</h5>
            </div>
            <div class="card-body p-0">
                <div v-if="reservations.length > 0" class="table-responsive">
                    <table class="table table-hover table-striped mb-0">
                        <thead>
                            <tr>
                                <th>Lot Name</th>
                                <th>Spot ID</th>
                                <th>Vehicle Number</th>
                                <th>Parking Time</th>
                                <th>Leaving Time</th>
                                <th>Duration</th>
                                <th>Cost</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(res) in reservations" :key="res.id">
                                <td>{{ res.lot_name }}</td>
                                <td>{{ res.spot_id || 'Out of Service' }}</td>
                                <td>{{ res.vehicle_number }}</td>
                                <td>{{ formatDateTime(res.parking_timestamp) }}</td>
                                <td>
                                    <span v-if="res.leaving_timestamp">{{ formatDateTime(res.leaving_timestamp)}}</span>
                                    <span v-else>-</span>
                                </td>
                                <td>
                                    <span v-if="res.duration_hours">{{ res.duration_hours.toFixed(2) }} hours</span>
                                    <span v-else>-</span>
                                </td>
                                <td>
                                    <span v-if="res.total_cost">₹{{ res.total_cost.toFixed(2) }}</span>
                                    <span v-else>-</span>
                                </td>
                                <td>
                                    <span v-if="res.leaving_timestamp" class="badge bg-success">Completed</span>
                                    <button v-else class="btn btn-sm btn-danger"
                                        @click="releaseSpot(res)">Release</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div v-else class="p-4 text-center">
                    <p class="mb-0">No parking history records found.</p>
                </div>
            </div>
        </div>

        <Modal v-model="showReleaseModal" title="Release Parking Spot" no-footer centered>
            <form @submit.prevent="confirmRelease">
                <div class="mb-3">
                    <label for="release_vehicle_number" class="form-label">Vehicle Number</label>
                    <input type="text" class="form-control" id="release_vehicle_number"
                        :value="releaseForm.vehicle_number" disabled readonly />
                </div>
                <div class="mb-3">
                    <label for="parking_time" class="form-label">Parking Time</label>
                    <input type="text" class="form-control" id="parking_time" :value="releaseForm.parking_timestamp"
                        disabled readonly />
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
import Chart from 'chart.js/auto';

const API_BASE = import.meta.env.VITE_API_BASE_URL;

const { create } = useToast();
const reservations = ref([]);
const costChart = ref(null);
const durationChart = ref(null);
const hasChartData = ref(false);
const showReleaseModal = ref(false);
const currentTime = computed(() => new Date());

let costChartInstance = null;
let durationChartInstance = null;

const releaseForm = ref({
    reservation_id: null,
    vehicle_number: '',
    parking_timestamp: '',
    duration_hours: 0,
    total_cost: 0
});

onMounted(() => {
    fetchHistory();
});

const fetchHistory = async () => {
    try {
        const response = await fetch(`${API_BASE}/user/history`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch history');
        }

        const data = await response.json();
        reservations.value = data.history;

        if (data.chart_data) {
            hasChartData.value = data.chart_data.dates && data.chart_data.dates.length > 0;
            setTimeout(() => {
                renderCharts(data.chart_data);
            }, 0);
        }
    } catch (error) {
        create({
            title: error.message || 'Failed to load history',
            variant: 'danger'
        });
    }
};

const renderCharts = (chartData) => {
    if (costChartInstance) costChartInstance.destroy();
    if (durationChartInstance) durationChartInstance.destroy();

    if (costChart.value && chartData.dates.length > 0) {
        costChartInstance = new Chart(costChart.value, {
            type: 'line',
            data: {
                labels: chartData.dates,
                datasets: [{
                    label: 'Cost (₹)',
                    data: chartData.costs,
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.2,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true
            }
        });
    }

    if (durationChart.value && chartData.dates.length > 0) {
        durationChartInstance = new Chart(durationChart.value, {
            type: 'bar',
            data: {
                labels: chartData.dates,
                datasets: [{
                    label: 'Duration (hours)',
                    data: chartData.durations,
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgb(54, 162, 235)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true
            }
        });
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
        await fetchHistory();
    } catch (error) {
        console.error('Error releasing spot:', error);
        create({ title: error.message || 'Failed to release spot', variant: 'danger' });
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