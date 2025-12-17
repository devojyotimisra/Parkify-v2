import { ref } from 'vue';

const toasts = ref([]);

const remove = (id) => {
    toasts.value = toasts.value.filter(t => t.id !== id);
};

const create = ({ title, body, variant = 'info', timeout = 3000 }) => {
    const id = Date.now() + Math.random();
    toasts.value.push({ id, title, body, variant });

    if (timeout) {
        setTimeout(() => {
            remove(id);
        }, timeout);
    }
};

export function useToast() {
    return {
        toasts,
        create,
        remove
    };
}