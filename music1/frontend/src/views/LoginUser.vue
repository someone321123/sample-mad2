<template>
    <div>
   <img src="@/assets/topleft.png" width="250px" height="250px" style="position:fixed; top:0; left:0; margin-left: 0; "> 
    <img src="@/assets/topright.png" width="250px" height="250px" style="position:fixed; top:0; right:0; margin-right: 0; "> 
    <img src="@/assets/bottom left.png" width="250px" height="250px" style="position:fixed; bottom:0; left:0; margin-left: 0; "> 
    <img src="@/assets/bottom right.png" width="250px" height="250px" style="position:fixed; bottom:0; right:0; margin-left: 0; "> 
    <img src="@/assets/Crescendo.png" width="300px" height="125px" style="margin-left: 600px;"><br clear="all"> 
          
            <div id="login"><h1 style="background-color: #885058;">USER LOGIN PAGE</h1> </div>

<br clear="all">
<div id="login">
            <div id="hl"> 
                <h1 style="background-color: #55718b;">Username: 
                    <input class="ip1" type="text" v-model="uname" placeholder="Registered Username" required>
            </h1><br clear="all">
            <h1 style="background-color: #55718b;">Email: 
                <input class="ip1" type="email" v-model="umail" placeholder="Registered Email" required>
        </h1><br clear="all">
            <h1 style="background-color: #55718b;">Password:
                 <input class="ip1" type="password" v-model="pword" placeholder="Password" required></h1><br clear="all"></div>
            <br>
        <br>
            <button class="subm" type="button" @click="loginForm">LOGIN</button>
            <router-link to="/login/admin"><h3 style="float:left">ADMIN LOGIN</h3></router-link>
            <router-link to="/"><h3 style="background-color: #55718b;">MAIN PAGE</h3></router-link>

</div>
</div>
</template>
  
<script>
import axios from 'axios';

export default {
    name: 'LoginUser',
    data(){
      return{
                uname: "",
                umail: "",
                pword: "",
                stat: true
        };
    },
    methods:{
        async loginForm() {
    try {
        const response = await axios.post('http://127.0.0.1:5000/login-user', {
            "username": this.uname,
            "password": this.pword,
            "email": this.umail,
        }, {
            headers: {
                'Content-Type': 'application/json',
                Accept: 'application/json',
            },
        });
        const data = response.data;
        console.log('Data',data)
        if (response.status === 201) {
            alert(data.message);
         } 
        else if (response.status === 401) {
            alert(data.message);
        }
        else if (response.status === 404) {
            alert(data.message); 
        }
        else if (response.status === 200) {
            if (data.token){
            localStorage.setItem('auth-token', data.token)
            localStorage.setItem('username', data.username)
            localStorage.setItem('id', data.id)
            localStorage.setItem('role', data.role)
            console.log('SUCCESS')
            this.$router.push({path: `/${data.role}/${data.username}/home`})
        }
         else {
            alert('User undefined')
         }  
        } 
    } catch (error) {
        alert(error);
    }
}
}}
  </script>
  
<style>
  @import url("@/assets/stylelogin.css")
</style>
