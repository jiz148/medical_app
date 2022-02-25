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
            <label for="password" class="form-label">Enter a New Password</label>
            <input type="password" class="form-control" id="password" v-model="password" placeholder="Enter password">
        </div>
        <div class="mb-3">
          <label for="password2" class="form-label">Confirm Password</label>
          <input type="password" class="form-control" id="password2" v-model="password2" placeholder="Re-type password">
        </div>
        <button id="submitBut" class="btn btn-danger" type="submit" @click="newpass">Change Password</button>
        <button id="cancelBut" class="btn btn-outline-danger" type="submit" @click="cancel">Cancel</button>
    </div>
  </div>
</template>

<script>
export default { //controls form input
    name: 'NewPassPage',
    props: {
        token: String
    },
    data() {
        return {
            query: "",
            message: "AI Interal Medicine searches a large database to diagnose you. To start simply enter your symptoms and answer the questions the app asks you.",
            password: "",
            password2: "",
            showError: false,
            errorMess: "",
            response: {},
            tok: "",
            status: 0
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
          this.response = data; //update table with new data
          if(this.status == 200) {
              if(this.response.accepted == null) {
                  this.$router.push('/');
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
    methods: {
        newpass() { //keeps track of which database to query
            this.tok = this.$route.query.token;
            if(this.password.length < 8) {
                this.errorMess = "Please input a password with at least 8 characters.";
                this.showError = true;
            } else if(this.password != this.password2) {
                this.errorMess = "The passwords do not match.";
                this.showError = true;
            } else {//should also sanitize input for sql injection, but we can worry about that later
                this.showError = false;
                this.performQuery();
            }
        },
        performQuery() {
            document.getElementById("submitBut").disabled = true; //stop queries from happening
            let url = "http://127.0.0.1:5001/user/change_password";
            fetch(url, { //executes the query with a promise to get around asynchronous javascript behavior
                method: 'PUT',
                credentials: "include",
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json;charset=UTF-8',
                    "Set-Cookie": "test=value; Path=/; Secure; SameSite=None;",
                    'Access-Control-Allow-Origin': '127.0.0.1:5001',
                    'Access-Control-Allow-Credentials': true,
                },
                body:  JSON.stringify({
                    'token': this.tok,
                    'new_password': this.password
                })
                })
                .then((response) => { 
                    this.status = response.status;
                    return response.json() 
                })
                .then(data => {
                    this.response = data; 
                    if(this.status == 200) {
                        this.$router.push('/login?msg=Password successfully changed.');
                    } else {
                        this.errorMess = this.response.msg;
                        this.showError = true;
                    }
                    }).catch(error => {
                    if(error.response) {
                        var status = error.response.status;
                        if(status == 404) {
                            this.errorMess = error.response.data.msg;
                            this.showError = true;
                        }
                    }
                    document.getElementById("submitBut").disabled = false; //allow queries to start again
                    this.password = "";
                });
        },
        cancel() {
            this.$router.push('/login');
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
  #cancelBut {
      margin-top: 0.51em;
  }
</style>
