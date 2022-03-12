<template>
  <div id="login">
    <div id="appinfo" class="card"> 
      <div class="card-body">
        {{ message }} 
      </div>
    </div>
    <div id="alert" class="card" v-show="showAlert">
      <div class="card-body">
        {{ alertMess }}
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
        <button id="submitBut" class="btn btn-primary btn-lg" type="submit" @click="loginInfo">Login</button>
        <br>
        <button id="registerBut" class="btn btn-link btn-sm" type="submit" @click="godisclaimer" >Create Account</button>
        <button id="forgetBut" class="btn btn-link btn-sm" type="submit" @click="forgotpass">Forgot Password?</button>
    </div>
  </div>
</template>

<script>
export default { //controls form input
    name: 'LoginPage',
    props: {
        msg: String
    },
    data() {
        return {
            query: "",
            message: "AI Interal Medicine searches a large database to diagnose you. To start simply enter your symptoms and answer the questions the app asks you.",
            username: "",
            password: "",
            showError: false,
            errorMess: "",
            response: {},
            alertMess: "",
            showAlert: false,
            status: 0,
        }
    },
    beforeCreate: function() {
        let url = "http://127.0.0.1:5001/user/sessiondata";
        fetch(url, { //executes the query with a promise to get around asynchronous javascript behavior
        method: 'get',
        credentials: "include",
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json;charset=UTF-8',
            "Set-Cookie": "test=value; Path=/; Secure; SameSite=None;",
            'Access-Control-Allow-Origin': '127.0.0.1:5001',
            'Access-Control-Allow-Credentials': true,
        }})
        .then((response) => { 
            this.status = response.status;
            return response.json() 
        })
        .then(data => {
          console.log(this.status);
          this.response = data; //update table with new data
          if(this.status == 200) {
              if(this.response.accepted == null) {
                  this.$router.push('/');
              } else if(this.response.uid != null) {
                  this.$router.push('/visit');
              }
          }
        }).catch(error => {
        if(error.response) {
            if(this.status == 200) {
              console.log(this.response.msg); //switch to main page here
            } else {
              this.$router.push('/');
            }
        }
        });
    },
    created: function() {
        this.alertMess = this.$route.query.msg;
        if(this.alertMess) {
            this.showAlert = true;
        }
    },
    methods: {
        loginInfo() { //keeps track of which database to query
            this.showError = false;
            this.showAlert = false;
            if(this.username == "") { 
                this.errorMess = "Please input a username.";
                this.showError = true;
            } else if(this.password == "") {
                this.errorMess = "Please input a password.";
                this.showError = true;
            } else { //should also sanitize input for sql injection, but we can worry about that later
                this.showError = false;
                this.performQuery();
            }
        },
        performQuery() {
            document.getElementById("submitBut").disabled = true; //stop queries from happening
            let url = "http://127.0.0.1:5001/user/login";
            fetch(url, { //executes the query with a promise to get around asynchronous javascript behavior
                method: 'POST',
                credentials: "include",
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json;charset=UTF-8',
                    "Set-Cookie": "test=value; Path=/; Secure; SameSite=None;",
                    'Access-Control-Allow-Origin': '127.0.0.1:5001',
                    'Access-Control-Allow-Credentials': true,
                },
                body:  JSON.stringify({
                    'username': this.username, 
                    'password': this.password
                })
                })
                .then((response) => { 
                    this.status = response.status;
                    return response.json() 
                })
                .then(data => {
                    this.response = data; 
                    if(this.status == 200) {
                        this.$router.push('/visit');
                    } else {
                        this.errorMess = this.response.msg;
                        this.showError = true;
                    }
                    }).catch(error => {
                    if(error.response) {
                        console.log("Error: " + error.message);
                        if(this.status == 401) {
                            this.errorMess = error.response.data.msg;
                            this.showError = true;
                        }
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
        forgotpass() {
            this.$router.push('/forget');
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
  #alert {
    color: rgb(40, 190, 90);
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
      margin-bottom: 0.2em
  }
  #registerBut {
      margin-top: 2em;
      margin-left: -0.6em;
      margin-right: 0.4em;
  }
  #forgetBut {
      margin-left: -0.6em;
  }
</style>
