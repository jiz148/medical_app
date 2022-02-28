import { createApp } from 'vue';
import App from './App.vue';
import 'jquery/src/jquery.js'
import "bootstrap/dist/css/bootstrap.min.css";
import 'bootstrap/dist/js/bootstrap.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css'
import * as VueRouter from 'vue-router';

import routes from './routes';

const router = new VueRouter.createRouter({history: VueRouter.createWebHashHistory(), routes});

createApp(App).use(router).mount('#app');
