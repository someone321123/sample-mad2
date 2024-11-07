<template>
  <div>
 <img src="@/assets/topleft.png" width="250px" height="250px" style="position:fixed; top:0; left:0; margin-left: 0; "> 
  <img src="@/assets/topright.png" width="250px" height="250px" style="position:fixed; top:0; right:0; margin-right: 0; "> 
  <img src="@/assets/bottom left.png" width="250px" height="250px" style="position:fixed; bottom:0; left:0; margin-left: 0; "> 
  <img src="@/assets/bottom right.png" width="250px" height="250px" style="position:fixed; bottom:0; right:0; margin-left: 0; "> 
  <img src="@/assets/Crescendo.png" width="300px" height="125px" style="margin-left: 600px;"><br clear="all"> 
        
<div id="login"><h1 style="background-color: #885058;">ADMIN LOGIN PAGE</h1> </div>
<br clear="all">
<div id="login">
          <div id="hl"> 
              <h1 style="background-color: #55718b;">Name: 
                  <input class="ip1" type="text" v-model="name" required disabled/>
          </h1><br clear="all">
          <h1 style="background-color: #55718b;">Password: 
              <input class="ip1" type="password" v-model="pword" placeholder="Password" required>
      </h1><br clear="all">
          <h1 style="background-color: #55718b;">Token:
               <input class="ip1" type="password" v-model="adm_token" placeholder="Token" required></h1><br clear="all"></div>
          <br>
      <div id="login" v-if="stat==false">
      <h3 v-if="stat==false" class="validation-message">INVALID CREDENTIALS: Please check username/password</h3>
      </div>
      <br>
          <button class="subm" type="button" @click="loginAdmin">LOGIN</button>
          <router-link to="/login/user"><h3 style="float:left">USER/CREATOR LOGIN</h3></router-link>
          <router-link to="/"><h3>MAIN PAGE</h3></router-link>
</div>
</div>
</template>
   
<script>
import axios from 'axios';

export default {
    name: 'LoginAdmin',
    data(){
      return{
                name: "Admin",
                pword: "",
                adm_token: "",
                stat: true
        };
    },
    methods:{
        async loginAdmin() {
    try {
        const response = await axios.post('http://127.0.0.1:5000/login-admin', {
            "password": this.pword,
            "adm_token": this.adm_token,
        }, {
            headers: {
                'Content-Type': 'application/json',
                Accept: 'application/json',
            },
        });
        const data = response.data;
        if (response.status === 201) {
            alert(data.message);
            this.stat=data.stat;
            console.log(data.stat)
        } else if (response.status === 200) {
            this.stat=data.stat;
            console.log(data.stat)
            localStorage.setItem('auth-token', data.token)
            localStorage.setItem('username', data.username)
            localStorage.setItem('id', data.id)
            localStorage.setItem('role', data.role)
            this.$router.push({path: '/admin/dashboard'})
        } 
        else if (response.status === 404) {
            alert(data.message); 
        }
        console.log(data)
    } catch (error) {
        alert(error);
    }
}
}}
  </script>
   
<style>
    @import url("@/assets/stylelogin.css")
</style>
   