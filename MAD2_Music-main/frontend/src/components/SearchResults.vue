<template>
<NavBar :person="person" :username="username" />
<br clear="all">
<div id="parent">
    <div id="genre" style="display:block">
<h2 style="margin-left: 30px;">Search Results for "{{query}}":</h2>
<br>
<br>
<table style="padding:0px">
<tr v-for="i in results['album']" :key="i">
    <td><h3 style="background-color: #55718b"> {{ i.Salb }} - {{ i.Sgenre }}</h3></td>
    <td><h3>{{ i.Sname }} - {{ i.Sartist }}</h3></td>
    <td><audio controls><source src="http://localhost:8080/static/Music/{{i.Sname}} -{{i.Sartist}}.mp3" type="audio/mp3"></audio></td>
</tr>
<tr v-for="i in results['genre']" :key="i">
    <td><h3 style="background-color: #55718b"> {{ i.Salb }} - {{ i.Sgenre }}</h3></td>
    <td><h3>{{ i.Sname }} - {{ i.Sartist }}</h3></td>
    <td><audio controls><source src="http://localhost:8080/static/Music/{{i.Sname}} -{{i.Sartist}}.mp3" type="audio/mp3"></audio></td>
</tr>
<tr v-for="i in results['artist']" :key="i">
    <td><h3 style="background-color: #55718b"> {{ i.Salb }} - {{ i.Sgenre }}</h3></td>
    <td><h3>{{ i.Sname }} - {{ i.Sartist }}</h3></td>
    <td><audio controls><source src="http://localhost:8080/static/Music/{{i.Sname}} -{{i.Sartist}}.mp3" type="audio/mp3"></audio></td>
</tr>
<tr v-for="i in results['song']" :key="i">
    <td><h3 style="background-color: #55718b"> {{ i.Salb }} - {{ i.Sgenre }}</h3></td>
    <td><h3>{{ i.Sname }} - {{ i.Sartist }}</h3></td>
    <td><audio controls><source src="http://localhost:8080/static/Music/{{i.Sname}} -{{i.Sartist}}.mp3" type="audio/mp3"></audio></td>
</tr>
</table>
</div>

</div>
</template>


<script>
import NavBar from './NavBar.vue'; 
import axios from 'axios';

export default {
  name: "SearchResults",
  components: {
    NavBar
  },
  data() {
    return {
      person: localStorage.getItem('role'),
      username: localStorage.getItem('username'), 
      query: "",
      results: {}
    };
  },
  mounted() {
    this.fetchSearchResults();
  },
  methods: {
    async fetchSearchResults() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/search', {
          params: {
            query: this.query
          }
        });
        this.results = response.data.results;
        console.log(this.results['genre'])
      } catch (error) {
        console.error('Error fetching search results:', error);
      }
    },
    getAudioSource(item) {
      return `http://localhost:8080/static/Music/${item.Sname} - ${item.Sartist}.mp3`;
    }
  },
  created() {
    this.query = this.$route.query.query;
  }
};
</script>

<style>
  @import url("@/assets/style2.css");
</style>
  