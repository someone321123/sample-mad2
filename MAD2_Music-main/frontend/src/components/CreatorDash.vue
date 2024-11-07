<template>
    <div>
      <NavBar :person="person" :username="username" />
      <br clear="all">
      <div id="parent">
        <div id="genre">
          <h2 style="margin-left: 40px; background-color: #55718b;">MY SONGS</h2>
          <br>
          <table style='float:none; padding:0px'>
            <tr v-for="song in songs" :key="song.SID">
              <td><h3 style="margin-left:0px; margin-right:2px">{{ song.Salb }}</h3></td>
              <td><h3>{{ song.Sname }}</h3></td>
              <td><input type="button" id="ip2" style="background-color: #55718b" value="Delete Song" @click="deleteSong(song.SID)"></td>
              <td>
                    <div style="float:left">
              <RatingsComp :sid="song.SID" :ratingsInfo="ratings_dict[song.SID]" />
                    </div>
              </td>
            </tr>
          </table>
        </div>
          <div>
            <router-link :to="`/creator/${username}/adds`"><h3 style="background-color: #ac797c;">ADD NEW SONG</h3></router-link>
          </div>
        </div>
      </div>
  </template>
  
  <script>
  import NavBar from './NavBar.vue'; 
  import RatingsComp from './RatingsComp.vue'; 
  import axios from 'axios';
  
  export default {
    components: {
      NavBar,
      RatingsComp
    },
    data() {
      return {
        username: localStorage.getItem('username'), 
        songs: [],
        album_list: [],
        ratings_dict: {},
        all:[]
      };
    },
    mounted() {
      this.fetchSongs();
        },
    methods: {
      async fetchSongs() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/get-songs',{
          params: {
            arg: null, 
            type:'all'
          }
        });
          this.all = response.data.data;
          console.log(this.all)
          this.all.forEach(song => {
            console.log(song.Sartist)
                if (song.Sartist === this.username) {
            console.log('NAME', song.Sartist)
            this.songs.push(song);
            this.album_list.push(song.Salb);
                    }
            });
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      },
      async deleteSong(SID) {
      try {
        const response = await axios.post('http://127.0.0.1:5000/delete-song', { id: SID });
        alert(response.data.message);
        this.$router.push({path: `/creator/${this.username}/home`})
      } catch (error) {
        alert('Error deleting song');
      }
    }
    }
  };
  </script>
  
  <style>
    @import url("@/assets/style2.css");
  </style>
  