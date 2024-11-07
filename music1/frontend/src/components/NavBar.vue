<template>
<section id="header" v-if="person === 'Creator' || person === 'User'">
    <img id="prof" src='@/assets/CREATORP.png' width="70px" height="70px">
    <h2 style="margin:0">{{  username }}</h2>
    <button @click='logout' style="font-size: medium; padding:10px; border-radius: 10px; margin: 5px">Logout</button>
    <router-link to="/"><h2 style="margin:0px;background-color: #a2aebe;color:#032641;">Main</h2></router-link>
    <img id="logo" src='@/assets/Crescendo.png' width="240px" height="100px" style="margin:0px">
    <ul id="nav" style="display:flex">
      <SearchBar/>
      <li>
        <router-link :to="`/${person}/${username}/home`"><img class="icons" src='@/assets/HOME.png' width="55px" height="50px"></router-link>
      </li>
      <li v-if="person === 'Creator'">
        <router-link :to="'/creator/' + username + '/adds'"><img class="icons" src='@/assets/ADD.png' width="50px" height="50px"></router-link>
      </li>
      <li v-if="person === 'User'">
        <router-link :to="'/user/' + username + '/upgrade'"><img class="icons" src='@/assets/UPGRADE.png' width="50px" height="50px"></router-link>
      </li>
      <li>
        <router-link :to="`/${person}/${username}/favourites`"><img class="icons" src='@/assets/FAVOURITES.png' width="50px" height="50px"></router-link>
      </li>
      <li>
        <router-link :to="`/${person}/${username}/playlists`"><img class="icons" src='@/assets/PLAYLISTS.png' width="50px" height="50px"></router-link>
      </li>
      </ul>
    </section>
    <section id="header" v-if="person === 'Admin'" style="width:2000px; margin:0px">   
      <img id="prof" src='@/assets/CREATORP.png' width="70px" height="70px" style="margin-left:170px">
    <h2 style="margin:0; margin-left: 20px; background-color:#a2aebe; color: #032641;">ADMIN</h2>
    <button @click='logout' style="font-size: medium; padding:10px; border-radius: 10px; margin: 5px; margin-left:20px">Logout</button>
    <router-link to="/"><h2 style="margin:0px;margin-left: 20px;background-color: #a2aebe;color:#032641;">Main</h2></router-link>
    <img id="logo" src='@/assets/Crescendo.png' width="240px" height="100px" style="margin:0px; margin-left:30px">   
    <router-link to="/admin/dashboard"><h2 style="margin:0px;margin-left: 20px;background-color: #55718b;color:#032641;">Dashboard</h2></router-link>
    <router-link to="/admin/statistics"><h2 style="margin:0px;margin-left: 20px;background-color: #a2aebe;color:#032641;">App Stats</h2></router-link>


</section>

</template>

<script>
import SearchBar from './SearchBar.vue';

export default{
    components: {
      SearchBar
    },
    data() {
    return {
      person: localStorage.getItem('role'),
      username: localStorage.getItem('username'),
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('auth-token')
      localStorage.removeItem('role')
      localStorage.removeItem('id')
      localStorage.removeItem('username')
      this.$router.push({ path: '/' })
    },
  },
}
</script>

<style>
    @import url("@/assets/style2.css")
</style>
