<template>
  <div id="main">
    <div id="top">
      <div id="error" class="card" v-show="showError">
        <div class="card-body">
          {{ errorMess }}
        </div>
      </div>
      <div id="appinfo" class="card" v-show="showInfo"> 
        <div class="card-body">
          {{ message }} 
        </div>
      </div>
      
      <div id="ralTop">
        <div id="settingsDrop" class="btn-group">
          <button type="button" class="btn btn-outline-secondary dropdown-toggle caret-off" data-bs-display="static" data-bs-toggle="dropdown" aria-expanded="false">
            <i class="bi bi-three-dots-vertical"></i>
          </button>
          <ul class="dropdown-menu dropdown-menu-end">
            <li><button class="dropdown-item" type="button" @click='this.$router.push("/profile")'>Profile</button></li>
            <li><button class="dropdown-item" type="button" @click='this.$router.push("/settings")'>Settings</button></li>
            <li><button class="dropdown-item" type="button" @click="contact">Contact Us</button></li>
            <li><button class="dropdown-item" type="button" @click="logout">Logout</button></li>
          </ul>
        </div>
      </div>

      <div id="buttonSection">
        <select id="visitSelect" v-model="curVisit" class="btn btn-outline-primary dropdown-toggle">
          <option class="visitItem" v-for="item in visitList" :value="item" :key="item.visit_id">{{item.note + " " + item.datetime}}</option>
        </select>
        <br>
        <button type="submit" class="btn btn-primary" id="confirmBut" @click='loadVisit'>Confirm</button>
        <br>
        <button id="newVisitBut" class="btn btn-success" type="submit" @click="createVisit">New Visit</button>
      </div>

      <div id="contactModal" class="modal" tabindex="-1" role="dialog" aria-labelledby="contactModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="contactModalLabel">Contact Us</h5>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                You can email us at (enter email here), or call us at (enter phone number here).
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeContact">Close</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default { //controls form input
    name: "VisitPage",
    props: {
    },
    beforeCreate: async function () {
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
        url = "http://127.0.0.1:5001/visit";
        fetch(url, { //executes the query with a promise to get around asynchronous javascript behavior
                method: 'GET',
                credentials: "include",
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json;charset=UTF-8',
                    "Set-Cookie": "test=value; Path=/; Secure; SameSite=None;",
                    'Access-Control-Allow-Origin': '127.0.0.1:5001',
                    'Access-Control-Allow-Credentials': true,
                }
                })
                .then((response) => { 
                    this.status = response.status;
                    return response.json() 
                })
                .then(data => {
                    this.response = data; 
                    if(this.status == 200) {
                        let li = this.response.result;
                        for(let i=0;i<li.length;i++) {
                          if(li[i].visit_id > 0) {
                            this.visitList.push(li[i]);
                          }
                        }
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
                });
    },
    data() {
        return {
            query: "",
            message: "Select a visit from the dropdown and confirm, or create a new visit.",
            showInfo: true,
            showError: false,
            errorMess: "",
            response: {},
            status: 0,
            visitList: [ //should hide all inputs when an actual visit isnt selected
              {'note': 'Select a Visit', 'visit_id': 0, 'datetime': ""}], 
            curVisit: {'note': 'Select a Visit', 'visit_id': 0, 'datetime': ""},
            visitname: ""
        }
    },
    methods: {
      loadVisit: async function() {
        this.showError = false;
        if(this.curVisit != null && this.curVisit.visit_id > 0) {
            this.$router.push('/main?visit='+this.curVisit.visit_id);
        } else {
            this.errorMess = "Please select a visit before confirming, or create a new visit."
            this.showError = true;
        }
      },
      createVisit: function() {
        let url = "http://127.0.0.1:5001/visit";
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
                    'note': 'New Visit'
                })
                })
                .then((response) => { 
                    this.status = response.status;
                    return response.json() 
                })
                .then(data => {
                    this.response = data; 
                    if(this.status == 200) {
                        this.$router.push('/main?visit='+data.visit_id);
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
                });
      },
      contact: function() {
        /*eslint-disable */
        //suppress all warnings between comments
        $('#contactModal').modal('show'); //need to do this disable because eslint doesnt understand jquery for some reason
        /*eslint-enable */
      },
      closeContact: function() {
        /*eslint-disable */
        //suppress all warnings between comments
        $('#contactModal').modal('hide'); //need to do this disable because eslint doesnt understand jquery for some reason
        /*eslint-enable */
      },
      logout: function() {
        let url = "http://127.0.0.1:5001/user/logout";
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
      },
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
  #main {
    display: flex;
    flex-direction: column;
  }
  #infoBut {
    margin-left: 0.6em;
  }
  #logoutBut {
    margin-left: 0.6em;
  }
  #formbtn {
    display: inline;
  }
  #newVisitBut {
    margin-right: 0.6em;
  }
  .visitItem {
    background-color: #f7f7f7;
    color: #0275d8;
  }
  .dropdown {
    display: block;
    float:left;
  }
  .caret-off::before {
    display: none;
  }
  .caret-off::after {
    display: none;
  }
  .modal-header {
    background-color: rgb(250, 251, 252);
  }
  .modal-footer {
     background-color: rgb(250, 251, 252);
  }
  #visitSelect {
    margin-right: 0.6em;
    height: 2.4em;
    display: inline;
    max-width: 80%;
  }
  .visitItem {
    height: 2.0em;
    text-align-last: center;
  }
  option{
     text-align-last: center;
     padding:5px 0;
   }
   #confirmBut {
       margin-top: 0.5em;
       margin-right: 0.4em;
       width: 6em;
   }
   #newVisitBut {
       margin-top: 0.5em;
       width: 6em;
   }
   #buttonSection {
       margin-top: 0.5em;
       margin-left: 0.6em;
   }
   #ralTop {
    float: right;
    display: inline;
    margin-top: 0.2em;
  }
  #infoBut {
    margin-left: 0.6em;
  }
  #logoutBut {
    margin-left: 0.6em;
  }
</style>
