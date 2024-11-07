<template>
  <div>
    <NavBar :person="person" :username="username" />
    <br clear="all">
    <div id="parent" style="padding: 20px; margin-left: 100px">
      <h2 style="float: left; background-color: rgb(85, 113, 139);">ARTIST -> {{ artist }}:</h2>
      <br clear="all">
      <div style="margin-left: 0px; width:1300px">
        <div v-for="song in songs" :key="song.SID">
          <div> 
            <h3>{{ song.Sname }} -{{ song.Sartist }}</h3>
          </div>
          <div style="float:right; margin-top: 10px; background-color: aqua;">
            <h1>{{ song.Surl }}</h1>
            <audio controls>
              <source :src="require( '@/assets/Music/' + song.Surl )" type="audio/mpeg" />
              Your browser does not support the audio element.
            </audio>
            <div style="float:left">
              <RatingsComp :sid="song.SID" :ratingsInfo="ratings_dict[song.SID]" />
            </div>
          </div>
          <br clear="all">
          <br>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from './NavBar.vue';
import RatingsComp from './RatingsComp.vue'; 
import axios from 'axios'; 

export default {
  name:"ArtistComp",
  components: {
    NavBar,
    RatingsComp
  },
  data() {
    return {
      artist: '', 
      username: localStorage.getItem('username'), 
      songs: [], 
      ratings_dict: {},
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
            arg: this.artist, 
            type: 'artist'
          }
        });
        this.songs = response.data; 
        console.log(response.data, "my super power")
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
  },
  created() {
    this.artist = this.$route.params.artist;
  }
};
</script>

<style> 
h3 {
  display: inline-block;
}
@import url("@/assets/style2.css");
</style>
