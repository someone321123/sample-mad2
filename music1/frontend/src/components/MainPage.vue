<template>
<!DOCTYPE html>
<html>
    <img src="@/assets/topleft.png" width="250px" height="250px" style="position:fixed; top:0; left:0; margin-left: 0; "> 
        <img src="@/assets/topright.png" width="250px" height="250px" style="position:fixed; top:0; right:0; margin-right: 0; "> 
        <img src="@/assets/bottom left.png" width="250px" height="250px" style="position:fixed; bottom:0; left:0; margin-left: 0; "> 
        <img src="@/assets/bottom right.png" width="250px" height="250px" style="position:fixed; bottom:0; right:0; margin-left: 0; "> 
        
   
<img src="@/assets/Crescendo.png" width="637.5px" height="250px">
<br clear="all">
<body>
        <div id="login">
<h1 style="margin-left: 130px;">Welcome to Crescende Music!</h1></div>
<br clear="all">
<div id="login">
        <router-link to="/login/user"><h1 style="float:left; background-color: #885058;">Login as User/Creator</h1></router-link>
        <router-link to='/login/admin'><h1 style="float:left; background-color: #885058;">Login As Admin</h1></router-link>
</div>
<br clear="all">
<div id="login">
        <router-link to="/register/new"><h1 style="margin-left: 170px;">Register as New User!</h1></router-link>
</div>
</body>
</html>
</template>

<script>
    export default {
      name: 'MainPage'
    }
    </script>
    
   
<style scoped>
    @import url("@/assets/stylelogin.css")
</style>
    