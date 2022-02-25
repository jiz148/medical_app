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
    <button id="logoutBut" class="btn btn-secondary" type="submit" @click="logout">Logout</button>
  </div>
</template>

<script>
  export default { //controls form input
    name: "MainPage",
    props: {
      sid: String
    },
    beforeCreate: function () {
      let url = "http://127.0.0.1:5001/user/sessiondata";
      console.log("mainpage sid: " + this.$route.query.sid);
      //document.cookie = 'session='+this.$route.query.sid;
      document.cookies = "secure=true";
      //document.cookie['session'] = this.$route.query.sid;
      //let csrf = document.getElementsByName("csrf-token")[0].content;
      console.log(document.cookie);
      //console.log("csrf" + this.csrf);
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
            //console.log('test');
            this.status = response.status;
            return response.json() 
        })
        .then(data => {
          console.log(this.status);
          this.response = data; //update table with new data
          if(this.status == 200) {
              if(this.response.accepted == null) {
                  this.$router.push('/');
              }
              else if(this.response.uid == null) {
                  this.$router.push('/login');
              }
              console.log(this.response); //switch to main page here
              //this.$router.push('/main');
          } else {
            console.log('bad');
              this.$router.push('/');
          }
        }).catch(error => {
        if(error.response) {
            console.log("Error: " + error.message);
            console.log(this.response);
            if(this.status == 200) {
              console.log(this.response.msg); //switch to main page here
              //this.$router.push('/main');
            } else {
              this.$router.push('/');
            }
        }
        });
      /*this.axios //executes the query with a promise to get around asynchronous javascript behavior
        .get(url, { withCredentials: true }, {
            credentials: "include",
          }, {
            headers: {
            'Content-Type': 'application/json;charset=UTF-8',
            "Set-Cookie": "test=value; Path=/; Secure; SameSite=None;",
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': true,
            "X-CSRFToken": csrf
        },
        })
        .then(response => {
          this.response = response.data; //update table with new data
          var status = response.status;
          console.log(this.response);
          if(status == 200) {
              console.log(this.response.msg); //switch to main page here
              //this.$router.push('/main');
          } else {
              this.$router.push('/');
          }
        }).catch(error => {
        if(error.response) {
            console.log("Error: " + error.message);
            console.log(this.response);
            var status = error.response.status;
            if(status == 200) {
              console.log(this.response.msg); //switch to main page here
              //this.$router.push('/main');
            } else {
              this.$router.push('/');
            }
        }
        });*/
    },
    data() {
        return {
            query: "",
            message: "AI Interal Medicine searches a large database to diagnose you. To start simply enter your symptoms and answer the questions the app asks you.",
            showError: false,
            errorMess: "",
            response: {},
            //csrf: document.querySelector('meta[name="csrf-token"]').getAttribute('content'), //document.getElementsByName("csrf-token")[0].content
            status: 0
        }
    },
    methods: {
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
              //console.log('test');
              this.status = response.status;
              return response.json() 
          })
          .then(data => {
            console.log(this.status);
            this.response = data; //update table with new data
            if(this.status == 200) {
                this.$router.push('/');
                console.log(this.response); //switch to main page here
                //this.$router.push('/main');
            } else {
              console.log('bad');
            }
          }).catch(error => {
          if(error.response) {
              console.log("Error: " + error.message);
              console.log(this.response);
              if(this.status == 200) {
                console.log(this.response.msg); //switch to main page here
                //this.$router.push('/main');
              } else {
                this.$router.push('/');
              }
          }
          });
      },
      toggleMessage: function() {
        this.show = !this.show;
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
  #logoutBtn {
    margin-left: 0.6em;
  }
  #formbtn {
    display: inline;
  }
</style>
