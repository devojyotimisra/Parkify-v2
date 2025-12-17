import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

const app = createApp(App);
app.use(router);

const originalFetch = window.fetch;
window.fetch = async (...args) => {
    const response = await originalFetch(...args);

    if (response.status === 401) {
        localStorage.clear();
        router.replace('/notallowed');
        return response;
    }

    if (response.status === 403) {
        router.push('/notallowed');
        return response;
    }

    if (response.status === 404) {
        router.push('/notfound');
        return response;
    }

    const newToken = response.headers.get('x-refresh-token');
    if (newToken) {
        localStorage.setItem('token', newToken);
    }
    return response;
};

app.mount('#app');