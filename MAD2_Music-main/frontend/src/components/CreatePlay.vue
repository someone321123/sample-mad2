<template>
    <div>
      <NavBar :person="person" :username="username" />
      <br clear="all">
      <div id="parent">
        <h1>Add Songs to New/Existing Playlist:</h1>
        <br clear="all"> 
        <div id="cplay">
            <div>
              <label><b>Playlist Name:</b></label>
              <input type="text" id="ip1" v-model="plname" placeholder="Name of Playlist" required style="margin-left: 5px"/>
            </div>
            <br>
            <div>
              <label><b>Username:</b></label>
              <input type="text" id="ip1" v-model="username" disabled style="margin-left: 5px"/>
            </div>
            <br>
            <div>
              <label style="float:left;"><b>Select Songs:</b></label>
              <br><br><br>
              <ul style="list-style-type: none">
                <li v-for="song in songs" :key="song.SID" style="display: flex; align-items: center;">
                  <input type="checkbox" :id="song.SID" :value="song.SID" v-model="selected" style="float:left">
                  <label :for="song.SID" style="background-color: #55718b; margin-left: 30px">{{ song.Sname }}</label>
                </li>
              </ul>
            </div>
            <br>
            <input type="button" id="ip2" value="Add to Playlist" @click="createPlaylist">
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import NavBar from './NavBar.vue';
  
  export default {
    name: 'CreatePlay',
    components: {
        NavBar
    },
    data() {
      return {
        person: localStorage.getItem('role'),
        username: localStorage.getItem('username'),
        plname: '',
        songs: [],
        selected: [] 
      };
    },
    mounted() {
    this.fetchSongs(); 
  },
  methods:{
    async fetchSongs() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/get-songs', {
          params: {
            arg: null, 
            type: 'all'
          }
        });
        this.songs = response.data; 
      } catch (error) {
        console.error('Error fetching songs:', error);
      }
    },
      async createPlaylist() {
        try {
          const response = await axios.post('http://127.0.0.1:5000/create-playlist', {
            userid: localStorage.getItem('id'),
            plname: this.plname,
            selected: this.selected
          });
          const data = response.data;
          if (response.status === 201) {
            alert(data.message);
            this.$router.push({ path: `/${this.person}/${this.username}/playlists` });
          } else if (response.status === 200) {
            console.log(data.stat);
          } 
        } catch (error) {
          console.error('Error creating playlist:', error);
        }
      }
    }
  };
  </script>

<style scoped>
@import url("@/assets/style2.css");
</style>

  