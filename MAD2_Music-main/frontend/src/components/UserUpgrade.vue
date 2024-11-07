<template>
    <div>
        <NavBar :person="person" :username="username" />
    <br clear="all">
<div id="parent">
   
<h1>Upgrade from User to Creator: </h1>
<br clear="all"> 
<div id="cplay">
        <div>
        <label><b>Username: </b>
        <input type="text" name="uname" id="ip1" v-model=username /></label>
        </div>
        <br>
        <br>
        <div>
        <input style="background-color: #55718b;" type="button" id="ip2" value="Upgrade to Creator" @click="upgradeToCreator">
        </div>
        <br>
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
      };
    },
  methods:{
      async upgradeToCreator() {
        try {
          const response = await axios.post('http://127.0.0.1:5000/user-upgrade', {
            id: localStorage.getItem('id')
          });
          const data = response.data;
          if (response.status === 201) {
            alert(data.message);
            this.$router.push({ path: '/login/user' });
          } else if (response.status === 200) {
            console.log(data.stat);
          } 
        } catch (error) {
          console.error('Error upgrading to creator:', error);
        }
      }
    }
  };
  </script>

<style scoped>
@import url("@/assets/style2.css");
</style>

  