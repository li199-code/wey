import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'

import App from './App.vue'
import router from './router'

import './index.css'

// axios.defaults.baseURL = import.meta.env.VITE_API_URL
// axios.defaults.baseURL = "http://1.116.161.57:8000"
axios.defaults.baseURL = "http://127.0.0.1:8000"
// axios.defaults.baseURL = 'https://api.wey.jasonleehere.com'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')


