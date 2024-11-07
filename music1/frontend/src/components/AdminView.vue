<template>
    <div>
      <NavBar :person="person" :username="username" />
      <br clear="all">
      <div id="parent" style="padding: 20px; margin-left: 100px">
        <h2 style="float: left; background-color: rgb(85, 113, 139);">GENRE -> {{ genre }}:</h2>
        <br clear="all">
        <div style="margin-left: 0px; width:1300px">
          <div v-for="song in songs" :key="song.SID">
            <div> 
              <h3 style="margin-right:0; margin-left:0; margin-top: 35px;">{{ song.Sname }} -{{ song.Sartist }}</h3>
            </div>
            <div style="float:right; margin-top: 10px;width:900px">
              <audio controls :id="song.SID" style="float:left; margin-top: 10px;" @play="handlePlay(song.Sname, song.Sartist)">
                      <source :src="getUrl(song.Sname,song.Sartist)" type="audio/mp3">
              </audio>
              <input type="button" id="ip2" style="background-color: #55718b; margin: 15px;align-self: center;" value="Delete Song" @click="deleteSong(song.SID)">
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
  import axios from 'axios'; 
  
  export default {
    name:"GenreComp",
    components: {
      NavBar
    },
    data() {
      return {
        spec:'',
        cat:'',
        username: localStorage.getItem('username'), 
        songs: [], 
        ratings_dict: {}
      };
    },
    mounted() {
      this.fetchSongs(); 
    },
    methods:{
        async fetchSongs() {
  try {
    console.log(this.prop,this.cat)
    const response = await axios.get('http://127.0.0.1:5000/get-songs', {
      params: {
        arg: this.prop,
        type: this.cat
      }
    });
    this.songs = response.data;
  } catch (error) {
    console.error('Error fetching songs:', error);
  }
},
      async getUrl(sname,artist) {
      try {
        const response = await fetch(`media/${sname} -${artist}.mp3`);
        if (!response.ok) {
          throw new Error('Failed to fetch audio source');
        }
        const audioUrl = await response.url();
        return audioUrl;
      } catch (error) {
        console.error('Error fetching audio source:', error);
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
    },
    created() {
      this.prop = this.$route.params.spec;
      this.cat = this.$route.params.category;
    }
  };
  </script>
  
  <style> 
  h3 {
    display: inline-block;
  }
  @import url("@/assets/style2.css");
  </style>
  