import { createApp } from 'vue';
import App from './App.vue';
//import * as Vue from 'vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import * as VueRouter from 'vue-router';
import VueCookies from 'vue3-cookies';
//import VueCsrf from 'vue-csrf';

import routes from './routes';

axios.defaults.withCredentials = true;

const router = new VueRouter.createRouter({history: VueRouter.createWebHashHistory(), routes});

createApp(App).use(VueAxios, axios).use(VueCookies, {
    expireTimes: "30d",
    path: "/",
    domain: "",
    SameSite: "none",
    secure: true
}).use(router).mount('#app');
