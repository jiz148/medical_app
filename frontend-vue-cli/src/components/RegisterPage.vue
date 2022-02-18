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
        <div class="mb-3">
          <label for="year" class="form-label">Birth Year</label>
          <input type="number" class="form-control" id="year" v-model="year" placeholder="Enter the year you were born">
       </div>
       <div class="mb-3">
        <label for="phone" class="form-label">Phone Number (Optional)</label>
        <input type="text" class="form-control" id="phone" v-model="phone" placeholder="Enter your phone number">
      </div>
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
        <button id="submitBut" class="btn btn-primary" type="submit" @click="register">Register</button>
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
            gender: "male",
            phone: "",
            showError: false,
            errorMess: "",
            response: {},
            switchpage: false
        }
    },
    methods: {
      register() { //keeps track of which database to query
        console.log("registering info");
        var re =  /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/; // eslint-disable-line
        var ph = /^[2-9]\d{2}[2-9]\d{2}\d{4}$/; // eslint-disable-line
        if(this.phone != "") {
          this.phone = this.phone.replace(/\D/g, "");
          if(!ph.test(this.phone)) {
            this.errorMess = "Invalid phone number.";
            this.showError = true;
            return;
          }
        }
        console.log(this.password);
        console.log(this.password.length);
        //console.log(this.password.value);
        if(this.password.length < 8) {
          console.log("sanity check");
            this.errorMess = "Please input a password with at least 8 characters.";
            this.showError = true;
        } else if(this.password != this.password2) {
            this.errorMess = "The passwords do not match.";
            this.showError = true;
        } else if(this.username == "") {
            this.errorMess = "Please input a username.";
            this.showError = true;
        //} else if(this.email == "") {
        } else if(!re.test(this.email)) {
            this.errorMess = "Please input a valid email.";
            this.showError = true;
        } else if(this.year < 1000 || this.year > 9999) {
            this.errorMess = "Please input a valid year.";
            this.showError = true;
        } else { //should also sanitize input for sql injection, but we can worry about that later
            this.showError = false;
            /*if(this.phone != null) {
              let ind = this.phone.indexof('-');
              if(this.phone.indexof('-') > -1) {
                let temp = this.phone.substring(0,ind);
                let ind2 = this.phone.substring(ind+1, this.phone.length).indexof('-') + ind + 1;
                temp += this.phone.substring(ind+1, ind2) + this.phone.substring(ind2+1, this.phone.length);
                this.phone = temp;
              } 
            }*/
            
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
        console.log(data);
        this.axios //executes the query with a promise to get around asynchronous javascript behavior
          .post(url, data,
          {
            headers: {
              'Content-Type': 'application/json;charset=UTF-8',
              'Access-Control-Allow-Origin': '*',
            }
          })
          .then(response => {
            this.response = response.data; //update table with new data
            console.log(response);
            var status = response.status;
            if(status == 201) {
              console.log(this.response.msg); //switch to main page here
              this.$router.push('/login');
            } else {
              this.errorMess = this.response.msg;
              this.showError = true;
            }
          }).catch(error => {
            if(error.response) {
              console.log("Error: " + error.message);
              var status = error.response.status;
              if(status == 409) {
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
</style>