<template>
    <div>
        <img src="@/assets/topleft.png" width="250px" height="250px" style="position:fixed; top:0; left:0; margin-left: 0; "> 
        <img src="@/assets/topright.png" width="250px" height="250px" style="position:fixed; top:0; right:0; margin-right: 0; "> 
        <img src="@/assets/bottom left.png" width="250px" height="250px" style="position:fixed; bottom:0; left:0; margin-left: 0; "> 
        <img src="@/assets/bottom right.png" width="250px" height="250px" style="position:fixed; bottom:0; right:0; margin-left: 0; "> 
        
   
<img src="@/assets/Crescendo.png" width="637.5px" height="250px" style="margin-left:450px">
<br clear="all">
<br clear="all">
<div id="parent">
   
<h1>Register as a New User: </h1>
<br clear="all"> 
<div id="cplay">
    <form action="/register/new">
        <div>
        <label><b>Username: </b>
                <input type="text" style="background-color: #55718b;" v-model="uname" class="ip1" minlength="4" required/>
        </label> <br><br>
        <label><b>Email: </b>
                <input type="email" style="background-color: #55718b;" v-model="umail" class="ip1" required/>
        </label> <br><br>
        <label><b>Password: </b>
                <input type="password" style="background-color: #55718b;" v-model="pword" class="ip1" minlength="8" required/>
        </label>
     <br v-if="stat==false">
     <span v-if="stat==false" class="validation-message"><h4>You are already a User/Creator!</h4></span>
     <br clear="all">
     <router-link to="/login/user"><h3 style="float:left">USER/CREATOR LOGIN</h3></router-link>
     
        </div>
        <br clear="all">
        <div>
        <input style="background-color: #55718b;" type="button" id="ip2" value="Register as User" @click="submitForm">
        </div>
        </form>
</div>
</div>
</div>
</template>

<script>
import axios from 'axios';
export default{
    name:'RegisterNew',
    data(){
        return{
                uname: "",
                umail: "",
                pword: "",
                stat: true
        };
    },
    methods:{
        async submitForm() {
    try {
        const response = await axios.post('http://127.0.0.1:5000/api/userapi', {
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
        if (response.status === 201) {
            alert(data.message);
            this.stat=data.stat;
            this.$router.push({ path: '/' })
        } else if (response.status === 200) {
            alert(data.message); 
            this.stat=data.stat;

        } 
    } catch (error) {
        console.error(error);
    }
}
}}
</script>


<style>
label{
    padding-left: 5px;
    padding-right: 5px;
    padding-top: 5px;
    padding-bottom: 10px;
    border-radius: 10px;
    margin-top: 10px;
    margin-bottom: 2px;
    background-color: #885058; 
    border-radius:10px;
    color:#D9D9D9;
    font-size: 25px;
    }
#parent {
    align-content: center;
    margin-left:370px;
    width: 70%;
  }
#ip2{
    color:#D9D9D9;
    font-family: Georgia, 'Times New Roman', Times, serif;
    font-weight: bold;
    font-size: large ;
    text-align: center;
    display: inline;
    margin-bottom:5px;
    align-self: auto;
    border-radius: 18px;
    background: #885058;
    height: 40px;
    width:200px
  }
@import url("@/assets/stylelogin.css")
</style>