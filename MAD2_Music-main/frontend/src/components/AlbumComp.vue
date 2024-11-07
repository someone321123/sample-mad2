<template>
  <div>
    <NavBar :person="person" :username="username" />
    <br clear="all">
    <div id="parent" style="padding: 20px; margin-left: 100px">
      <h2 style="float: left; background-color: rgb(85, 113, 139)">ALBUM -> {{ album }}:</h2>
      <br clear="all">
      <div style="margin-left: 0px; width:1300px">
        <div v-for="song in data" :key="song">
          <div> 
            <h3>{{ song.Sname }} -{{ song.Sartist }}</h3>
          </div>
          <div style="float:right; margin-top: 10px;">
            <audio controls>        
              <source :src="song.Surl" type="audio/mp3">   
            </audio>        
            <audio controls>
              <source src="@/assets/Music/Song_1712329117-6628a4.mp3" type="audio/mp3">
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
  name:"AlbumComp",
  components: {
    NavBar,
    RatingsComp
  },
  data() {
    return {
      album: '', 
      username: localStorage.getItem('username'), 
      ratings_dict: {},
      data: []
    };
  },
  async mounted() {
   await this.fetchSongs();
  },
  methods:{
    async fetchSongs() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/get-songs', {
          params: {
            arg: this.album, 
            type: 'album'
          }
        });
        this.data = response.data;
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
    this.album = this.$route.params.album;
  }
};
</script>

<style> 
h3 {
  display: inline-block;
}
@import url("@/assets/style2.css");
</style>
