<template>
  <div id="register">
    <div id="error" class="card" v-show="showError">
      <div class="card-body">
        {{ errorMess }}
      </div>
    </div>
    <div id="alert" class="card" v-show="showAlert">
      <div class="card-body">
        {{ alertMess }}
      </div>
    </div>
    <div id="formElements">
        <div class="mb-3">
          <label for="email" class="form-label">
            Email
         </label>
          <input :disabled="!emailchange" type="email" class="form-control" id="email" v-model="email" placeholder="Enter email">
      </div>
        <div class="mb-3">
            <label for="username" class="form-label">
                Username
            </label>
            <input :disabled="!userchange" type="text" class="form-control" id="username" v-model="username" placeholder="Enter username">
        </div>
        <div class="mb-3" id="yeardiv">
          <label for="year" class="form-label">
              Birth Year
              <button v-if="!yearchange" type="button" class="btn btn-link" @click='yearchange=true'><i class="bi bi-pencil-square"></i></button>
              <button v-if="yearchange" type="button" class="btn btn-link" @click='() => {yearchange=false; year = currentVals[3]}'><i class="bi bi-x-square"></i></button>
          </label>
          <input :disabled="!yearchange" type="number" class="form-control" id="year" v-model="year" placeholder="Enter the year you were born">
       </div>
       <label class="form-check-label" id="genderlabel" for="gendergroup">
           Sex
           <button v-if="!sexchange" type="button" class="btn btn-link" @click='sexchange=true'><i class="bi bi-pencil-square"></i></button>
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
            <button v-if="numchange" type="button" class="btn btn-link" @click='() => {numchange=false; phone = currentVals[5]}'><i class="bi bi-x-square"></i></button>
        </label>
        <input :disabled="!numchange" type="text" class="form-control" id="phone" v-model="phone" placeholder="Enter your phone number">
      </div>
        <button :disabled="!yearchange && !sexchange && !numchange" id="saveBut" class="btn btn-primary" type="submit" @click="sendQuery">Save</button>
        <button id="changePassBut" class="btn btn-success" type="submit" @click="changePassEmail">Change Password</button>
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
            showAlert: false,
            alertMess: "",
            response: {},
            status: 0,
            currentVals: null,
            userchange: false,
            passchange: false,
            emailchange: false,
            yearchange: false,
            sexchange: false,
            numchange: false,
            timerlock: 0,
            querylock: false
        }
    },
    beforeCreate: async function() {
        let url = "http://jinchispace.com:5001/user/sessiondata";
        await fetch(url, { //executes the query with a promise to get around asynchronous javascript behavior
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
      getInfo: async function() {
          //perform query to get user data; for now just use dummy values
          let url = 'http://jinchispace.com:5001/user/profile';
          await fetch(url, { //executes the query with a promise to get around asynchronous javascript behavior
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
                console.log('test');
                this.username = data.data.username;
                this.password = "password";
                this.email = data.data.email;
                this.year = data.data.birth_year;
                this.gender = data.data.gender;
                this.phone = data.data.phone;
                this.currentVals = [this.email, this.username, this.password, this.year, this.gender, this.phone];
            } else {
                this.currentVals = [null, null, null, null, null, null];
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
      changePassEmail: async function() {
          document.getElementById("changePassBut").disabled = true; //stop queries from happening
          let url = "http://jinchispace.com:5001/user/forget_password";
          this.showAlert = false;
           await fetch(url, { //executes the query with a promise to get around asynchronous javascript behavior
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
                      this.alertMess = "An email with a password reset link has been sent to " + this.email + ". If you do not see the email check you spam folder as well.";
                      this.showAlert = true;
                      setTimeout(() => { 
                        this.showAlert = false;
                      }, 10000);
                    } else {
                      this.errorMess = this.response.msg;
                      this.showError = true;
                      this.timerlock += 1;
                        let lock = this.timerlock;
                        setTimeout(() => { 
                          if(this.timerlock == lock) {
                            this.showError = false
                          }
                        }, 5000);
                    }
                    }).catch(error => {
                    if(error.response) {
                        if(this.status == 401 || this.status == 500) {
                            this.errorMess = error.response.data.msg;
                            this.showError = true;
                            this.timerlock += 1;
                            let lock = this.timerlock;
                            setTimeout(() => { 
                              if(this.timerlock == lock) {
                                this.showError = false
                              }
                            }, 5000);
                        }
                    }
                    document.getElementById("changePassBut").disabled = false; //allow queries to start again
                });
            document.getElementById("changePassBut").disabled = false; //allow queries to start again
      },
      sendQuery: async function() {
        let proceed = 0;
        let num = 0;
        if(this.yearchange) {
          let temp = this.yearQuery();
          if(temp == 0) {
            this.yearchange = false;
            this.year = this.currentVals[3]; //reset
            this.sexchange = false;
            this.gender = this.currentVals[4]; //reset
            this.numchange = false;
            this.phone = this.currentVals[5]; //reset
            return false;
          } else {
            proceed += temp;
            num += 1;
          }
        }
        if(this.sexchange) {
          let temp = this.sexQuery();
          if(temp == 0) {
            this.yearchange = false;
            this.year = this.currentVals[3]; //reset
            this.sexchange = false;
            this.gender = this.currentVals[4]; //reset
            this.numchange = false;
            this.phone = this.currentVals[5]; //reset
            return false;
          } else {
            proceed += temp;
            num += 1;
          }
        }
        if(this.numchange) {
          let temp = this.numQuery();
          if(temp == 0) {
            this.yearchange = false;
            this.year = this.currentVals[3]; //reset
            this.sexchange = false;
            this.gender = this.currentVals[4]; //reset
            this.numchange = false;
            this.phone = this.currentVals[5]; //reset
            return false;
          } else {
            proceed += temp;
            num += 1;
          }
        }
        if(proceed == 2*num) { //none of the values changed
            this.yearchange = false;
            this.year = this.currentVals[3]; //reset
            this.sexchange = false;
            this.gender = this.currentVals[4]; //reset
            this.numchange = false;
            this.phone = this.currentVals[5]; //reset
            return false;
        } else { //some values actually changed, do a query to update
          let url = 'http://jinchispace.com:5001/user/profile';
          let data = {'birth_year': this.year, 'gender': this.gender, 'phone': this.phone}
          await fetch(url, { //executes the query with a promise to get around asynchronous javascript behavior
            method: 'post',
            credentials: "include",
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json;charset=UTF-8',
                "Set-Cookie": "test=value; Path=/; Secure; SameSite=None;",
                'Access-Control-Allow-Origin': 'jinchispace.com:5001',
                'Access-Control-Allow-Credentials': true,
            },
            body:  JSON.stringify(data)})
            .then((response) => { 
                this.status = response.status;
                return response.json() 
            })
            .then(data => {
            this.response = data; //update table with new data
            if(this.status == 200) {
                this.alertMess = "Changes saved.";
                this.showAlert = true;
                setTimeout(() => { 
                  this.showAlert = false;
                }, 3000);
                this.yearchange = false;
                this.sexchange = false;
                this.numchange = false;
            } else {
                this.errorMess = "Saving failed.";
                this.showError = true;
                this.timerlock += 1;
                let lock = this.timerlock;
                setTimeout(() => { 
                  if(this.timerlock == lock) {
                    this.showError = false
                  }
                }, 5000);
                this.yearchange = false;
                this.year = this.currentVals[3]; //reset
                this.sexchange = false;
                this.gender = this.currentVals[4]; //reset
                this.numchange = false;
                this.phone = this.currentVals[5]; //reset
            }
            }).catch(error => {
            if(error.response) {
                if(this.status == 200) {
                console.log(this.response.msg); //switch to main page here
                } 
                this.errorMess = "Saving failed.";
                this.showError = true;
                this.timerlock += 1;
                let lock = this.timerlock;
                setTimeout(() => { 
                  if(this.timerlock == lock) {
                    this.showError = false
                  }
                }, 5000);
                this.yearchange = false;
                this.year = this.currentVals[3]; //reset
                this.sexchange = false;
                this.gender = this.currentVals[4]; //reset
                this.numchange = false;
                this.phone = this.currentVals[5]; //reset 
            }
            });
          return true;
        }
      },
      emailQuery: function() {
        this.showError = false;
        this.querylock = true;
        var re =  /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/; // eslint-disable-line
        if(!re.test(this.email)) {
            this.errorMess = "Please input a valid email.";
            this.showError = true;
            this.email = this.currentVals[0]; //reset email
            this.emailchange = false;
            this.querylock = false;
            this.timerlock += 1;
            let lock = this.timerlock;
            setTimeout(() => { 
              if(this.timerlock == lock) {
                this.showError = false
              }
            }, 5000);
        } else if(this.email == this.currentVals[0]) {
            this.emailchange = false; //email did not change so no need to update
            this.querylock = false;
        } else {
            //do query
            //need error message for if username is taken (should come from the backend)
            this.querylock = false;
        }
      },
      userQuery: function() {
        this.showError = false;
        this.querylock = true;
        if(this.username == "" || this.username == null) {
            this.errorMess = "Please input a username.";
            this.showError = true;
            this.username = this.currentVals[1]; //reset
            this.userchange = false;
            this.querylock = false;
            this.timerlock += 1;
            let lock = this.timerlock;
            setTimeout(() => { 
              if(this.timerlock == lock) {
                this.showError = false
              }
            }, 5000);
        } else if(this.username == this.currentVals[1]) {
            this.userchange = false; //no change
            this.querylock = false;
        } else {
            //query
            //check if username is taken
            this.querylock = false;
        }
      },
      passQuery: function() {
        this.showError = false;
        this.querylock = true;
        if(this.password.length < 8) {
            this.errorMess = "Your password must have a minimum of 8 characters.";
            this.showError = true;
            this.password = this.currentVals[2]; //reset
            this.password2 = ""; //reset
            this.passchange = false;
            this.querylock = false;
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
            this.querylock = false;
            this.timerlock += 1;
            let lock = this.timerlock;
            setTimeout(() => { 
              if(this.timerlock == lock) {
                this.showError = false
              }
            }, 5000);
        } else if(this.password == this.currentVals[2]) {
            this.passchange = false; //no change
            this.querylock = false;
        } else {
            //do query, shouldn't be any errors from backend here, other than query issues
            this.querylock = false;
        }
      },
      yearQuery: function() {
        this.showError = false;
        this.querylock = true;
        var today = new Date();
        var yyyy = today.getFullYear();
        if(this.year < yyyy-120 || this.year > yyyy) {
            this.errorMess = "Please input a valid year.";
            this.showError = true;
            this.year = this.currentVals[3]; //reset
            this.yearchange = false;
            this.querylock = false;
            this.timerlock += 1;
            let lock = this.timerlock;
            setTimeout(() => { 
              if(this.timerlock == lock) {
                this.showError = false
              }
            }, 5000);
            return 0;
        } else if(yyyy - this.year < 16) {
            this.errorMess = "You must be at least 16 years old to use Medisys.";
            this.showError = true;
            this.year = this.currentVals[3]; //reset
            this.yearchange = false;
            this.querylock = false;
            this.timerlock += 1;
            let lock = this.timerlock;
            setTimeout(() => { 
              if(this.timerlock == lock) {
                this.showError = false
              }
            }, 5000); 
            return 0; //error
        } else if(this.year == this.currentVals[3]) {
            this.yearchange = false;
            this.querylock = false;
            return 2; //no errors but same as current value
        } else {
            //do query, shouldn't be any backend errors here
            this.querylock = false;
            return 1; //no errors
        }
      },
      sexQuery: function() {
        this.showError = false;
        this.querylock = true;
        if(this.gender == null) { //this shouldn't really happen, but just in case
            this.errorMess = "Please select your sex.";
            this.showError = true;
            this.gender = this.currentVals[4]; //reset
            this.sexchange = false;
            this.querylock = false;
            this.timerlock += 1;
            let lock = this.timerlock;
            setTimeout(() => { 
              if(this.timerlock == lock) {
                this.showError = false
              }
            }, 5000);
            return 0;
        } else if(this.gender == this.currentVals[4]) {
            this.sexchange = false;
            this.querylock = false;
            return 2;
        } else {
            //do query, shouldn't be any backend errors
            this.querylock = false;
            return 1;
        }
      },
      numQuery: function() {
        this.showError = false;
        this.querylock = true;
        var ph = /^[2-9]\d{2}[2-9]\d{2}\d{4}$/; // eslint-disable-line
        if(this.phone == this.currentVals[5]) {
            this.numchange = false;
            this.querylock = false;
            return 2;
        } else {
            if(this.phone != "" && this.phone != null) {
                let phtest = ph.test(this.phone.replace(/\D/g, ""));
                if(this.phone != "" && !phtest) {
                    this.errorMess = "Invalid phone number.";
                    this.showError = true;
                    this.phone = this.currentVals[5]; //reset
                    this.numchange = false;
                    this.querylock = false;
                    this.timerlock += 1;
                    let lock = this.timerlock;
                    setTimeout(() => { 
                    if(this.timerlock == lock) {
                        this.showError = false
                    }
                    }, 5000);
                    return 0;
                } else {
                    //do query, shouldn't be backend issues here
                    this.querylock = false;
                    return 1;
                }
            } else {
              return 2;
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
  #saveBut {
    margin-top: 0.6em;
  }
  #alert {
    color: rgb(40, 190, 90);
    margin-top: 0.2em;
    margin-bottom: 0.2em;
    margin-left: 0.6em;
    margin-right: 0.6em;
  }
  #changePassBut {
    margin-top: 0.3em;
    margin-right: 0.6em;
  }
</style>