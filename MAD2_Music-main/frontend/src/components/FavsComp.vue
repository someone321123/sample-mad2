<template>
    <div>
    <NavBar :person="person" :username="username" />
      <br clear="all">
      <div id="parent">
        <h1 style="background-color: #885058;">Favourites (Rated 5STAR):</h1> 
        <router-link :to="`/${person}/${username}/home`">
          <h2 style="background-color: #55718b;">Add New 5 Star ratings</h2>
        </router-link>
        <br clear="all">
        <div id="playlist" style="width:750px; height:110px;padding:0px">
          <br>
          <table>
            <tr v-for="i in songs" :key="i.SID">
              <td>
                <h3 style="float:left; background-color: #55718b;">{{ i.Sname }} - {{ i.Sartist }}</h3>
                <audio controls style="float:left; margin-top: 10px;" @play="handlePlay(i.Sname, i.Sartist)">
                  <source :src="`../assets/Music/${i.Sname} -${i.Sartist}.mp3`" type="audio/mp3">
                </audio>
              </td>
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
  name:"FavouRites",
  components: {
    NavBar
  },
  data() {
    return {
      username: localStorage.getItem('username'), 
      songs: []
    };
  },
  mounted() {
    this.fetchSongs(); 
  },
  methods:{
    async fetchSongs() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/get-favs', {
          params: {
            id: localStorage.getItem('id')
          }
        });
        this.songs = response.data; 
        console.log(response.data)
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
h3 {
  display: inline-block;
}
@import url("@/assets/style2.css");
</style>

<style> 
@import url("@/assets/style2.css")
</style>