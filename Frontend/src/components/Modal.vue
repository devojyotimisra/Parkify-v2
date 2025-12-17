<template>
    <Teleport to="body">
        <Transition name="fade">
            <div v-if="modelValue" class="modal-backdrop show"></div>
        </Transition>
        <Transition name="fade">
            <div v-if="modelValue" class="modal d-block" tabindex="-1" role="dialog" aria-modal="true"
                @click.self="close">
                <div class="modal-dialog" :class="[getSizeClass(), { 'modal-dialog-centered': centered }]">
                    <div class="modal-content">
                        <div class="modal-header" :class="headerBgVariant ? `bg-${headerBgVariant} text-white` : ''">
                            <h5 class="modal-title">{{ title }}</h5>
                            <button type="button" class="btn-close" :class="{ 'btn-close-white': headerBgVariant }"
                                @click="close" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <slot></slot>
                        </div>
                        <div v-if="!noFooter" class="modal-footer">
                            <button type="button" class="btn btn-secondary" @click="close">{{ cancelTitle }}</button>
                            <button type="button" class="btn" :class="`btn-${okVariant}`" @click="handleOk">{{ okTitle }}</button>
                        </div>
                    </div>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<script setup>
const props = defineProps({
    modelValue: {
        type: Boolean,
        required: true
    },
    title: {
        type: String,
        default: ''
    },
    size: {
        type: String,
        default: ''
    },
    centered: {
        type: Boolean,
        default: false
    },
    noFooter: {
        type: Boolean,
        default: false
    },
    headerBgVariant: {
        type: String,
        default: ''
    },
    okTitle: {
        type: String,
        default: 'OK'
    },
    okVariant: {
        type: String,
        default: 'primary'
    },
    cancelTitle: {
        type: String,
        default: 'Cancel'
    }
});

const emit = defineEmits(['update:modelValue', 'ok', 'cancel']);

const close = () => {
    emit('update:modelValue', false);
    emit('cancel');
};

const handleOk = () => {
    emit('ok');
    close();
};

const getSizeClass = () => {
    switch (props.size) {
        case 'sm': return 'modal-sm';
        case 'lg': return 'modal-lg';
        case 'xl': return 'modal-xl';
        default: return '';
    }
};
</script>


<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.1s linear;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>