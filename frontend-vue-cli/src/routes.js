import LoginPage from './components/LoginPage.vue';
import DisclaimerPage from './components/DisclaimerPage.vue';
import RegisterPage from './components/RegisterPage.vue';
import MainPage from './components/MainPage';
import ForgetPage from './components/ForgetPage';
//import NewPassPage from './components/NewPassPage';
import VisitPage from './components/VisitPage';
import ProfilePage from './components/ProfilePage';
//import SettingsPage from './components/SettingsPage';

const routes = [
    {path: '/login', component: LoginPage, props: true},
    {path: '/', component: DisclaimerPage, props: true},
    {path: '/register', component: RegisterPage},
    {path: '/visit', component: VisitPage},
    {path: '/main', component: MainPage},
    {path: '/forget', component: ForgetPage},
    //{path: '/newpass', component: NewPassPage, props: true},
    {path: '/profile', component: ProfilePage},
    //{path: '/settings', component: SettingsPage}
];

export default routes;