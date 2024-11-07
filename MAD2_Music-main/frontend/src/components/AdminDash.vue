<template>
    <div>
    <NavBar :person="person" :username="username" />
      <br clear="all">
      <div id="parent" style="margin-left: 40px; margin-right: 0px; display:flex;width: fit-content;">
  
        <div id="genre">
          <h2 style="margin-left: 90px;">GENRES: </h2>
          <br>
          <table style="float:left; padding-right:30px">
            <tr v-for="g in genre_list" :key="g">
              <td><h3 style="background-color: #55718b;">{{ g }}</h3></td>
              <td><router-link :to="`/admin/genre/${g}`"><h3 style="background-color: #a2aebe; color:#032641">VIEW GENRE</h3></router-link></td>
            </tr>
          </table>
        </div>
  
        <div id="artist">
          <h2 style="margin-left: 90px;">ARTISTS: </h2>
          <br>
          <table style="float:left; padding-right:30px">
            <tr v-for="i in featured_artists" :key="i">
              <td><h3 style="background-color: #55718b;">{{ i }}</h3></td>
              <td><router-link :to="`/admin/artist/${i}`"><h3 style="background-color: #a2aebe; color:#032641">VIEW ARTIST</h3></router-link></td>
            </tr>
          </table>
        </div>
  
        <div id="album">
          <h2 style="margin-left: 90px;">ALBUMS: </h2>
          <br>
          <table style="float:left">
            <tr v-for="a in album_list" :key="a">
              <td><h3 style="background-color: #55718b;">{{ a }}</h3></td>
              <td><router-link :to="`/admin/view/album/${a}`"><h3 style="background-color: #a2aebe; color:#032641">VIEW ALBUM</h3></router-link></td>
            </tr>
          </table>
        </div>
  
      </div>
    </div>
  </template>
  
  <script>
  import NavBar from './NavBar.vue'; 
  import axios from 'axios';

  export default {
    components: {
      NavBar
    },
    data() {
      return {
        person: localStorage.getItem('role'),
        genre_list: [], 
        featured_artists: [], 
        album_list: [] 
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
  
  <style>
    @import url("@/assets/style2.css")
  </style>
  