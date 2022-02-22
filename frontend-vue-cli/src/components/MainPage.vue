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
  </div>
</template>

<script>
  export default { //controls form input
    name: "MainPage",
    props: {},
    beforeCreate: function () {
      let url = "http://127.0.0.1:5001/user/authenicate"
      this.axios //executes the query with a promise to get around asynchronous javascript behavior
        .get(url, {
            credentials: "include",
          }, {
            headers: {
            'Content-Type': 'application/json;charset=UTF-8',
            'Access-Control-Allow-Origin': '*',
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
            var status = error.response.status;
            if(status == 401) {
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
            response: {}
        }
    },
    methods: {
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
  #formElements {
    margin-left: 0.6em;
  }
  #formbtn {
    display: inline;
  }
</style>
