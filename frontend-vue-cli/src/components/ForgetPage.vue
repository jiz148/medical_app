<template>
  <div id="login">
    <div id="appinfo" class="card"> 
      <div class="card-body">
        {{ message }} 
      </div>
    </div>
    <div id="alertinfo" class="card" v-show="showAlert"> 
      <div class="card-body">
        {{ alert }} 
      </div>
    </div>
    <div id="error" class="card" v-show="showError">
      <div class="card-body">
        {{ errorMess }}
      </div>
    </div>
    <div id="formElements">
        <div class="mb-3">
          <label for="email" class="form-label">Enter Your Email</label>
          <input type="email" class="form-control" id="email" v-model="email" placeholder="Enter your email">
      </div>
        <button id="submitBut" class="btn btn-primary" type="submit" @click="forgetquery">Confirm</button>
        <button id="backBut" class="btn btn-secondary" type="submit" @click="$router.go(-1)">Cancel</button>
    </div>
  </div>
</template>

<script>
export default { //controls form input
    name: 'ForgetPage',
    props: {},
    data() {
        return {
            query: "",
            message: "AI Interal Medicine searches a large database to diagnose you. To start simply enter your symptoms and answer the questions the app asks you.",
            email: "",
            showError: false,
            errorMess: "",
            response: {},
            alert: "",
            showAlert: false,
            status: 0
        }
    },
    beforeCreate: function() {
        let url = "http://jinchispace.com:5001/user/sessiondata";
        fetch(url, { //executes the query with a promise to get around asynchronous javascript behavior
        method: 'get',
        credentials: "include",
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json;charset=UTF-8',
            "Set-Cookie": "test=value; Path=/; Secure; SameSite=None;",
            'Access-Control-Allow-Origin': 'jinchispace.com:5001',
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
        forgetquery() {
            document.getElementById("submitBut").disabled = true; //stop queries from happening
            let url = "http://jinchispace.com:5001/user/forget_password";
            this.showAlert = false;
            this.showError = false;
            fetch(url, { //executes the query with a promise to get around asynchronous javascript behavior
                method: 'POST',
                credentials: "include",
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json;charset=UTF-8',
                    "Set-Cookie": "test=value; Path=/; Secure; SameSite=None;",
                    'Access-Control-Allow-Origin': 'jinchispace.com:5001',
                    'Access-Control-Allow-Credentials': true,
                },
                body:  JSON.stringify({
                  'email': this.email
                })
                })
                .then((response) => { 
                    this.status = response.status;
                    return response.json() 
                })
                .then(data => {
                    this.response = data; 
                    if(this.status == 200) {
                      this.alert = "An email with a password reset link has been sent to " + this.email + ". If you do not see the email check you spam folder as well.";
                      this.showAlert = true;
                    } else {
                      this.errorMess = this.response.msg;
                      this.showError = true;
                    }
                    }).catch(error => {
                    if(error.response) {
                        if(this.status == 401 || this.status == 500) {
                            this.errorMess = error.response.data.msg;
                            this.showError = true;
                        }
                    }
                    document.getElementById("submitBut").disabled = false; //allow queries to start again
                });
            document.getElementById("submitBut").disabled = false; //allow queries to start again
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
  #backBut {
    margin-top: 0.3em;
  }
</style>
