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
    },
    beforeCreate: function () {
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
    },
    data() {
        return {
            query: "",
            message: "AI Interal Medicine searches a large database to diagnose you. To start simply enter your symptoms and answer the questions the app asks you.",
            showError: false,
            errorMess: "",
            response: {},
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
  #logoutBut {
    margin-left: 0.6em;
  }
  #formbtn {
    display: inline;
  }
</style>
