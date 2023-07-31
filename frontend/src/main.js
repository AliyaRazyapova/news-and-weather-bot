import { createApp } from 'vue'
import App from './App.vue'
import MessageHistory from "@/components/MessageHistory.vue";
import DashboardBot from "@/components/DashboardBot.vue";
import ResponseForm from "@/components/ResponseForm.vue";
import ResponseList from "@/components/ResponseList.vue";
import {createRouter, createWebHistory} from "vue-router";

const routes = [
    { path: '/history', component: MessageHistory },
    { path: '/dashboard', component: DashboardBot },
    { path: '/response', component: ResponseList },
    { path: '/response/:id/edit', component: ResponseForm },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

const app = createApp(App);
app.use(router);
app.mount('#app');
