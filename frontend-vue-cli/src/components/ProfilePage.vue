<template>
  <div id="register">
    <div id="error" class="card" v-show="showError">
      <div class="card-body">
        {{ errorMess }}
      </div>
    </div>
    <div id="formElements">
        <div class="mb-3">
          <label for="email" class="form-label">
            Email
            <button v-if="!emailchange" type="button" class="btn btn-link" @click='emailchange=true'><i class="bi bi-pencil-square"></i></button>
            <button v-if="emailchange" type="button" class="btn btn-link" @click='emailQuery'><i class="bi bi-check-square"></i></button>
            <button v-if="emailchange" type="button" class="btn btn-link" @click='() => {emailchange=false; email = currentVals[0]}'><i class="bi bi-x-square"></i></button>
          </label>
          <input :disabled="!emailchange" type="email" class="form-control" id="email" v-model="email" placeholder="Enter email">
      </div>
        <div class="mb-3">
            <label for="username" class="form-label">
                Username
                <button v-if="!userchange" type="button" class="btn btn-link" @click='userchange=true'><i class="bi bi-pencil-square"></i></button>
                <button v-if="userchange" type="button" class="btn btn-link" @click='userQuery'><i class="bi bi-check-square"></i></button>
                <button v-if="userchange" type="button" class="btn btn-link" @click='() => {userchange=false; username = currentVals[1]}'><i class="bi bi-x-square"></i></button> 
            </label>
            <input :disabled="!userchange" type="text" class="form-control" id="username" v-model="username" placeholder="Enter username">
        </div>
        <div class="mb-3">
            <label for="password" class="form-label">
                Password
                <button v-if="!passchange" type="button" class="btn btn-link" @click='passchange=true'><i class="bi bi-pencil-square"></i></button>
                <button v-if="passchange" type="button" class="btn btn-link" @click='passQuery'><i class="bi bi-check-square"></i></button>
                <button v-if="passchange" type="button" class="btn btn-link" @click='() => {passchange=false; password = currentVals[2]}'><i class="bi bi-x-square"></i></button>
            </label>
            <input :disabled="!passchange" type="password" class="form-control" id="password" v-model="password" placeholder="Enter password">
        </div>
        <div class="mb-3" v-if="passchange">
          <label for="password2" class="form-label">Confirm Password</label>
          <input type="password" class="form-control" id="password2" v-model="password2" placeholder="Re-type password">
        </div>
        <div class="mb-3" id="yeardiv">
          <label for="year" class="form-label">
              Birth Year
              <button v-if="!yearchange" type="button" class="btn btn-link" @click='yearchange=true'><i class="bi bi-pencil-square"></i></button>
              <button v-if="yearchange" type="button" class="btn btn-link" @click='yearQuery'><i class="bi bi-check-square"></i></button>
              <button v-if="yearchange" type="button" class="btn btn-link" @click='() => {yearchange=false; year = currentVals[3]}'><i class="bi bi-x-square"></i></button>
          </label>
          <input :disabled="!yearchange" type="number" class="form-control" id="year" v-model="year" placeholder="Enter the year you were born">
       </div>
       <label class="form-check-label" id="genderlabel" for="gendergroup">
           Sex
           <button v-if="!sexchange" type="button" class="btn btn-link" @click='sexchange=true'><i class="bi bi-pencil-square"></i></button>
           <button v-if="sexchange" type="button" class="btn btn-link" @click='sexQuery'><i class="bi bi-check-square"></i></button>
           <button v-if="sexchange" type="button" class="btn btn-link" @click='() => {sexchange=false; gender = currentVals[4]}'><i class="bi bi-x-square"></i></button>
        </label>
       <div id="gendergroup">
        <div class="form-check form-check-inline">
          <input :disabled="!sexchange" class="form-check-input" type="radio" name="male" id="male" value="male" v-model="gender">
          <label class="form-check-label" for="male">Male</label>
        </div>
        <div class="form-check form-check-inline">
          <input :disabled="!sexchange" class="form-check-input" type="radio" name="female" id="female" value="female" v-model="gender">
          <label class="form-check-label" for="female">Female</label>
        </div>
       </div>
       <div class="mb-3">
        <label for="phone" class="form-label">
            Phone Number
            <button v-if="!numchange" type="button" class="btn btn-link" @click='numchange=true'><i class="bi bi-pencil-square"></i></button>
            <button v-if="numchange" type="button" class="btn btn-link" @click='numQuery'><i class="bi bi-check-square"></i></button>
            <button v-if="numchange" type="button" class="btn btn-link" @click='() => {numchange=false; phone = currentVals[5]}'><i class="bi bi-x-square"></i></button>
        </label>
        <input :disabled="!numchange" type="text" class="form-control" id="phone" v-model="phone" placeholder="Enter your phone number">
      </div>
        <button id="backBut" class="btn btn-secondary" type="submit" @click="$router.go(-1)">Back</button>
    </div>
  </div>
</template>

