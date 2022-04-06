<template>
  <div id="register">
    <div id="error" class="card" v-show="showError">
      <div class="card-body">
        {{ errorMess }}
      </div>
    </div>
    <div id="formElements">
      <label class="form-check-label" id="asboollabel" for="autosavegroup">
          Autosaving
      </label>
      <div id="autosavegroup">
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="asyes" id="asyes" value="yes" v-model="autosavebool">
          <label class="form-check-label" for="asyes">Yes</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="asno" id="asno" value="no" v-model="autosavebool">
          <label class="form-check-label" for="asno">No</label>
        </div>
       </div>
       <div class="mb-3" v-if="autosavebool == 'yes'">
          <label for="astime" class="form-label">Time Between Autosaves in Seconds</label>
          <input type="number" class="form-control" id="astime" v-model="astime">
        </div>
        <label class="form-check-label" id="tablelabel" for="tablegroup">
          Tables
        </label>
        <div id="tablegroup">
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="radio" name="tableex" id="tableex" value="expanded" v-model="tablebool">
            <label class="form-check-label" for="tableex">Expanded</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="radio" name="tableco" id="tableco" value="collapsed" v-model="tablebool">
            <label class="form-check-label" for="tableco">Collapsed</label>
          </div>
          </div>
        <div class="mb-3">
          <label for="numcolumns" class="form-label">
            Max Number of Columns Per Table
          </label>
          <input type="number" class="form-control" id="numcolumns" v-model="numcolumns">
      </div>
      <button id="saveBut" class="btn btn-primary" type="submit" @click="save">Save</button>
      <button id="backBut" class="btn btn-secondary" type="submit" @click="$router.go(-1)">Back</button>
    </div>
  </div>
</template>

<script>
  export default { //controls form input
    name: "SettingsPage",
    props: {},
    data() {
        return {
            query: "",
            showError: false,
            errorMess: "",
            response: {},
            switchpage: false,
            status: 0,
            autosavebool: 'yes',
            astime: 30,
            tablebool: 'expanded',
            numcolumns: 20,
            currentVals: [],
            timerlock: 0,
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
          this.autosavebool = "yes";
          this.astime = 30;
          this.tablebool = "expanded";
          this.numcolumns = 20;
          this.currentVals = [this.autosavebool, this.astime, this.tablebool, this.numcolumns];
      },
      save: function() {
        if(this.astime == null || this.astime < 1) {
          this.errorMess = "Please enter a time greater than 0 seconds.";
          this.showError = true;
          this.reset();
          this.timerlock += 1;
          let lock = this.timerlock;
          setTimeout(() => { 
            if(this.timerlock == lock) {
              this.showError = false;
            }
          }, 5000);
        } else if(this.astime > 86400) {
          this.errorMess = "Please enter a time less than 1 day.";
          this.showError = true;
          this.reset();
          this.timerlock += 1;
          let lock = this.timerlock;
          setTimeout(() => { 
            if(this.timerlock == lock) {
              this.showError = false;
            }
          }, 5000);
        } else if(this.numcolumns == null || this.numcolumns < 1) {
          this.errorMess = "Please display at least 1 column.";
          this.showError = true;
          this.reset();
          this.timerlock += 1;
          let lock = this.timerlock;
          setTimeout(() => { 
            if(this.timerlock == lock) {
              this.showError = false;
            }
          }, 5000);
        } else if(this.numcolumns > 100) {
          this.errorMess = "Please display 100 or less columns.";
          this.showError = true;
          this.reset();
          this.timerlock += 1;
          let lock = this.timerlock;
          setTimeout(() => { 
            if(this.timerlock == lock) {
              this.showError = false;
            }
          }, 5000);
        } else {
          //perform query
        }
      },
      reset: function() {
        this.autosavebool = this.currentVals[0];
        this.astime = this.currentVals[1];
        this.tablebool = this.currentVals[2];
        this.numcolumns = this.currentVals[3];
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
  #backBut {
    margin-top: 0.3em;
  }
  #autosavegroup {
    margin-bottom: 0.6em;
    font-size: 17px;
    color: rgb(108,117,125);
  }
  #tablegroup {
    margin-bottom: 0.6em;
    font-size: 17px;
    color: rgb(108,117,125);
  }
</style>