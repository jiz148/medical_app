<template>
  <div id="register">
    <div id="error" class="card" v-show="showError">
      <div class="card-body">
        {{ errorMess }}
      </div>
    </div>
    <div id="formElements">
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input type="email" class="form-control" id="email" v-model="email" placeholder="Enter email">
      </div>
        <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input type="text" class="form-control" id="username" v-model="username" placeholder="Enter username">
        </div>
        <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" class="form-control" id="password" v-model="password" placeholder="Enter password">
        </div>
        <div class="mb-3">
          <label for="password2" class="form-label">Confirm Password</label>
          <input type="password" class="form-control" id="password2" v-model="password2" placeholder="Re-type password">
        </div>
        <div class="mb-3" id="yeardiv">
          <label for="year" class="form-label">Birth Year</label>
          <input type="number" class="form-control" id="year" v-model="year" placeholder="Enter the year you were born">
       </div>
       <label class="form-check-label" id="genderlabel" for="gendergroup">Gender</label>
       <div id="gendergroup">
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="male" id="male" value="male" v-model="gender">
          <label class="form-check-label" for="male">Male</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="female" id="female" value="female" v-model="gender">
          <label class="form-check-label" for="female">Female</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="other" id="other" value="other" v-model="gender">
          <label class="form-check-label" for="other">Other</label>
        </div>
       </div>
       <div class="mb-3">
        <label for="phone" class="form-label">Phone Number (Optional)</label>
        <input type="text" class="form-control" id="phone" v-model="phone" placeholder="Enter your phone number">
      </div>
        <button id="submitBut" class="btn btn-primary" type="submit" @click="register">Register</button>
        <button id="backBut" class="btn btn-secondary" type="submit" @click="$router.go(-1)">Cancel</button>
    </div>
  </div>
</template>

<script>
  export default { //controls form input
    name: "RegisterPage",
    props: {},
    data() {
        return {
            query: "",
            username: "",
            password: "",
            password2: "",
            email: "",
            year: null,
            gender: null,
            phone: "",
            showError: false,
            errorMess: "",
            response: {},
            switchpage: false,
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
              console.log(this.response);
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
      register() { //keeps track of which database to query
        this.showError = false;
        var re =  /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/; // eslint-disable-line
        var ph = /^[2-9]\d{2}[2-9]\d{2}\d{4}$/; // eslint-disable-line
        var today = new Date();
        var yyyy = today.getFullYear();
        let phtest = true
        if(this.phone != "") {
          phtest = ph.test(this.phone.replace(/\D/g, ""))
        }
        if(!re.test(this.email)) {
            this.errorMess = "Please input a valid email.";
            this.showError = true;
        } else if(this.username == "") {
            this.errorMess = "Please input a username.";
            this.showError = true;
        } else if(this.password.length < 8) {
          console.log("sanity check");
            this.errorMess = "Your password must have a minimum of 8 characters.";
            this.showError = true;
        } else if(this.password != this.password2) {
            this.errorMess = "The passwords do not match.";
            this.showError = true;
        }  else if(this.year < yyyy-120 || this.year > yyyy) {
            this.errorMess = "Please input a valid year.";
            this.showError = true;
        } else if(yyyy - this.year < 16) {
            this.errorMess = "You must be at least 16 years old to register.";
            this.showError = true;
        } else if(this.gender == null) {
            this.errorMess = "Please select your gender.";
            this.showError = true;
        } else if(this.phone != "" && !phtest) {
          this.errorMess = "Invalid phone number.";
          this.showError = true;
        } else { //should also sanitize input for sql injection, but we can worry about that later
            this.showError = false;
            this.performQuery();
        }
      },
      performQuery() {
        document.getElementById("submitBut").disabled = true; //stop queries from happening
        var url = "http://127.0.0.1:5001/user/register";
        let data = {
            'email': this.email,
            'username': this.username,
            'password': this.password,
            'birth_year': this.year,
            'gender': this.gender
          }
        if(this.phone != null) {
          data['phone'] = this.phone;
        }
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
                body:  JSON.stringify(data)
                })
                .then((response) => { 
                    this.status = response.status;
                    return response.json() 
                })
                .then(data => {
                    this.response = data; 
                    if(this.status == 201) {
                      this.$router.push('/login');
                    } else {
                      this.errorMess = this.response.msg;
                      this.showError = true;
                    }
                    }).catch(error => {
                    if(error.response) {
                      if(this.status == 409) {
                        this.errorMess = error.response.data.msg;
                        this.showError = true;
                      }
                    }
                    document.getElementById("submitBut").disabled = false; //allow queries to start again
                    this.username = "";
                    this.password = "";
                    this.password2 = "";
                    this.email = "";
                    this.year = null;
                    this.gender = "male";
                    this.phone = "";
                });
          document.getElementById("submitBut").disabled = false; //allow queries to start again
      }
    }
  }
</script>

<style>
  #error {
    color: rgb(255, 10, 67);
    margin-top: 0.2em;
    margin-bottom: 0.2em;
    margin-left: 0.6em;
    margin-right: 0.6em;
  }
  #formElements {
    margin-top: 0.3em;
    margin-left: 0.6em;
  }
  #submitBut {
    margin-top: 0.5em;
  }
  #gendergroup {
    margin-bottom:0.6em;
    margin-left: 0.2em;
  }
  #year {
    margin-bottom: -0.2em;
  }
  #backBut {
    margin-top: 0.3em;
  }
</style>