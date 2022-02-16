import { createApp } from 'vue';
import App from './App.vue';
//import * as Vue from 'vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import * as VueRouter from 'vue-router';

import routes from './routes';

const router = new VueRouter.createRouter({history: VueRouter.createWebHashHistory(), routes});

createApp(App).use(VueAxios, axios).use(router).mount('#app');
