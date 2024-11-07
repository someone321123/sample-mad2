<template>
  <ul id="nav">
  <form style="width:480px" @submit.prevent="submitSearch">
    <input id="ip1" type="text" v-model="query" style="background-color: #885058; margin-top: 15px; margin-right: 2px; padding-left: 0px" placeholder="Search artist/album/keyword">
    <img src="@/assets/SEARCH.png" class="icons" alt="Submit" width="55px" height="55px" style="margin-top: 2px; float:right; cursor: pointer;padding-right:2px" @click="submitSearch">  
  </form>
  </ul>
</template>

<script>
export default {
  name: "SearchBar",
  data() {
    return {
      query: "",
      person: localStorage.getItem('role'),
      username: localStorage.getItem('username')
    };
  },
  methods: {
    async submitSearch() {
      try {
        this.$router.push({
          path: `/${this.person}/${this.username}/search`,
          query: { query: this.query }
        });      } catch (error) {
        console.error('Error searching:', error);
      }
    }
  }
};
</script>


<style>
    @import url("@/assets/style2.css")
</style>

