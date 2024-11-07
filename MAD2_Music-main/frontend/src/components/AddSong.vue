<template>
    <div>
      <NavBar :person="person" :username="username" />
      <br clear="all">
      <div id="parent">
        <h1>Add Song by Creator:</h1>
        <br clear="all"> 
        <div id="cplay">
            <div>
              <label><b>Song Name:</b></label>
              <input type="text" id="ip1" v-model="name" placeholder="Name of Song" required style="margin-left: 5px"/>
            </div>
            <br>
            <div>
              <label><b>Song File:</b></label>
              <input type="file" id="ip1" placeholder="Upload .MP3 File" required style="margin-left: 5px; padding-bottom:15px" @change="handleEventListener"/>
            </div>
            <!-- <br>
            <div>
              <label><b>Artist:</b></label>
              <input type="text" id="ip1" v-model="username" style="margin-left: 5px"/>
            </div> -->
            <br>
            <div>
              <label style="float:left;"><b>Select Album:</b></label>
              <br><br><br>
              <ul style="list-style-type: none">
                <li v-for="alb in album_list" :key="alb" style="display: flex; align-items: center;">
                        <input type="radio" :value="alb" v-model="album">
                        <label :for="alb" style="background-color: #55718b; margin-left: 30px">{{ alb }}</label>
                </li>
              </ul>
            </div>
            <br>
            <div>
              <label style="float:left;"><b>Select Genre:</b></label>
              <br><br><br>
              <ul style="list-style-type: none">
                <li v-for="gen in genre_list" :key="gen" style="display: flex; align-items: center;">
                        <input type="radio" :value="gen" v-model="genre">
                        <label :for="gen" style="background-color: #55718b; margin-left: 30px">{{ gen }}</label>
                </li>
              </ul>
            </div>
            <input type="button" id="ip2" value="Add Song" @click="addSong">
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import NavBar from './NavBar.vue';
  
  export default {
    name: 'AddSong',
    components: {
        NavBar
    },
    data() {
      return {
        person: localStorage.getItem('role'),
        username: localStorage.getItem('username'),
        name: '',
        album: '',
        genre: '',
        genre_list: [],
        album_list: [],
        url: ''
      };
    },
    mounted() {
      this.fetchData();
    },
    methods: {
    handleEventListener(event) {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = (e) => {
      this.url = e.target.result;
      };
      reader.readAsDataURL(file);
      },
      async fetchData() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/get-data');
          const data = response.data;
          this.genre_list = data.genre_list;
          this.album_list = data.album_list;
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      },
      async addSong() {
        try {
          const response = await axios.post('http://127.0.0.1:5000/add-song', {
            username: localStorage.getItem('username'),
            name: this.name,
            artist: this.username,
            album: this.album,
            genre: this.genre,
            url: this.url
          });
          const data = response.data;
          if (response.status === 201) {
            alert(data.message);
            this.$router.push({ path: `/${this.person}/${this.username}/dashboard` });
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

  