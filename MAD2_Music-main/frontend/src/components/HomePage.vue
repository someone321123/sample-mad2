<template>
    <div>
      <NavBar :person="person" :username="username" />
      <div>
        <a v-if="person === 'Creator'" :href="`/creator/${username}/dashboard`">
          <h3 style="background-color: #AC797C;color: #032641; margin-left: 320px;width:fit-content">CREATOR DASHBOARD</h3>
        </a>
        <br clear="all">
        <div id="parent" style="margin-left: 300px;">
          <div id="genre">
            <h2 style="background-color: #55718b;">GENRES</h2>
            <div v-for="(gen, index) in genre_list" :key="index">
              <router-link :to="`/${person}/${username}/genre/${gen}`" type="button"><h3>{{ gen }}</h3></router-link>
            </div>
          </div>
          <div id="artist">
            <h2 style="background-color: #55718b;">ARTISTS</h2>
            <div v-for="(art, index) in featured_artists" :key="index">
              <router-link :to="`/${person}/${username}/artist/${art}`" type="button"><h3>{{ art }}</h3></router-link>
            </div>
          </div>
          <div id="album">
            <h2 style="background-color: #55718b;">ALBUMS</h2>
            <div v-for="(alb, index) in album_list" :key="index">
              <router-link :to="`/${person}/${username}/album/${alb}`" type="button"><h3>{{ alb }}</h3></router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import NavBar from './NavBar.vue';
  import axios from 'axios';
  
  export default {
    name: 'HomePage',
    components: {
      NavBar
    },
    data() {
      return {
        person: '',
        username: '',
        genre_list: [],
        album_list: [],
        featured_artists: []
      };
    },
    mounted() {
      this.fetchData();
    },
    methods: {
      async fetchData() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/get-data');
          const data = response.data;
          console.log(data)
          this.person = localStorage.getItem('role');
          this.username = localStorage.getItem('username');
          this.genre_list = data.genre_list;
          this.album_list = data.album_list;
          this.featured_artists = data.featured_artists;
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  @import url("@/assets/style2.css");
  </style>
  