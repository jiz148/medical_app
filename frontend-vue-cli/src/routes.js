import LoginPage from './components/LoginPage.vue';
import DisclaimerPage from './components/DisclaimerPage.vue';
import RegisterPage from './components/RegisterPage.vue';
import MainPage from './components/MainPage';

const routes = [
    {path: '/', component: LoginPage},
    {path: '/disclaimer', component: DisclaimerPage},
    {path: '/register', component: RegisterPage},
    {path: '/main', component: MainPage}
];

export default routes;