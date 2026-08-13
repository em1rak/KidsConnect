import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/font.css'
import './assets/styles.css'

const app = createApp(App)

app.use(router)
app.mount('#app')
