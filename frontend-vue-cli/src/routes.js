import LoginPage from './components/LoginPage.vue';
import DisclaimerPage from './components/DisclaimerPage.vue';
import RegisterPage from './components/RegisterPage.vue';
import MainPage from './components/MainPage';
import ForgetPage from './components/ForgetPage';
import NewPassPage from './components/NewPassPage';

const routes = [
    {path: '/login', component: LoginPage, props: true},
    {path: '/', component: DisclaimerPage},
    {path: '/register', component: RegisterPage},
    {path: '/main', component: MainPage},
    {path: '/forget', component: ForgetPage},
    {path: '/newpass', component: NewPassPage, props: true}
];

export default routes;