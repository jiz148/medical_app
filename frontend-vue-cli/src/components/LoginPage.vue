<template>
  <div id="login">
    <div id="appinfo" class="card"> 
      <div class="card-body">
        {{ message }} 
      </div>
    </div>
    <div id="error" class="card" v-show="showError">
      <div class="card-body">
        {{ errorMess }}
      </div>
    </div>
    <div id="formElements">
        <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input type="text" class="form-control" id="username" v-model="username" placeholder="Enter username">
        </div>
        <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" class="form-control" id="password" v-model="password" placeholder="Enter password">
        </div>
        <button id="submitBut" class="btn btn-primary" type="submit" @click="loginInfo">Login</button>
        <button id="registerBut" class="btn btn-danger" type="submit" @click="godisclaimer" >Register</button>
        <br>
        <button id="forgetBut" class="btn btn-outline-primary" type="submit" @click="forgotpass">Forgot Password?</button>
    </div>
  </div>
</template>

<script>
export default { //controls form input
    name: 'LoginPage',
    props: {},
    data() {
        return {
            query: "",
            message: "AI Interal Medicine searches a large database to diagnose you. To start simply enter your symptoms and answer the questions the app asks you.",
            username: "",
            password: "",
            showError: false,
            errorMess: "",
            response: {}
        }
    },
    methods: {
        loginInfo() { //keeps track of which database to query
            console.log("logging in");
            if(this.password == "") { 
                this.errorMess = "Please input a password.";
                this.showError = true;
            } else if(this.username == "") {
                this.errorMess = "Please input a username.";
                this.showError = true;
            } else { //should also sanitize input for sql injection, but we can worry about that later
                this.showError = false;
                this.performQuery();
            }
        },
        performQuery() {
            document.getElementById("submitBut").disabled = true; //stop queries from happening
            //var url = "/login";
            let url = "http://127.0.0.1:5001/users/login";
            //url += "?username=" + this.username;
            //url += "?password=" + this.password; 
            this.axios //executes the query with a promise to get around asynchronous javascript behavior
                .post(url,{
                'username': this.username, 
                'password': this.password, 
                }, {
                    headers: {
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Access-Control-Allow-Origin': '*',
                }
                })
                .then(response => {
                this.response = response.data; //update table with new data
                console.log(this.response);
                if(this.response.success == 0) {
                    this.errorMess = this.response.msg;
                    this.showError = true;
                } else {
                    console.log(this.response.msg); //switch to main page here
                    this.$router.push('/main');
                }
                }).catch(error => {
                if(error.response) {
                    console.log("Error: " + error.message);
                }
                document.getElementById("submitBut").disabled = false; //allow queries to start again
                this.username = "";
                this.password = "";
                });
            document.getElementById("submitBut").disabled = false; //allow queries to start again
        },
        toggleMessage() {
            this.show = !this.show;
        },
        godisclaimer() {
            this.$router.push('/register');
        },
        async forgotpass() {
            //should query backend to get password based on username
            let url = "http://127.0.0.1:5001/users/forgot";
            let data = { 'username': this.username };
            let pass = "";
            let email = "";
            let success = false;
            await this.axios
                .post(url, data, {
                    headers: {
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Access-Control-Allow-Origin': '*',
                }
                }).then(response => {
                    if(response.data.success == 1) {
                        pass = response.data.password;
                        email = response.data.email;
                        success = true;
                    } else {
                        this.errorMess = response.data.msg;
                        this.showError = true;
                    }
                }).catch(error => {
                    if(error.response) {
                        console.log("Error: " + error.message);
                    }
                });
            if(success) {
                //send email to user with updated data
                data = [pass, email];
            }
        }
    }
}
</script>

<style>
  #appinfo {
    margin-top: 0.4em;
    margin-bottom: 0.4em;
    margin-left: 0.6em;
    margin-right: 0.6em;
    font-size: 14px;
    font-weight: normal;
  }
  #error {
    color: rgb(255, 10, 67);
    margin-top: 0.2em;
    margin-bottom: 0.2em;
    margin-left: 0.6em;
    margin-right: 0.6em;
  }
  #formElements {
    margin-left: 0.6em;
    margin-right: 0.6em;
  }
  #submitBut {
      margin-right: 0.4em;
  }
  #registerBut {
      margin-top: 0.51em;
  }
  #forgetBut {
      margin-top: 0.5em;
  }
</style>
