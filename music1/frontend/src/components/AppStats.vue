<template>
    <div>
      <NavBar :person="person" :username="username" />
      <br clear="all">
      <div>
        <h3 style="width: fit-content; margin-left: 100px;">Total Users Registered: {{ us }}</h3>
        <h3 style="width: fit-content; margin-left: 100px;">Total Creators Registered: {{ cr }}</h3>
        <h3 style="width: fit-content; margin-left: 100px;">Total Songs: {{ sgs }}</h3>
      </div>
      <br clear="all">
      <div id="parent" style="margin-left: 40px; margin-right: 0px; display:flex; width: fit-content;">
        <div id="genre">
          <h2 style="margin-left: 30px;">Total Genres: {{ genreListLength }}</h2>
          <br>
        </div>
        <div id="artist">
          <h2 style="margin-left: 30px;">Total Artists: {{ featuredArtistsLength }}</h2>
          <br>
        </div>
        <div id="album">
          <h2 style="margin-left: 30px;">Total Albums: {{ albumListLength }}</h2>
          <br>
        </div>
      </div>
      <br clear="all">
      <div>
        <h2 style="margin-left: 90px; background-color: #a2aebe; color:#032641;">Highest Rated Songs:</h2>
        <br>
        <table>
          <tbody>
            <tr v-for="song in highestRatedSongs" :key="song.SID">
              <td><h3 style="float:left; background-color: #AC797C; margin-left: 70px;color:#032641;">{{ song.SID }}</h3></td>
              <td><h3 style="float:left">{{ song.Sname }} - {{ song.Sartist }}</h3></td>
              <td><h6 style="background-color: #a2aebe;">Average Rating: {{ song.average_rating }}</h6></td>
            </tr>
          </tbody>
        </table>
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
        username: localStorage.getItem('username'),
        us: 0,
        cr: 0,
        sgs: 0,
        genreListLength: 0,
        featuredArtistsLength: 0,
        albumListLength: 0,
        highestRatedSongs: []
      };
    },
    mounted() {
      this.fetchData();
    },
    methods: {
      async fetchData() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/admin-stats');
          const data = response.data;
          this.us = data.us;
          this.cr = data.cr;
          this.sgs = data.sgs;
          this.genreListLength = data.genlen;
          this.featuredArtistsLength = data.artlen;
          this.albumListLength = data.alblen;
          this.highestRatedSongs = data.highest_rated_songs;
          console.log(data)
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      }
    }
  };
  </script>
  
  <style>
  @import url("@/assets/style2.css");
  </style>
  