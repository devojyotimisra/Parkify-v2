<template>
    <Navbar role-name="admin" />
    <main class="container py-4">
        <h1 class="mb-4">Parking History & Analytics</h1>

        <div class="row mb-4">
            <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h6 class="text-muted">Total Revenue</h6>
                        <h3>₹{{ analytics.total_revenue?.toFixed(2) || '0.00' }}</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h6 class="text-muted">Completed Reservations</h6>
                        <h3>{{ analytics.total_completed_reservations || 0 }}</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h6 class="text-muted">Active Reservations</h6>
                        <h3>{{ analytics.active_reservations || 0 }}</h3>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mb-4">
            <div class="col-md-6 mb-4">
                <div class="card h-100">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">Revenue by Parking Lot</h5>
                    </div>
                    <div class="card-body">
                        <canvas v-if="hasRevenueData" ref="revenueChartCanvas"></canvas>
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
                        <h5 class="mb-0">Occupancy by Parking Lot</h5>
                    </div>
                    <div class="card-body">
                        <canvas v-if="hasOccupancyData" ref="occupancyChartCanvas"></canvas>
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
                                <th>Duration (hours)</th>
                                <th>Total Cost</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="res in reservations" :key="res.id">
                                <td>{{ res.lot_name }}</td>
                                <td>{{ res.spot_id || 'Out of Service' }}</td>
                                <td>{{ res.vehicle_number }}</td>
                                <td>{{ formatDateTime(res.parking_timestamp) }}</td>
                                <td>
                                    <span v-if="res.leaving_timestamp">{{ formatDateTime(res.leaving_timestamp) }}</span>
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
                                    <span v-else class="badge bg-danger">Active</span>
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
    </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Navbar from '@/components/Navbar.vue';
import Chart from 'chart.js/auto';
import { useToast } from '@/components/useToast';

const API_BASE = import.meta.env.VITE_API_BASE_URL;

const { create } = useToast();
const reservations = ref([]);
const analytics = ref({});
const revenueChartCanvas = ref(null);
const occupancyChartCanvas = ref(null);
const hasRevenueData = ref(false);
const hasOccupancyData = ref(false);

let revenueChart = null;
let occupancyChart = null;

onMounted(() => {
    fetchHistory();
});

const fetchHistory = async () => {
    try {
        const response = await fetch(`${API_BASE}/admin/history`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            }
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'Failed to fetch history');
        }

        const data = await response.json();
        reservations.value = data.history || [];
        analytics.value = data.analytics || {};

        if (data.chart_data) {
            hasRevenueData.value = data.chart_data.revenue?.labels?.length > 0;
            hasOccupancyData.value = data.chart_data.occupancy?.labels?.length > 0;
            setTimeout(() => {
                createCharts(data.chart_data);
            }, 0);
        }

    } catch (error) {
        console.error('Error fetching history:', error);
        create({ title: error.message || 'Failed to load history data', variant: 'danger' });
    }
};

const createCharts = (chartData) => {
    if (revenueChart) revenueChart.destroy();
    if (occupancyChart) occupancyChart.destroy();

    if (revenueChartCanvas.value && chartData.revenue) {
        revenueChart = new Chart(revenueChartCanvas.value, {
            type: 'bar',
            data: {
                labels: chartData.revenue.labels,
                datasets: [{
                    label: 'Revenue (₹)',
                    data: chartData.revenue.data,
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    if (occupancyChartCanvas.value && chartData.occupancy) {
        occupancyChart = new Chart(occupancyChartCanvas.value, {
            type: 'bar',
            data: {
                labels: chartData.occupancy.labels,
                datasets: [
                    {
                        label: 'Occupied',
                        data: chartData.occupancy.occupied,
                        backgroundColor: 'rgba(255, 99, 132, 0.5)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Available',
                        data: chartData.occupancy.available,
                        backgroundColor: 'rgba(75, 192, 192, 0.5)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    x: {
                        stacked: true,
                    },

                    y: {
                        stacked: true,
                        beginAtZero: true
                    }
                }
            }
        });
    }
};

const formatDateTime = (isoString) => {
    if (!isoString) return '-';
    const date = new Date(isoString);
    return date.toLocaleString('en-IN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
};
</script>