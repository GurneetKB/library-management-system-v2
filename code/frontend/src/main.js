import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import PrimeVue from 'primevue/config';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.bundle.js'
import App from './App.vue';
import HomePage from './components/HomePage.vue';
import AllBooks from './components/AllBooks.vue';
import UserSignup from './components/UserSignup.vue';
import UserLogin from './components/UserLogin.vue';
import LibrarianLogin from './components/LibrarianLogin.vue';
import UserDashboard from './components/UserDashboard.vue';
import LibrarianDashboard from './components/LibrarianDashboard.vue';
import AvailaibleSection from './components/AvailaibleSection.vue';
import DeleteBookResource from './components/DeleteBookResource.vue';
import RevokeBookResource from './components/RevokeBookResource.vue';
import FetchLibrarianBooksResource from './components/FetchLibrarianBooksResource.vue';
import BooksIssuedCountResource from './components/BooksIssuedCountResource.vue';
import BooksPerGenreResource from './components/BooksPerGenreResource.vue';
import UpdateBookResource from './components/UpdateBookResource.vue';
import AllocatedByUserResource from './components/AllocatedByUserResource.vue';
import BooksListResource from './components/BooksListResource.vue';
import BookResource from './components/BookResource.vue';
import GenresListResource from './components/GenresListResource.vue';
import UserBooksResource from './components/UserBooksResource.vue';
import AllocateBookResource from './components/AllocateBookResource.vue';
import BooksRequested from './components/BooksRequested.vue';
import AvailaibleBooks from './components/AvailaibleBooks.vue';
import AllocatedBooks from './components/AllocatedBooks.vue';
import AllStats from './components/AllStats.vue';
import StatsSection from './components/StatsSection.vue';
import MyBooks from './components/MyBooks.vue';
import MyBooksRequest from './components/MyBooksRequest.vue';
import UserProfile from './components/UserProfile.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/api/fetch/genre/books', component: AllBooks },
  { path: '/api/usersignup', component: UserSignup},
  { path: '/api/userlogin', component: UserLogin },
  { path: '/api/librarianlogin', component: LibrarianLogin },
  { path: '/user/dashboard', component: UserDashboard },
  { path: '/api/books/delete', component: DeleteBookResource },
  { path: '/api/revoke/book', component: RevokeBookResource },
  { path: '/api/fetch/librarian/books', component: FetchLibrarianBooksResource },
  { path: '/api/books/issued-count', component: BooksIssuedCountResource },
  { path: '/api/books-per-genre', component: BooksPerGenreResource },
  { path: '/api/books/update', component: UpdateBookResource },
  { path: '/api/books/allocated-by-user', component: AllocatedByUserResource },
  { path: '/api/books', component: BooksListResource },
  { path: '/api/books/:book_id', component: BookResource },
  { path: '/api/genres', component: GenresListResource },
  { path: '/api/users/:user_id/books', component: UserBooksResource },
  { path: '/api/books/allocate', component: AllocateBookResource },
  { path: '/librarian/dashboard/availaiblesection', component: AvailaibleSection },
  { path: '/librarian/dashboard', component: LibrarianDashboard },
  { path: '/librarian/dashboard/requestedbooks', component: BooksRequested },
  { path: '/librarian/dashboard/availaiblebook', component: AvailaibleBooks },
  { path: '/librarian/dashboard/allocatedbooks', component: AllocatedBooks },
  { path: '/librarian/dashboard/stats', component: StatsSection },
  { path: '/user/dashboard/all-stats', component: AllStats },
  { path: '/user/dashboard/all-books', component: AllBooks },
  { path: '/user/dashboard/my-books', component: MyBooks },
  { path: '/user/dashboard/my-request', component: MyBooksRequest },
  { path: '/user/profile', component: UserProfile },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});
createApp(App).use(router).use(PrimeVue, { /* options */ }).mount('#app');
