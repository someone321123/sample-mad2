const Login = {
    template:`
<div class="overlay">
<div class="row">
    <div class="col-8"></div>
    <div class="col-4"><br><br><br><br><a href="#" class="btn btn-danger">X</a></div>
</div>
    <div class="login">
    <div class="container">
        <h3 align="center">User Login</h3> <br>
        
        
        <form method="POST" action="/login">
            <div class="mb-3">
                <label for="Username" class="form-label">Username</label>
                <input type="text" class="form-control" id="Username" name="Username">
            </div>
            <div class="mb-3">
                <label for="Password" class="form-label">Password</label>
                <input type="password" class="form-control" id="Password" name="Password">
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
      </form>
      <br>
      <p>Don't have an account? <router-link to="/register">Sign Up</router-link></p>
    </div>
</div>
    </div>
    `
};

const Register = {
    template:`
    <div class="overlay">
    <div class="row">
    <div class="col-8"></div>
    <div class="col-4" align=""left><br><a href="#" class="btn btn-danger">X</a></div>
</div>
    <div class="register">
        <div class="container">
          <h3 align="center">User Registration</h3><br>
          <form method="POST" action="/register">
                   

                  <div class="mb-3">
                      <label for="Username" class="form-label">Username</label>
                      <input type="text" class="form-control" id="user_name" name="Username">
                      <!--<div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>-->
                    </div>
                    <div class="mb-3">
                      <label for="Name" class="form-label">Name</label>
                      <input type="text" class="form-control" id="name" name="Name">
                      <!--<div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>-->
                    </div>
                    <div class="mb-3">
                      <label for="Email" class="form-label">Email Address</label>
                      <input type="email" class="form-control" id="e_mail" name="Email">
                      <!--<div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>-->
                    </div>
                    <div class="mb-3">
                      <label for="Password" class="form-label">Password</label>
                      <input type="password" class="form-control" id="pass_word" name="Password">
                    </div>
                    
                    <!--<div class="mb-3 form-check">
                      <input type="checkbox" class="form-check-input" id="exampleCheck1">
                      <label class="form-check-label" for="exampleCheck1">Check me out</label>
                    </div>-->
                    <button type="submit" class="btn btn-primary">Submit</button>
                    <br><br>
                    <p>Already have an account? <router-link to="/login">Login</router-link></p>
            </form>
      </div>
      </div>
      </div>
    `
};



const InvalidLogin = {
    template:`
    <div class="overlay">
    <div class="row">
    <div class="col-8"></div>
    <div class="col-4" align=""left><br><br><br><br><br><br><br><router-link to="/login" class="btn btn-danger">X</router-link></div>
</div>
        <div class="login">
            <div class="container" align="center">
                <h5 style="color: red;">Invalid username or password. Please try again.</h5>
                <br>
                <router-link to="/login" class="btn btn-primary">Try Again</router-link>
            </div>
        </div>
    </div>
    `
};


const ExistingUserName = {
    template:`
    <div class="overlay">
    <div class="row">
    <div class="col-8"></div>
    <div class="col-4" align=""left><br><br><br><br><br><br><br><router-link to="/register" class="btn btn-danger">X</router-link></div>
</div>
        <div class="login">
            <div class="container" align="center">
                <h5 style="color: red;">Username already exists. Please choose a different username.</h5>
                <br>
                <router-link to="/register" class="btn btn-primary">Try Again</router-link>
            </div>
        </div>
    </div>
    `
};


const ExistingEmail = {
    template:`
    <div class="overlay">
    <div class="row">
    <div class="col-8"></div>
    <div class="col-4" align=""left><br><br><br><br><br><br><br><router-link to="/register" class="btn btn-danger">X</router-link></div>
</div>
        <div class="login">
            <div class="container" align="center">
                <h5 style="color: red;">Email already exists. Please use a different email.</h5>
                <br>
                <router-link to="/register" class="btn btn-primary">Try Again</router-link>
            </div>
        </div>
    </div>
    `
};

const routes = [
    { path: '/login', component: Login },
    { path: '/register', component: Register },
    { path: '/invalid-login', component: InvalidLogin },
    { path: '/existing-username', component: ExistingUserName },
    { path: '/existing-email', component: ExistingEmail }
];

const router = new VueRouter({
    routes
});

const app = new Vue({
    el: '#app',
    router
});