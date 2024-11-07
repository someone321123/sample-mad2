<template>
  <div>
    <NavBar :person="person" :username="username" />
    <br clear="all">
    <div id="parent">
      <h1 style="background-color: #885058;">All Playlists:</h1> 
      <router-link :to="`/${person}/${username}/create/playlist`">
        <h2 style="background-color: #55718b;">Add Songs/Create Playlists</h2>
      </router-link>
      <br clear="all">
      <div id="playlist">
        <br>
        <template v-for="(songs, playlistName) in playlist" :key="playlistName">
          <h2 style="align-content:start; background-color: #55718b;">{{ playlistName }}</h2>
          <br>
          <table>
            <tbody>
              <tr v-for="song in songs" :key="song.SID">
                <td><h3>{{ song.Sname }} - {{ song.Sartist }}</h3></td>
                <td>
                  <audio controls @play="handlePlay(song.Sname, song.Sartist)">
                    <source :src="`../assets/Music/${song.Sname} - ${song.Sartist}.mp3`" type="audio/mp3">
                  </audio>
                </td>
              </tr>
            </tbody>
          </table>
          <br>
          <br>
        </template>
      </div>
    </div>
  </div>
</template>

  
  <script>
  import NavBar from './NavBar.vue';
  import axios from 'axios'; 
  
  export default {
    name:"PlayLists",
    components: {
      NavBar
    },
    data() {
      return {
        username: localStorage.getItem('username'), 
        playlist: {}
      };
    },
    mounted() {
      this.fetchSongs(); 
    },
    methods:{
      async fetchSongs() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/get-plays', {
            params: {
              id: localStorage.getItem('id')
            }
          });
          this.person = localStorage.getItem('role');
          this.playlist = response.data.playlists; 
        } catch (error) {
          console.error('Error fetching songs:', error);
        }
      },
      handlePlay(selectedSongName, selectedSongArtist) {
          this.songs.forEach(song => {
            if (song.Sname !== selectedSongName || song.Sartist !== selectedSongArtist) {
              const audioElement = document.getElementById(`${song.SID}`);
              if (audioElement) {
                audioElement.pause();
              }
            }
          });
        }
    }
  };
  
  </script>

<style>
    @import url("@/assets/style2.css")
</style>