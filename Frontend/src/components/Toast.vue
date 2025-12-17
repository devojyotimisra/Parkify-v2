<template>
    <div class="position-fixed top-0 end-0 p-3 pe-none mt-5" style="z-index: 9999">
        <TransitionGroup name="toast">
            <div v-for="toast in toasts" :key="toast.id"
                :class="['alert p-2 d-flex mt-2 align-items-center pe-auto', getVariantClass(toast.variant)]"
                role="alert" style="min-width: 125px; max-width: 500px">
                <span class="small flex-grow-1 pe-2">{{ toast.title }}</span>
                <button type="button" class="btn-close py-2" @click="remove(toast.id)" aria-label="Close"></button>
            </div>
        </TransitionGroup>
    </div>
</template>

<script setup>
import { useToast } from '@/components/useToast';

const { toasts, remove } = useToast();

const getVariantClass = (variant) => {
    switch (variant) {
        case 'success': return 'alert-success';
        case 'danger': return 'alert-danger';
        case 'warning': return 'alert-warning';
        case 'info': return 'alert-info';
        default: return 'alert-primary';
    }
};
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
    transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
    opacity: 0;
}
</style>