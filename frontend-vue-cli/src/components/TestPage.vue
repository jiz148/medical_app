<template>
  <div id="header">
      AI Internal Medicine
    </div>
</template>

<script>
export default {
  name: "TestPage",
  props: {},
  data() {
      return {}
  },
  created: function() {
      fetch('http://127.0.0.1:5001/user/test', { //executes the query with a promise to get around asynchronous javascript behavior
        method: 'get',
        credentials: "include",
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json;charset=UTF-8',
            'Set-Cookie': 'widget_session=abc123; SameSite=None; Secure',
            'Access-Control-Allow-Origin': 'http://127.0.0.1:5001/',
            'Access-Control-Allow-Credentials': true,
        }})
        .then((response) => { 
            console.log('test');
            console.log(response);
            this.status = response.status;
            return response; //return response.json() 
        })
        .then(data => {
          console.log('test1');
          console.log(data);
          this.response = data; //update table with new data
          if(this.status == 200) {
            console.log('success');
          } else {
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

  }
}
</script>

<style>
  #header {
    font-size: 24px;
    color: rgb(134, 146, 146);
    background-color: rgb(217, 248, 255);
    padding-top: 0.6em;
    padding-bottom: 0.6em;
    padding-left: 0.8em;
    font-weight: bold;
  }
</style>