<script>
  export default { //controls form input
    name: "ProfilePage",
    props: {},
    data() {
        return {
            query: "",
            username: null,
            password: null,
            password2: "",
            email: null,
            year: null,
            gender: null,
            phone: null,
            showError: false,
            errorMess: "",
            response: {},
            status: 0,
            currentVals: null,
            userchange: false,
            passchange: false,
            emailchange: false,
            yearchange: false,
            sexchange: false,
            numchange: false,
            timerlock: 0
        }
    },
    beforeCreate: async function() {
        let url = "http://127.0.0.1:5001/user/sessiondata";
        await fetch(url, { //executes the query with a promise to get around asynchronous javascript behavior
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
                else if(this.response.uid == null) {
                    this.$router.push('/login');
                }
            } else {
                console.log('bad');
                this.$router.push('/');
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
        this.getInfo();
    },
    methods: {
      getInfo: function() {
          //perform query to get user data; for now just use dummy values
          this.username = "user";
          this.password = "password";
          this.email = "ken_erickson@yahoo.com";
          this.year = 2000;
          this.gender = "male";
          this.currentVals = [this.email, this.username, this.password, this.year, this.gender, this.phone];
      },
      emailQuery: function() {
        this.showError = false;
        var re =  /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/; // eslint-disable-line
        if(!re.test(this.email)) {
            this.errorMess = "Please input a valid email.";
            this.showError = true;
            this.email = this.currentVals[0]; //reset email
            this.emailchange = false;
            this.timerlock += 1;
            let lock = this.timerlock;
            setTimeout(() => { 
              if(this.timerlock == lock) {
                this.showError = false
              }
            }, 5000);
        } else if(this.email == this.currentVals[0]) {
            this.emailchange = false; //email did not change so no need to update
        } else {
            //do query
            //need error message for if username is taken (should come from the backend)
        }
      },
      userQuery: function() {
        this.showError = false;
        if(this.username == "" || this.username == null) {
            this.errorMess = "Please input a username.";
            this.showError = true;
            this.username = this.currentVals[1]; //reset
            this.userchange = false;
            this.timerlock += 1;
            let lock = this.timerlock;
            setTimeout(() => { 
              if(this.timerlock == lock) {
                this.showError = false
              }
            }, 5000);
        } else if(this.username == this.currentVals[1]) {
            this.userchange = false; //no change
        } else {
            //query
            //check if username is taken
        }
      },
      passQuery: function() {
        this.showError = false;
        if(this.password.length < 8) {
            this.errorMess = "Your password must have a minimum of 8 characters.";
            this.showError = true;
            this.password = this.currentVals[2]; //reset
            this.password2 = ""; //reset
            this.passchange = false;
            this.timerlock += 1;
            let lock = this.timerlock;
            setTimeout(() => { 
              if(this.timerlock == lock) {
                this.showError = false
              }
            }, 5000);
        } else if(this.password != this.password2) {
            this.errorMess = "The passwords do not match.";
            this.showError = true;
            this.password = this.currentVals[2]; //reset
            this.password2 = ""; //reset
            this.passchange = false;
            this.timerlock += 1;
            let lock = this.timerlock;
            setTimeout(() => { 
              if(this.timerlock == lock) {
                this.showError = false
              }
            }, 5000);
        } else if(this.password == this.currentVals[2]) {
            this.passchange = false; //no change
        } else {
            //do query, shouldn't be any errors from backend here, other than query issues
        }
      },
      yearQuery: function() {
        this.showError = false;
        var today = new Date();
        var yyyy = today.getFullYear();
        if(this.year < yyyy-120 || this.year > yyyy) {
            this.errorMess = "Please input a valid year.";
            this.showError = true;
            this.year = this.currentVals[3]; //reset
            this.yearchange = false;
            this.timerlock += 1;
            let lock = this.timerlock;
            setTimeout(() => { 
              if(this.timerlock == lock) {
                this.showError = false
              }
            }, 5000);
        } else if(yyyy - this.year < 16) {
            this.errorMess = "You must be at least 16 years old to use Medisys.";
            this.showError = true;
            this.year = this.currentVals[3]; //reset
            this.yearchange = false;
            this.timerlock += 1;
            let lock = this.timerlock;
            setTimeout(() => { 
              if(this.timerlock == lock) {
                this.showError = false
              }
            }, 5000);
        } else if(this.year == this.currentVals[3]) {
            this.yearchange = false;
        } else {
            //do query, shouldn't be any backend errors here
        }
      },
      sexQuery: function() {
        this.showError = false;
        if(this.gender == null) { //this shouldn't really happen, but just in case
            this.errorMess = "Please select your sex.";
            this.showError = true;
            this.gender = this.currentVals[4]; //reset
            this.sexchange = false;
            this.timerlock += 1;
            let lock = this.timerlock;
            setTimeout(() => { 
              if(this.timerlock == lock) {
                this.showError = false
              }
            }, 5000);
        } else if(this.gender == this.currentVals[4]) {
            this.sexchange = false;
        } else {
            //do query, shouldn't be any backend errors
        }
      },
      numQuery: function() {
        this.showError = false;
        var ph = /^[2-9]\d{2}[2-9]\d{2}\d{4}$/; // eslint-disable-line
        if(this.phone == this.currentVals[5]) {
            this.numchange = false;
        } else {
            if(this.phone != "" && this.phone != null) {
                let phtest = ph.test(this.phone.replace(/\D/g, ""));
                if(this.phone != "" && !phtest) {
                    this.errorMess = "Invalid phone number.";
                    this.showError = true;
                    this.phone = this.currentVals[5]; //reset
                    this.numchange = false;
                    this.timerlock += 1;
                    let lock = this.timerlock;
                    setTimeout(() => { 
                    if(this.timerlock == lock) {
                        this.showError = false
                    }
                    }, 5000);
                } else {
                    //do query, shouldn't be backend issues here
                }
            }
        }
      },
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
    margin-right: 0.7em;
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
    margin-left: -0.1em;
  }
</style>