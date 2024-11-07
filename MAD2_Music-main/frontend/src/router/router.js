import {createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'
import MainPage from '../components/MainPage.vue'
import AdminDash from '../components/AdminDash.vue'
import GenreComp from '../components/GenreComp.vue'
import AlbumComp from '../components/AlbumComp.vue'
import ArtistComp from '../components/ArtistComp.vue'
import FavsComp from '../components/FavsComp.vue'
import PlayLists from '../components/PlayLists.vue'
import CreatePlay from '../components/CreatePlay.vue'
import UserUpgrade from '../components/UserUpgrade.vue'
import AddSong from '../components/AddSong.vue'
import CreatorDash from '../components/CreatorDash.vue'
import SearchResults from '../components/SearchResults.vue'
import AdminView from '../components/AdminView.vue'
import AppStats from '../components/AppStats.vue'
import LoginUser from '../views/LoginUser.vue'
import LoginAdmin from '../views/LoginAdmin.vue'
import RegisterNew from '../views/RegisterNew.vue'


const routes = [
  {
    path: '/:role/:username/home',
    name: 'home',
    component: HomePage,
    props: true
  },
  {
    path: '/login/user',
    name: 'loginu',
    component: LoginUser
  },
  {
    path: '/login/admin',
    name: 'logina',
    component: LoginAdmin
  },
  {
    path: '/',
    name: 'main',
    component: MainPage
  },
  {
    path: '/register/new',
    name: 'register',
    component: RegisterNew
  },
  {
    path: '/admin/dashboard',
    name: 'admindash',
    component: AdminDash
  },
  {
    path: '/:role/:username/genre/:genre',
    name: 'genres',
    component: GenreComp,
    props: true
  },
  {
    path: '/:role/:username/album/:album',
    name: 'albums',
    component: AlbumComp,
    props: true
  },
  {
    path: '/:role/:username/artist/:artist',
    name: 'artists',
    component: ArtistComp,
    props: true
  },
  {
    path: '/:role/:username/favourites',
    name: 'favourites',
    component: FavsComp,
    props: true
  },
  {
    path: '/:role/:username/playlists',
    name: 'playlists',
    component: PlayLists,
    props: true
  },
  {
    path: '/:role/:username/create/playlist',
    name: 'createplay',
    component: CreatePlay,
    props: true
  },
  {
    path: '/:role/:username/upgrade',
    name: 'userupgrade',
    component: UserUpgrade,
    props: true
  },
  {
    path: '/:role/:username/adds',
    name: 'addsong',
    component: AddSong,
    props: true
  },
  {
    path: '/:role/:username/dashboard',
    name: 'creatordash',
    component: CreatorDash,
    props: true
  },
  {
    path: '/:role/:username/search',
    name: 'searchresults',
    component: SearchResults,
    props: true
  },
  {
    path: '/admin/:category/:spec',
    name: 'adminview',
    component: AdminView,
    props: true
  },
  {
    path: '/admin/statistics',
    name: 'appstats',
    component: AppStats,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (['/', '/register/new', '/login/user', '/login/admin'].includes(to.path)){
    next();
  }
  else if (to.name!=="loginu" && !localStorage.getItem('auth-token') ? true : false){
    console.log('IN LOGIN USER')
    next({ path: '/login/user' });
  }
  else {
    next();
  }
} 
);

export default router

