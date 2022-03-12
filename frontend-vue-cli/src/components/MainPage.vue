<template>
  <div id="main">
    <div id="top">
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

      <button id="infoBut" class="btn btn-outline-secondary" @click="this.showInfo=!this.showInfo">Info</button>
      
      <div id="ralTop">
        <div id="settingsDrop" class="btn-group">
          <button type="button" class="btn btn-outline-secondary dropdown-toggle caret-off" data-bs-display="static" data-bs-toggle="dropdown" aria-expanded="false">
            <i class="bi bi-three-dots-vertical"></i>
          </button>
          <ul class="dropdown-menu dropdown-menu-end">
            <li><button class="dropdown-item" type="button">Profile</button></li>
            <li><button class="dropdown-item" type="button">Edit</button></li>
            <li><button class="dropdown-item" type="button" @click="contact">Contact Us</button></li>
            <li><button class="dropdown-item" type="button" @click="logout">Logout</button></li>
          </ul>
        </div>
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

      <div id="appinfo" class="card" v-show="showInfo"> 
        <div class="card-body">
          {{ message }} 
        </div>
      </div>
    </div>
    <div id="middle">
      <div class="accordion accordion-flush" id="tableAccordion1">
        <div id="currentFindDiv" class="accordion-item">
          <div id="currentFindHead" class="accordion-header">
            <button id="currentFindTitle" class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#currentFindBody" aria-expanded="true" aria-controls="currentFindBody">
              Current Findings For {{curVisit.note}}
            </button>
          </div>
          <div id="currentFindBody" class="accordion-collapse collapse show" aria-labelledby="currentFindHead" data-bs-parent="#tableAccordion1">
            <div class="accordion-body">
              <table id="currentFind" class="table table-striped align-middle table-sm">
                <thead>
                  <tr>
                    <th scope="col">Question</th>
                      <th scope="col">Response</th>
                      <th scope="col"></th>
                      <th scope="col"></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in currentFindings" :key="item.FID">
                      <td>{{item.Name}}</td>
                      <td>{{item.answer}}</td>
                      <td><button type="button" class="btn btn-link" @click="createEditFind(item)">Edit</button></td>
                      <td><input class="form-check-input" type="checkbox" v-model="item.checked"></td>
                    </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <div class="accordion accordion-flush" id="tableAccordion">
        <div id="findingsDiv" class="accordion-item">
          <div id="findHead" class="accordion-header">
            <button id="findingsTitle" class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#findingsBody" aria-expanded="true" aria-controls="findingsBody">
              Top Findings
            </button>
          </div>
          <div id="findingsBody" class="accordion-collapse collapse show" aria-labelledby="findHead" data-bs-parent="#tableAccordion">
            <div class="accordion-body">
              <button id="nbqBut" class="btn btn-primary" type="submit" @click="getNbq">Next Best Question</button>
              <input type="text" class="form-control" id="findSearch" v-model="findSearch" @input="searchFindings" placeholder="Search top findings">
              <table id="findings" class="table table-striped table-hover align-middle table-sm">
                <thead>
                  <tr>
                    <th scope="col">#</th>
                    <th scope="col">Question</th>
                    <th scope="col"></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in searchedFindings" :key="item.FID" @click="createNewFind(item)">
                    <td>{{item.FID}}</td>
                    <td>{{item.Name}}</td>
                    <td><a :href="item.URL" class="button btn btn-link">Info</a></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <div class="accordion accordion-flush" id="tableAccordion2">
        <div id="matchesDiv" class="accordion-item">
          <div id="matchesHead" class="accordion-header">
            <button id="matchesTitle" class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#matchesBody" aria-expanded="true" aria-controls="matchesBody">
              Top Diseases
            </button>
          </div>
          <div id="matchesBody" class="accordion-collapse collapse show" aria-labelledby="matchesHead" data-bs-parent="#tableAccordion2">
            <div class="accordion-body">
              <table id="matches" class="table table-striped align-middle table-sm">
                <thead>
                  <tr>
                    <th scope="col">#</th>
                    <th scope="col">Disease</th>
                    <th scope="col"></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in matchesList" :key="item.DID">
                    <td>{{item.DID}}</td>
                    <td>{{item.Name}}</td>
                    <td><a :href="item.link" class="button btn btn-link">Info</a></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <div id="editFindModal" class="modal" tabindex="-1" role="dialog" aria-labelledby="editFindLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="editFindLabel">Edit Finding</h5>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <a v-if="editFindQuestion!=null" style="font-size: 16px; font-weight: bold; margin-left: 0.4em;">{{
                  editFindQuestion.Name
                }}</a>
                <br>
                <input class="form-check-input" type="radio" name="flexRadioDefault" id="findEditYes" value="yes" v-model="editFindResp">
                <label class="form-check-label" for="findEditYes">
                  Yes
                </label>
                <input class="form-check-input" type="radio" name="flexRadioDefault" id="findEditNo" value="no" v-model="editFindResp">
                <label class="form-check-label" for="findEditNo">
                  No
                </label>
                <input class="form-check-input" type="radio" name="flexRadioDefault" id="findEditMaybe" value="maybe" v-model="editFindResp">
                <label class="form-check-label" for="findEditMaybe">
                  Not Sure
                </label>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-success" @click="makeEditFind">Update</button>
              <button type="button" class="btn btn-danger" data-dismiss="modal" @click="closeEditFind">Cancel</button>
            </div>
          </div>
        </div>
      </div>

      <div id="nbqModal" class="modal" tabindex="-1" role="dialog" aria-labelledby="nbqLabel" aria-hidden="true">
          <div class="modal-dialog" role="document">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="nbqLabel">Next Best Question</h5>
              </div>
              <div class="modal-body">
                <div class="mb-3">
                  <a v-if="nextBestQuestion!=null" style="font-size: 16px; font-weight: bold; margin-left: 0.4em;">{{
                    nextBestQuestion.Name
                  }}</a>
                  <br>
                  <input class="form-check-input" type="radio" name="flexRadioDefault" id="nbqYes" value="yes" v-model="nbqResp">
                  <label class="form-check-label" for="findEditYes">
                    Yes
                  </label>
                  <input class="form-check-input" type="radio" name="flexRadioDefault" id="nbqNo" value="no" v-model="nbqResp">
                  <label class="form-check-label" for="findEditNo">
                    No
                  </label>
                  <input class="form-check-input" type="radio" name="flexRadioDefault" id="nbqMaybe" value="maybe" v-model="nbqResp">
                  <label class="form-check-label" for="findEditMaybe">
                    Not Sure
                  </label>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-success" @click="confirmNbq">Update</button>
                <button type="button" class="btn btn-secondary" data-dismiss="modal" @click="closeNbq">Cancel</button>
              </div>
            </div>
          </div>
      </div>

      <div id="newFindModal" class="modal" tabindex="-1" role="dialog" aria-labelledby="newFindLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="newFindLabel">New Finding</h5>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <a v-if="newFindQuestion!=null" style="font-size: 16px; font-weight: bold; margin-left: 0.4em;">{{
                  newFindQuestion.Name
                }}</a>
                <br>
                <input class="form-check-input" type="radio" name="flexRadioDefault" id="findEditYes" value="yes" v-model="newFindResp">
                <label class="form-check-label" for="findEditYes">
                  Yes
                </label>
                <input class="form-check-input" type="radio" name="flexRadioDefault" id="findEditNo" value="no" v-model="newFindResp">
                <label class="form-check-label" for="findEditNo">
                  No
                </label>
                <input class="form-check-input" type="radio" name="flexRadioDefault" id="findEditMaybe" value="maybe" v-model="newFindResp">
                <label class="form-check-label" for="findEditMaybe">
                  Not Sure
                </label>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-success" @click="makeNewFind">Confirm</button>
              <button type="button" class="btn btn-danger" data-dismiss="modal" @click="closeNewFind">Cancel</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <br>
    <div id="bot">
      <div id="botButs">
        <div id="lalBot">
          <button id="saveBut" class="btn btn-primary" type="submit" @click="save">Save</button>
          <button id="editNameBut" class="btn btn-outline-primary" type="submit" @click="createEditNote">Rename</button>
        </div>
        <div id="ralBot">
          <button id="resetBut" class="btn btn-outline-secondary" type="submit" @click="reset">Reset</button>
          <button id="backBut" class="btn btn-secondary" type="submit" @click="$router.go(-1)">Back</button>
        </div>
      </div>

      <div id="editNoteModal" class="modal" tabindex="-1" role="dialog" aria-labelledby="editNoteLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="editNoteLabel">Change Visit Name</h5>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <label class="form-check-label" for="editNodeInput">
                  Enter Visit Name:
                </label>
                <input type="text" class="form-control" id="editNodeInput" v-model="newNodeVal" placeholder="Enter name">
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-success" @click="makeEditNote">Confirm</button>
              <button type="button" class="btn btn-danger" data-dismiss="modal" @click="closeEditNote">Cancel</button>
            </div>
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
      visit: {
        type: Number,
        default: 0
      }
    },
    beforeCreate: async function () {
      //console.log(this.$route.query.visit);
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
        if(this.$route.query.visit > 0) {
          url = "http://127.0.0.1:5001/visit";
          await fetch(url, { //executes the query with a promise to get around asynchronous javascript behavior
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
                          if(li[i].visit_id == this.$route.query.visit) {
                            this.curVisit = li[i];
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
          this.loadVisit();
        } else {
          this.curVisit = {'note': "New Visit", 'visit_id': 0, 'datetime': ""};
          this.loadVisit();
        }
    },
    data() {
        return {
            query: "",
            message: "AI Interal Medicine searches a large database to diagnose you. Your symptoms are displayed in the Current Findings table. Use the Top Findings table to search for and enter more of your symptoms. The best matches from the database are found in the Top Diseases table.",
            showInfo: false,
            showError: false,
            errorMess: "",
            alertMess: "",
            showAlert: false,
            response: {},
            status: 0,
            curVisit: {'note': 'New Visit', 'visit_id': 0, 'datetime': ""},
            findingsList: [
              {'Name': 'Gender is Male?', 'FID': 1, 'URL': 'https://www.google.com'},
              {'Name': 'Age is between 16 and 50?', 'FID': 2, 'URL': 'https://www.google.com'},
            ],
            searchedFindings: [
              {'Name': 'Gender is Male?', 'FID': 1, 'URL': 'https://www.google.com'},
              {'Name': 'Age is between 16 and 50?', 'FID': 2, 'URL': 'https://www.google.com'},
            ],
            currentFindings: [
              
            ],
            matchesList: [
              {'Name': "test1", 'DID': 1, 'link': 'https://www.google.com'}
            ],
            findSearch: "",
            editFindQuestion: null,
            editFindResp: null,
            newFindQuestion: null,
            newFindResp: null,
            nextBestQuestion: null,
            nbqResp: null,
            newNodeVal: ""
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
      loadVisit: async function() {
        await this.getCurrentFindings();
        this.getDiseases();
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
      createEditFind: function(item) {
        this.editFindQuestion = item;
        this.editFindResp = item.answer;
        /*eslint-disable */
        //suppress all warnings between comments
        $('#editFindModal').modal('show'); //need to do this disable because eslint doesnt understand jquery for some reason
        /*eslint-enable */
      },
      closeEditFind: function() {
        this.editFindQuestion = null;
        /*eslint-disable */
        //suppress all warnings between comments
        $('#editFindModal').modal('hide'); //need to do this disable because eslint doesnt understand jquery for some reason
        /*eslint-enable */
      },
      makeEditFind: function() {
        for(let i=0;i<this.findingsList.length;i++) {
          if(this.currentFindings[i].FID == this.editFindQuestion.FID) {
            if(this.currentFindings[i].answer == this.editFindResp) {
              break;
            }
            this.currentFindings[i].answer = this.editFindResp;
            this.closeEditFind();
            break;
          }
        }
        this.closeEditFind();
      },
      createNewFind: function(item) {
        this.newFindQuestion = item;
        this.newFindResp = item.answer;
        /*eslint-disable */
        //suppress all warnings between comments
        $('#newFindModal').modal('show'); //need to do this disable because eslint doesnt understand jquery for some reason
        /*eslint-enable */
      },
      closeNewFind: function() {
        this.newFindQuestion = null;
        /*eslint-disable */
        //suppress all warnings between comments
        $('#newFindModal').modal('hide'); //need to do this disable because eslint doesnt understand jquery for some reason
        /*eslint-enable */
      },
      makeNewFind: function() {
        let ob = {}
        let id = 1
        if(this.currentFindings.length > 0) {
          id =  this.currentFindings[this.currentFindings.length-1].FID + 1;
        }
        ob['FID'] = id;
        ob['answer'] = this.newFindResp;
        ob['Name'] = this.newFindQuestion.Name; 
        ob['checked'] = true
        this.currentFindings.push(ob);
        this.closeNewFind();
      },
      getNbq: function() {
        //send request to get next best question
        this.nextBestQuestion = {'Name': 'Do you have a fever?', 'FID': 2, 'answer': 'no', 'checked': true} //for testing
        this.nbqResp = null;
        /*eslint-disable */
        //suppress all warnings between comments
        $('#nbqModal').modal('show'); //need to do this disable because eslint doesnt understand jquery for some reason
        /*eslint-enable */
      },
      confirmNbq: function() {
        if(this.nbqResp != null) {
          //send request
          //get back request and update table
          this.nextBestQuestion.answer = this.nbqResp;
          this.currentFindings.push(this.nextBestQuestion);
          this.closeNbq();
        }
      },
      closeNbq: function() {
        this.nextBestQuestion = null;
        this.nbqResp = null;
        /*eslint-disable */
        //suppress all warnings between comments
        $('#nbqModal').modal('hide'); //need to do this disable because eslint doesnt understand jquery for some reason
        /*eslint-enable */
      },
      searchFindings: function() {
        let na = [];
        for(let i=0;i<this.findingsList.length;i++) {
          if(this.findingsList[i].Name.toLowerCase().includes(this.findSearch.toLowerCase())) {
            na.push(this.findingsList[i])
          }
        }
        this.searchedFindings = na;
      },
      toggleMessage: function() {
        this.show = !this.show;
      },
      getDiseases: function() {
        let url = "http://127.0.0.1:5001/disease/top_diseases";
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
                    if(this.response.msg == 'success') {
                        let arr = [];
                        let id = 1;
                        for (const c of Object.entries(data.data)) {
                          let ob = {'Name': c[0], 'Frq': c[1], 'DID': id};
                          id += 1;
                          arr.push(ob);
                        }
                        this.matchesList = arr;
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
              return;
      },
      getCurrentFindings: function() {
        let url = "http://127.0.0.1:5001/finding";
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
                body: JSON.stringify({
                    'visit_id': this.curVisit.visit_id
                })
                })
                .then((response) => { 
                    this.status = response.status;
                    console.log(response);
                    return response.json();
                })
                .then(data => {
                    this.response = data; 
                    console.log(data);
                    if(this.status == 200) {
                        for(let i=0;i<data.data.length;i++) {
                          if(!data.data[i]['checked']) {
                            data.data[i]['checked'] = true
                          }
                        }
                        this.currentFindings = data.data;
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
      reset: async function() {
        this.findingsList = [];
        this.searchedFindings = [];
        this.currentFindings = [];
        this.matchesList = [];
        let vid = this.curVisit.visit_id;
        this.curVisit.visit_id = 0;
        await this.loadVisit();
        this.curVisit.visit_id = vid;
      },
      save: async function() {
        this.showAlert = false;
        this.showError = false;
        let suc = false;
        //do query, probably as async await
        if(this.curVisit.visit_id == 0) { //new visit, create visit
          let url = "http://127.0.0.1:5001/visit";
          await fetch(url, { //executes the query with a promise to get around asynchronous javascript behavior
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
                'note': this.curVisit.note
            })
            })
            .then((response) => { 
                this.status = response.status;
                return response.json() 
            })
            .then(data => {
                this.response = data; 
                if(this.status == 200) {
                    //console.log(this.response); //seems like the query isnt passing back the right visit
                    this.curVisit = this.response.result[this.response.index];
                    suc = true;
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
        } else { //update visit
          suc = true; //placeholder
        }
        //on success perform the followings
        if(suc) {
          this.alertMess = "Changes saved successfully.";
          this.showAlert = true;
          setTimeout(() => {this.showAlert = false}, 5000);
        } else {
          this.errorMess = "Failed to save changes.";
          this.showError = true;
          setTimeout(() => {this.showError = false}, 5000);
        }
      },
      createEditNote: function() {
        this.newNodeVal = ""; //this.curVisit.note;
        /*eslint-disable */
        //suppress all warnings between comments
        $('#editNoteModal').modal('show'); //need to do this disable because eslint doesnt understand jquery for some reason
        /*eslint-enable */
      },
      closeEditNote: function() {
        /*eslint-disable */
        //suppress all warnings between comments
        $('#editNoteModal').modal('hide'); //need to do this disable because eslint doesnt understand jquery for some reason
        /*eslint-enable */
      },
      makeEditNote: function() {
        //console.log(this.newNodeVal);
        if(this.newNodeVal == null || this.newNodeVal == "") {
          this.errorMess = "Please enter a name.";
          this.showError = true;
          setTimeout(() => {this.showError = false}, 5000);
        } else {
          this.curVisit.note = this.newNodeVal;
        }
        this.closeEditNote();
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
#alert {
    color: rgb(40, 190, 90);
    margin-top: 0.2em;
    margin-bottom: 0.2em;
    margin-left: 0.6em;
    margin-right: 0.6em;
  }
#main {
  display: flex;
  flex-direction: column;
}
#top {
  margin-top: 0.4em;
  margin-bottom: 0.4em;
}
#middle {
  background-color: rgb(235,236,237);
  height: 37em;
  font-weight: normal;
  font-size: 14px;
  overflow-y: scroll;
}
#bot {
  font-weight: normal;
  font-size: 14px;
}
#ralTop {
  float: right;
  display: inline;
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
#settingsDrop {
  margin-right: 0.8em;
}
#visitSelect {
  margin-right: 0.6em;
  height: 2.4em;
  display: inline;
}
.visitItem {
  height: 2.0em;
  text-align-last: center;
}
option{
    text-align-last: center;
    padding:5px 0;
  }
  #findings {
    margin-left: 0.6em;
    margin-right: 0.6em;
    width: 99%;
    max-height: 30%;
    overflow: scroll;
  }
  #findingsTitle {
    font-weight: bold;
    font-size: 18px;
    margin-top: 0.4em;
  }
  #currentFindTitle {
    font-weight: bold;
    font-size: 18px;
    margin-top: 0.4em;
  }
  #currentFind {
    margin-left: 0.6em;
    margin-right: 0.6em;
    width: 99%;
    max-height: 30%;
    overflow: scroll;
  }
  #matches {
    margin-left: 0.6em;
    margin-right: 0.6em;
    width: 99%;
    max-height: 30%;
    overflow: scroll;
  }
  #matchesTitle {
    font-weight: bold;
    font-size: 18px;
    margin-top: 0.4em;
  }
  #findingsDiv {
    background-color: rgb(248, 249, 250);
  }
  #matchesDiv {
    background-color: rgb(248, 249, 250);
  }
  #findHead {
    display: inline;
  }
  #findSearch {
    max-width: 40%;
    float: right;
    margin-right:1em;
    height: 2.5em;
    margin-top:0.5em;
  }
  #findEditYes, #findEditNo, #findEditMaybe {
    margin-right:0.5em;
    margin-left:0.5em;
  }
  #botButs {
    margin-left:0.5em;
    margin-right:0.5em;
  }
  #nbqYes, #nbqNo, #nbqMaybe {
    margin-right:0.5em;
    margin-left:0.5em;
  }
  #nbqBut {
    margin-left: 0.4em;
    margin-top: 0.4em;
  }
  .accordion {
    width: 99%
  }
  .accordion-item {
    margin-left:1em;
  }
  .accordion-body {
    background-color: rgb(248, 249, 250);
  }
  #lalBot {
    float: left;
    margin-left: 0.4em;
  }
  #ralBot {
    float: right;
    margin-right: 0.6em;
    margin-top: -0.35em;
  }
  #saveBut {
    margin-right: 0.5em;
  }
  #editNameBut {

  }
  #resetBut {
    margin-top: 0.3em;
  }
  #backBut {
    margin-left: 0.5em;
    margin-top: -0.5em;
  }
</style>
    