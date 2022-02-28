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
    
    <select id="visitSelect" v-model="curVisit" class="btn btn-outline-primary dropdown-toggle" @change="loadVisit">
      <option class="visitItem" v-for="item in visitList" :value="item" :key="item.id">{{item.val}}</option>
    </select>

    <div id="visitModal" class="modal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">Create a New Visit</h5>
          </div>
          <div class="modal-body">
            <div class="mb-3">
                <label for="vistnanme" class="form-label">Visit Name</label>
                <input type="text" class="form-control" id="visitname" v-model="visitname" placeholder="Enter a name for the visit">
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-success" @click="createVisit">Create Visit</button>
            <button type="button" class="btn btn-danger" data-dismiss="modal" @click="closeVisit">Cancel</button>
          </div>
        </div>
      </div>
    </div>
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
            status: 0,
            curVisit: {'val': 'Select a Visit', 'id': 0},
            visitList: [
              {'val': 'Select a Visit', 'id': 0}, 
              {'val': 'New Visit', 'id': 1}],
            visitname: "",
            visitInit: false
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
      loadVisit: function() {
        let item = this.curVisit;
        if(item.id == 1) { //new visit
          this.launch();
        } else if(item.id > 1) {
          if(item.id !== 0 && !this.visitInit) { //remove initial select option
            this.visitList.splice(0,1);
            this.visitInit = true;
          }
        }
      },
      launch: function() {
        /*eslint-disable */
        //suppress all warnings between comments
        $('#visitModal').modal('show'); //need to do this disable because eslint doesnt understand jquery for some reason
        /*eslint-enable */
      },
      createVisit: function() {
        //probably need to query the backend here and on page load to store visit data
        let ln = this.visitList.length - 1;
        ln = this.visitList[ln].id + 1;
        if(!this.visitInit) { //remove initial select option
            this.visitList.splice(0,1);
            this.visitInit = true;
        }
        let el = {'val': this.visitname, 'id': ln}
        this.visitList.push(el);
        this.curVisit = el;

        this.closeVisit();
      },
      closeVisit: function() {
        this.visitname = "";
        /*eslint-disable */
        //suppress all warnings between comments
        $('#visitModal').modal('hide'); //need to do this disable because eslint doesnt understand jquery for some reason
        /*eslint-enable */
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
  .visitItem {
    background-color: #f7f7f7;
    color: #0275d8;
  }
  .modal-header {
    background-color: rgb(250, 251, 252);
  }
  .modal-footer {
     background-color: rgb(250, 251, 252);
  }
  #visitSelect {
    float: right;
    margin-right: 0.6em;
    height: 2.4em;
  }
  .visitItem {
    height: 2.0em;
    text-align-last: center;
  }
  option{
     text-align-last: center;
     padding:5px 0;
   }
</style>
