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
        <button id="submitBut" class="btn btn-success" type="submit" @click="forgetquery">Confirm</button>
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
            showAlert: false
        }
    },
    methods: {
        forgetquery() {
            document.getElementById("submitBut").disabled = true; //stop queries from happening
            //var url = "/login";
            let url = "http://127.0.0.1:5001/user/forget_password";
            //url += "?username=" + this.username;
            //url += "?password=" + this.password; 
            this.showAlert = false;
            this.showError = false;
            this.axios //executes the query with a promise to get around asynchronous javascript behavior
                .post(url,{
                'email': this.email
                }, {
                    headers: {
                    'Content-Type': 'application/json;charset=UTF-8',
                    'Access-Control-Allow-Origin': '*',
                }
                })
                .then(response => {
                this.response = response.data; //update table with new data
                var status = response.status;
                console.log(this.response);
                if(status == 200) {
                    console.log(this.response.msg); //switch to main page here
                    //this.$router.push('/login');
                   this. alert = "An email with a password reset link has been sent to " + this.email + ". If you do not see the email check you spam folder as well.";
                    this.showAlert = true;
                } else {
                    this.errorMess = this.response.msg;
                    this.showError = true;
                }
                }).catch(error => {
                if(error.response) {
                    console.log("Error: " + error.message);
                    var status = error.response.status;
                    if(status == 401 || status == 500) {
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
</style>
