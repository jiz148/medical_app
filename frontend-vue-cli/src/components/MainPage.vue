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
      
      <div id="visitNameDiv">
        <a id="visitNameA">{{ curVisit.displaynote}} </a>
        <button type="button" id="" class="btn btn-link" @click="createEditNote"><i class="bi bi-pencil-square"></i></button>
      </div>
      

      <div id="ralTop">
        <button id="infoBut" class="btn btn-outline-secondary" @click="this.showInfo=!this.showInfo"><i class="bi bi-info-lg"></i></button>
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
              Current Findings
            </button>
          </div>
          <div id="currentFindBody" class="accordion-collapse collapse show" aria-labelledby="currentFindHead" data-bs-parent="#tableAccordion1">
            <div class="accordion-body">
              <div class="findingsBBody">
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
                      <td><button type="button" class="btn btn-link" @click="createEditFind(item)"><i class="bi bi-pencil-square"></i></button></td>
                      <td><input class="form-check-input" type="checkbox" v-model="item.checked" @change="getDiseases"></td>
                      <td><button type="button" class="btn btn-link" @click="createDeleteFind(item)"><i class="bi bi-x-square"></i></button></td>
                    </tr>
                </tbody>
              </table>
              </div>
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
              <input type="text" class="form-control" id="findSearch" v-model="findSearch" @input="searchFindings" placeholder="Search top findings">
              <button id="nbqBut" class="btn btn-primary" type="submit" @click="getNbq"><i class="bi bi-chat-right-quote-fill"></i></button>
              <div class="findingsBBody">
              <table id="findings" class="table table-striped table-hover align-middle table-sm">
                <thead>
                  <tr>
                    <th scope="col">#</th>
                    <th scope="col">Question</th>
                    <th scope="col"></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in searchedFindings" :key="item.id" @click="createNewFind(item)">
                    <td>{{item.id}}</td>
                    <td>{{item.Name}}</td>
                    <td><button type="button" class="btn btn-link" @click="createNewFind(item)"><i class="bi bi-circle-square"></i></button></td>
                    <td><a v-if="item.URL!=''" :href="item.URL" target="_blank" class="button btn btn-link"><i class="bi bi-info-square"></i></a></td>
                  </tr>
                </tbody>
              </table>
              </div>
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
              <div class="findingsBBody">
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
                    <td>{{item.id}}</td>
                    <td>{{item.Name}}</td>
                    <td><a v-if="item.URL!=''" :href="item.URL" target="_blank" class="button btn btn-link"><i class="bi bi-info-square"></i></a></td>
                  </tr>
                </tbody>
              </table>
              </div>
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
                <a v-if="editFindQuestion!=null" style="font-size: 16px; font-weight: bold; margin-left: 0.4em;">
                  <a v-if="this.editFindQuestion.FID==3732 || this.editFindQuestion.FID==3738">
                    Sex
                  </a>
                  <a v-else-if="this.editFindQuestion.FID==3731 || this.editFindQuestion.FID==3735 || this.editFindQuestion.FID==3736">
                    Age
                  </a>
                  <a v-else>
                    {{editFindQuestion.Name}}
                  </a>
                </a>
                <br>
                <div v-if="editFindQuestion!=null">
                  <div v-if="this.editFindQuestion.FID==3732 || this.editFindQuestion.FID==3738">
                    <input class="form-check-input" type="radio" name="flexRadioDefault" id="findEditYes" value="Male" v-model="editFindResp">
                    <label class="form-check-label" for="findEditYes">
                      Male
                    </label>
                    <input class="form-check-input" type="radio" name="flexRadioDefault" id="findEditNo" value="Female" v-model="editFindResp">
                    <label class="form-check-label" for="findEditNo">
                      Female
                    </label>
                  </div>
                  <div v-else-if="this.editFindQuestion.FID==3731 || this.editFindQuestion.FID==3735 || this.editFindQuestion.FID==3736">
                    <input class="form-check-input" type="radio" name="flexRadioDefault" id="findEditYes" value="16 to 25" v-model="editFindResp">
                    <label class="form-check-label" for="findEditYes">
                      16 to 25
                    </label>
                    <input class="form-check-input" type="radio" name="flexRadioDefault" id="findEditNo" value="26 to 55" v-model="editFindResp">
                    <label class="form-check-label" for="findEditNo">
                      26 to 55
                    </label>
                    <input class="form-check-input" type="radio" name="flexRadioDefault" id="findEditMaybe" value="56+" v-model="editFindResp">
                    <label class="form-check-label" for="findEditMaybe">
                      56+
                    </label>
                  </div>
                  <div v-else>
                    <input class="form-check-input" type="radio" name="flexRadioDefault" id="findEditYes" value="yes" v-model="editFindResp">
                    <label class="form-check-label" for="findEditYes">
                      Yes
                    </label>
                    <input class="form-check-input" type="radio" name="flexRadioDefault" id="findEditNo" value="no" v-model="editFindResp">
                    <label class="form-check-label" for="findEditNo">
                      No
                    </label>
                    <input class="form-check-input" type="radio" name="flexRadioDefault" id="findEditMaybe" value="unknown" v-model="editFindResp">
                    <label class="form-check-label" for="findEditMaybe">
                      Unknown
                    </label>
                  </div>
                </div>
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
                  <a v-if="nextBestQuestion!=null" style="font-size: 16px; font-weight: bold; margin-left: 0.4em;">
                    <a v-if="this.nextBestQuestion.FID==3732 || this.nextBestQuestion.FID==3738">
                      Sex
                    </a>
                    <a v-else-if="this.nextBestQuestion.FID==3731 || this.nextBestQuestion.FID==3735 || this.nextBestQuestion.FID==3736">
                      Age
                    </a>
                    <a v-else>
                      {{nextBestQuestion.Name}}
                    </a>
                  </a>
                  <br>
                  <div v-if="nextBestQuestion!=null">
                    <div v-if="this.nextBestQuestion.FID==3732 || this.nextBestQuestion.FID==3738">
                      <input class="form-check-input" type="radio" name="flexRadioDefault" id="nbqYes" value="Male" v-model="nbqResp">
                      <label class="form-check-label" for="findEditYes">
                        Male
                      </label>
                      <input class="form-check-input" type="radio" name="flexRadioDefault" id="nbqNo" value="Female" v-model="nbqResp">
                      <label class="form-check-label" for="findEditNo">
                        Female
                      </label>
                    </div>
                    <div v-else-if="this.nextBestQuestion.FID==3731 || this.nextBestQuestion.FID==3735 || this.nextBestQuestion.FID==3736">
                      <input class="form-check-input" type="radio" name="flexRadioDefault" id="nbqYes" value="16 to 25" v-model="nbqResp">
                      <label class="form-check-label" for="findEditYes">
                        16 to 25
                      </label>
                      <input class="form-check-input" type="radio" name="flexRadioDefault" id="nbqNo" value="26 to 55" v-model="nbqResp">
                      <label class="form-check-label" for="findEditNo">
                        26 to 55
                      </label>
                      <input class="form-check-input" type="radio" name="flexRadioDefault" id="nbqMaybe" value="56+" v-model="nbqResp">
                      <label class="form-check-label" for="findEditMaybe">
                        56+
                      </label>
                    </div>
                    <div v-else>
                      <input class="form-check-input" type="radio" name="flexRadioDefault" id="nbqYes" value="yes" v-model="nbqResp">
                      <label class="form-check-label" for="findEditYes">
                        Yes
                      </label>
                      <input class="form-check-input" type="radio" name="flexRadioDefault" id="nbqNo" value="no" v-model="nbqResp">
                      <label class="form-check-label" for="findEditNo">
                        No
                      </label>
                      <input class="form-check-input" type="radio" name="flexRadioDefault" id="nbqMaybe" value="unknown" v-model="nbqResp">
                      <label class="form-check-label" for="findEditMaybe">
                        Unknown
                      </label>
                    </div>
                  </div>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" :disabled="nbqResp==null" class="btn btn-success" @click="confirmNbq">Update</button>
                <button type="button" class="btn btn-danger" data-dismiss="modal" @click="closeNbq">Cancel</button>
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
                <a v-if="newFindQuestion!=null" style="font-size: 16px; font-weight: bold; margin-left: 0.4em;">
                  <a v-if="this.newFindQuestion.FID==3732 || this.newFindQuestion.FID==3738">
                    Sex
                  </a>
                  <a v-else-if="this.newFindQuestion.FID==3731 || this.newFindQuestion.FID==3735 || this.newFindQuestion.FID==3736">
                    Age
                  </a>
                  <a v-else>
                    {{newFindQuestion.Name}}
                  </a>
                </a>
                <br>
                <div v-if="newFindQuestion!=null">
                  <div v-if="this.newFindQuestion.FID==3732 || this.newFindQuestion.FID==3738">
                    <input class="form-check-input" type="radio" name="flexRadioDefault" id="findEditYes" value="Male" v-model="newFindResp">
                    <label class="form-check-label" for="findEditYes">
                      Male
                    </label>
                    <input class="form-check-input" type="radio" name="flexRadioDefault" id="findEditNo" value="Female" v-model="newFindResp">
                    <label class="form-check-label" for="findEditNo">
                      Female
                    </label>
                  </div>
                  <div v-else-if="this.newFindQuestion.FID==3731 || this.newFindQuestion.FID==3735 || this.newFindQuestion.FID==3736">
                    <input class="form-check-input" type="radio" name="flexRadioDefault" id="findEditYes" value="16 to 25" v-model="newFindResp">
                    <label class="form-check-label" for="findEditYes">
                      16 to 25
                    </label>
                    <input class="form-check-input" type="radio" name="flexRadioDefault" id="findEditNo" value="26 to 55" v-model="newFindResp">
                    <label class="form-check-label" for="findEditNo">
                      26 to 55
                    </label>
                    <input class="form-check-input" type="radio" name="flexRadioDefault" id="findEditMaybe" value="56+" v-model="newFindResp">
                    <label class="form-check-label" for="findEditMaybe">
                      56+
                    </label>
                  </div>
                  <div v-else>
                    <input class="form-check-input" type="radio" name="flexRadioDefault" id="findEditYes" value="yes" v-model="newFindResp">
                    <label class="form-check-label" for="findEditYes">
                      Yes
                    </label>
                    <input class="form-check-input" type="radio" name="flexRadioDefault" id="findEditNo" value="no" v-model="newFindResp">
                    <label class="form-check-label" for="findEditNo">
                      No
                    </label>
                    <input class="form-check-input" type="radio" name="flexRadioDefault" id="findEditMaybe" value="unknown" v-model="newFindResp">
                    <label class="form-check-label" for="findEditMaybe">
                      Unknown
                    </label>
                  </div>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" :disabled="newFindResp==null" class="btn btn-success" @click="makeNewFind">Confirm</button>
              <button type="button" class="btn btn-danger" data-dismiss="modal" @click="closeNewFind">Cancel</button>
            </div>
          </div>
        </div>
      </div>

      <div id="deleteFindModal" class="modal" tabindex="-1" role="dialog" aria-labelledby="deleteFindLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="deleteFindLabel">Delete Finding</h5>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <a v-if="editFindQuestion!=null" style="font-size: 16px; font-weight: bold; margin-left: 0.4em;">
                  <a v-if="this.editFindQuestion.FID==3732 || this.editFindQuestion.FID==3738">
                   <a style='font-weight: normal'>Would you like to remove your </a>
                   sex?
                  </a>
                  <a v-else-if="this.editFindQuestion.FID==3731 || this.editFindQuestion.FID==3735 || this.editFindQuestion.FID==3736">
                   <a style='font-weight: normal'> Would you like to remove your </a>
                    age?
                  </a>
                  <a v-else>
                   <a style='font-weight: normal'> Would you like to delete </a>
                    {{editFindQuestion.Name}}?
                  </a>
                </a>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-success" @click="makeDeleteFind">Confirm</button>
              <button type="button" class="btn btn-danger" data-dismiss="modal" @click="closeDeleteFind">Cancel</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <br>
    <div id="bot">
      <div id="botButs">
        <div id="lalBot">
          <button id="saveBut" class="btn btn-primary btn-sm" type="submit" @click="save">Save</button>
          <button id="revertBut" class="btn btn-outline-primary btn-sm" type="submit" @click="getCurrentFindings">Revert</button>
        </div>
        <div id="ralBot">
          <button id="resetBut" class="btn btn-outline-secondary btn-sm" type="submit" @click="reset">Reset</button>
          <button id="backBut" class="btn btn-secondary btn-sm" type="submit" @click="$router.go(-1)">Back</button>
        </div>
      </div>

      
      </div>
      <div id="editNoteModal" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="editNoteLabel" aria-hidden="true" data-backdrop="false">
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
        if(this.$route.query.visit > 0) {
          url = "http://jinchispace.com:5001/visit";
          await fetch(url, { //executes the query with a promise to get around asynchronous javascript behavior
                method: 'GET',
                credentials: "include",
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json;charset=UTF-8',
                    "Set-Cookie": "test=value; Path=/; Secure; SameSite=None;",
                    'Access-Control-Allow-Origin': 'jinchispace.com:5001',
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
                            let disp = li[i].note;
                            if(disp.length > 20) {
                              disp = disp.substring(0,17) + "...";
                            }
                            this.curVisit['displaynote'] = disp;
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
          this.curVisit = {'note': "New Visit", 'displaynote': 'New Visit', 'visit_id': 0, 'datetime': ""};
          this.loadVisit();
        }
    },
    updated: function() { //gets called after a change in the dom
      this.aslock += 1;
      let asv = this.aslock;
      setTimeout(() => { //wait x seconds before running the code in this block
        if(asv == this.aslock) { //if aslock has not been changed then we are good to autosave
          this.save(); //otherwise a more recent change has been made, so we should not autosave
        }
      }, 30000); //30 sec
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
            curVisit: {'note': 'New Visit', 'displaynote': 'New Visit', 'visit_id': 0, 'datetime': ""},
            findingsList: [
              
            ],
            searchedFindings: [
              
            ],
            currentFindings: [
              
            ],
            matchesList: [
              
            ],
            findSearch: "",
            editFindQuestion: null,
            editFindResp: null,
            newFindQuestion: null,
            newFindResp: null,
            nextBestQuestion: null,
            nbqResp: null,
            newNodeVal: "",
            aslock: 0
        }
    },
    methods: {
      logout: function() {
        let url = "http://jinchispace.com:5001/user/logout";
        fetch(url, { //executes the query with a promise to get around asynchronous javascript behavior
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
        console.log("start")
        this.getCurrentFindings();
        return 0;
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
        //this.editFindResp = item.answer;
        switch(item.FID) {
          case 3732: this.editFindResp = "Male"; break;
          case 3738: this.editFindResp = "Female"; break;
          case 3731: this.editFindResp = "26 to 55"; break;
          case 3735: this.editFindResp = "16 to 25"; break;
          case 3736: this.editFindResp = "56+"; break;
          default: this.editFindResp = item.answer; break;
        }
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
        this.getDiseases();
      },
      makeEditFind: function() {
        if(this.editFindQuestion == null) {
          return;
        }
        if(this.editFindQuestion.FID == 3732 || this.editFindQuestion.FID == 3738) { //gender
          for(let i=0;i<this.currentFindings.length;i++) {
            if(this.currentFindings[i].FID == 3732 || this.currentFindings[i].FID == 3738) {
              if(this.editFindResp == "Male") {
                this.currentFindings[i].answer = "yes";
                this.currentFindings[i].FID = 3732;
                this.currentFindings[i].Name = "Sex Male";
              } else {
                this.currentFindings[i].answer = "yes";
                this.currentFindings[i].FID = 3738;
                this.currentFindings[i].Name = "Sex Female";
              }
              this.closeEditFind();
              break;
            }
          }
        } else if(this.editFindQuestion.FID == 3731 || this.editFindQuestion.FID == 3735 || this.editFindQuestion.FID == 3736) { //age
          for(let i=0;i<this.currentFindings.length;i++) {
            if(this.currentFindings[i].FID == 3731 || this.currentFindings[i].FID == 3735 || this.currentFindings[i].FID == 3736) {
              if(this.editFindResp == "16 to 25") {
                this.currentFindings[i].answer = "yes";
                this.currentFindings[i].FID = 3735;
                this.currentFindings[i].Name = "Age 16 to 25";
              } else if(this.editFindResp == "26 to 55") {
                this.currentFindings[i].answer = "yes";
                this.currentFindings[i].FID = 3731;
                this.currentFindings[i].Name = "Age 26 to 55";
              } else {
                this.currentFindings[i].answer = "yes";
                this.currentFindings[i].FID = 3736;
                this.currentFindings[i].Name = "Age Gtr Than 55";
              }
              this.closeEditFind();
              break;
            }
          }
        } else {
          for(let i=0;i<this.currentFindings.length;i++) {
            if(this.currentFindings[i].FID == this.editFindQuestion.FID) {
              this.currentFindings[i].answer = this.editFindResp;
              this.closeEditFind();
              break;
            }
          }
        }
        this.closeEditFind();
      },
      createNewFind: function(item) {
        this.newFindQuestion = item;
        this.newFindResp = null;//item.answer;
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
        this.getDiseases();
      },
      makeNewFind: function() {
        let ob = {};
        let id = 1;
        if(this.newFindResp != null) {
          for(let i=0; i<this.searchedFindings.length; i++) {
            if(this.searchedFindings[i].FID == this.newFindQuestion.FID) {
              this.searchedFindings.splice(i, 1);
            }
          }
          if(this.newFindQuestion.FID == 3732 || this.newFindQuestion.FID == 3738) { //gender
            for(let i=0;i<this.currentFindings.length;i++) {
              if(this.currentFindings[i].FID == 3732 || this.currentFindings[i].FID == 3738) {
                if(this.newFindResp == "Male") {
                  this.currentFindings[i].FID = 3732;
                  this.currentFindings[i].Name = "Sex Male";
                } else {
                  this.currentFindings[i].FID = 3738;
                  this.currentFindings[i].Name = "Sex Female";
                }
                this.currentFindings[i].answer = "yes";//this.newFindResp;
                this.closeNewFind();
                return;
              }
            }
          } else if(this.newFindQuestion.FID == 3731 || this.newFindQuestion.FID == 3735 || this.newFindQuestion.FID == 3736) { //age
            for(let i=0;i<this.currentFindings.length;i++) {
              if(this.currentFindings[i].FID == 3731 || this.currentFindings[i].FID == 3735 || this.currentFindings[i].FID == 3736) {
                if(this.newFindResp == "16 to 25") {
                  this.currentFindings[i].FID = 3735;
                  this.currentFindings[i].Name = "Age 16 to 25";
                } else if(this.newFindResp == "26 to 55") {
                  this.currentFindings[i].FID = 3731;
                  this.currentFindings[i].Name = "Age 26 to 55";
                } else {
                  this.currentFindings[i].FID = 3736;
                  this.currentFindings[i].Name = "Age Gtr Than 55";
                }
                this.currentFindings[i].answer = "yes";//this.newFindResp;
                this.closeNewFind();
                return;
              }
            }
          } else {
            //console.log(this.newFindQuestion);
            for(let i=0;i<this.currentFindings.length;i++) {
              //console.log(this.currentFindings[i]);
              if(this.currentFindings[i].FID == this.newFindQuestion.FID) {
                this.currentFindings[i].answer = this.newFindResp;
                this.closeNewFind();
                return;
              }
            }
          }
          if(this.currentFindings.length > 0) {
            id =  this.currentFindings[this.currentFindings.length-1].id + 1;
          }
          if(this.newFindQuestion.FID == 3732 || this.newFindQuestion.FID == 3738) {
            if(this.newFindResp == "Male") {
              ob.FID = 3732;
              ob.Name = "Sex Male";
            } else {
              ob.FID = 3738;
              ob.Name = "Sex Female";
            }
            ob['answer'] = "yes";
          } else if(this.newFindQuestion.FID == 3731 || this.newFindQuestion.FID == 3735 || this.newFindQuestion.FID == 3736) {
            if(this.newFindResp == "16 to 25") {
              ob.FID = 3735;
              ob.Name = "Age 16 to 25";
            } else if(this.newFindResp == "26 to 55") {
              ob.FID = 3731;
              ob.Name = "Age 26 to 55";
            } else {
              ob.FID = 3736;
              ob.Name = "Age Gtr Than 55";
            }
            ob.answer = "yes";//this.newFindResp;
          } else {
            ob['FID'] = this.newFindQuestion.FID;
            ob['answer'] = this.newFindResp;
            ob['Name'] = this.newFindQuestion.Name; 
          }
          ob['id'] = id
          ob['checked'] = true
          this.currentFindings.push(ob);
          this.closeNewFind();
        }
      },
      createDeleteFind: function(item) {
        this.editFindQuestion = item;
        /*eslint-disable */
        //suppress all warnings between comments
        $('#deleteFindModal').modal('show'); //need to do this disable because eslint doesnt understand jquery for some reason
        /*eslint-enable */
      },
      closeDeleteFind: function() {
        //this.editFindQuestion = null;
        /*eslint-disable */
        //suppress all warnings between comments
        $('#deleteFindModal').modal('hide'); //need to do this disable because eslint doesnt understand jquery for some reason
        /*eslint-enable */
        this.getDiseases();
      },
      makeDeleteFind: function() {
        for(let i=0;i<this.currentFindings.length;i++) {
          if(this.currentFindings[i].FID == this.editFindQuestion.FID) {
            this.currentFindings.splice(i,1);
          }
        }
        this.closeDeleteFind();
      },
      getNbq: function() {
        let url = "http://jinchispace.com:5001/finding/nbq";
        let fidlist = this.currentFindings;//[]
        /*console.log(this.currentFindings[0]);
        for(let i=0;i<this.currentFindings.length;i++) {
          if(this.currentFindings[i].checked) {
            fidlist.push(this.currentFindings[i].FID);
          }
        }*/
        if(fidlist.length < 1) {
          fidlist = [{}];
        }
            fetch(url, { //executes the query with a promise to get around asynchronous javascript behavior
                method: 'POST',
                credentials: "include",
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json;charset=UTF-8',
                    "Set-Cookie": "test=value; Path=/; Secure; SameSite=None;",
                    'Access-Control-Allow-Origin': 'jinchispace.com:5001',
                    'Access-Control-Allow-Credentials': true,
                },
                body: JSON.stringify({
                    "top_disease_id": this.matchesList[0].DID,
                    "current_findings": fidlist
                })
                })
                .then((response) => { 
                    this.status = response.status;
                    return response.json() 
                })
                .then(data => {
                    this.response = data; 
                    if(this.response.msg == 'success') {
                        this.nextBestQuestion = data.data //for testing
                        this.nbqResp = null;
                        /*eslint-disable */
                        //suppress all warnings between comments
                        $('#nbqModal').modal('show'); //need to do this disable because eslint doesnt understand jquery for some reason
                        /*eslint-enable */
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
        //send request to get next best question
      },
      confirmNbq: function() {
        if(this.nbqResp != null) {
          //send request
          //get back request and update table
          if(this.nextBestQuestion.FID == 3732 || this.nextBestQuestion.FID == 3738) { //gender
            if(this.nbqResp == "Male") {
              this.nextBestQuestion.FID = 3732;
              this.nextBestQuestion.Name = "Sex Male";
            } else if(this.nbqResp == "Female") {
              this.nextBestQuestion.FID = 3738;
              this.nextBestQuestion.Name = "Sex Female";
            }
            this.nbqResp = "yes";
          } else if(this.nextBestQuestion.FID == 3731 || this.nextBestQuestion.FID == 3735 || this.nextBestQuestion.FID == 3736) {
            if(this.nbqResp == "16 to 25") {
              this.nextBestQuestion.FID = 3735;
              this.nextBestQuestion.Name = "Age 16 to 25";
            } else if(this.nbqResp == "26 to 55") {
              this.nextBestQuestion.FID = 3731;
              this.nextBestQuestion.Name = "Age 26 to 55";
            } else {
              this.nextBestQuestion.FID = 3736;
              this.nextBestQuestion.Name = "Age Gtr Than 55";
            }
            this.nbqResp = "yes";
          }
          this.nextBestQuestion.answer = this.nbqResp;
          this.nextBestQuestion.checked = true;
          this.currentFindings.push(this.nextBestQuestion);
          //console.log(this.currentFindings);
          this.closeNbq();
          this.getDiseases();
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
        let url = "http://jinchispace.com:5001/finding/finding_search";
        let fidlist = this.currentFindings;//[]
        //console.log(this.currentFindings[0]);
        /*for(let i=0;i<this.currentFindings.length;i++) {
          if(this.currentFindings[i].checked) {
            //console.log(this.currentFindings[i]);
            fidlist.push(this.currentFindings[i].FID);
          }
        }*/
        if(fidlist.length < 1) {
          fidlist = [{}];
        }
        fetch(url, { //executes the query with a promise to get around asynchronous javascript behavior
                method: 'POST',
                credentials: "include",
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json;charset=UTF-8',
                    "Set-Cookie": "test=value; Path=/; Secure; SameSite=None;",
                    'Access-Control-Allow-Origin': 'jinchispace.com:5001',
                    'Access-Control-Allow-Credentials': true,
                },
                body: JSON.stringify({
                    "keyword": this.findSearch,
                    "current_findings": fidlist
                })
                })
                .then((response) => { 
                    this.status = response.status;
                    return response.json() 
                })
                .then(data => {
                    this.response = data; 
                    if(this.response.msg == 'success') {
                        //console.log(data.data.length);
                        let id = 1;
                        this.searchedFindings = data.data;
                        for(let i=0;i<this.searchedFindings.length;i++) {
                          this.searchedFindings[i]['id'] = id;
                          console.log(this.searchedFindings[i]['URL']);
                          if(this.searchedFindings[i]['URL'] != "") {
                            this.searchedFindings[i]['URL'] = "https://www.saedsayad.com/winnbq/" + this.searchedFindings[i]['URL'];
                          }
                          id += 1;
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
        /*let na = [];
        for(let i=0;i<this.findingsList.length;i++) {
          if(this.findingsList[i].Name.toLowerCase().includes(this.findSearch.toLowerCase())) {
            na.push(this.findingsList[i])
          }
        }
        this.searchedFindings = na;*/
      },
      toggleMessage: function() {
        this.show = !this.show;
      },
      getDiseases: async function() {
        let url = "http://jinchispace.com:5001/disease/top_diseases";
        let fidlist = this.currentFindings; //[]
        //console.log(this.currentFindings[0]);
        /*for(let i=0;i<this.currentFindings.length;i++) {
          if(this.currentFindings[i].checked) {
            //console.log(this.currentFindings[i]);
            fidlist.push(this.currentFindings[i]);
          }
        }*/
        if(fidlist.length < 1) {
          fidlist = [{}];
        }
        //console.log(fidlist);
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
                body: JSON.stringify({
                    "current_findings": fidlist
                })
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
                        for(let i=0;i<data.data.length;i++) {
                          let ob = data.data[i];
                          ob['id'] = id;
                          //ob['link'] = "https://www.google.com";
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
        let url = "http://jinchispace.com:5001/finding";
            fetch(url, { //executes the query with a promise to get around asynchronous javascript behavior
                method: 'POST',
                credentials: "include",
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json;charset=UTF-8',
                    "Set-Cookie": "test=value; Path=/; Secure; SameSite=None;",
                    'Access-Control-Allow-Origin': 'jinchispace.com:5001',
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
                        //console.log(this.currentFindings);
                        this.getDiseases();
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
        /*let vid = this.curVisit.visit_id;
        //this.curVisit.visit_id = 0;
        await this.loadVisit();
        this.curVisit.visit_id = vid;*/
      },
      save: async function() {
        this.showAlert = false;
        this.showError = false;
        let suc = false;
        //do query, probably as async await
        if(this.curVisit.visit_id == 0) { //new visit, create visit
          let url = "http://jinchispace.com:5001/visit";
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
          let fidlist = this.currentFindings;//[]
          /*console.log(this.currentFindings[0]);
          for(let i=0;i<this.currentFindings.length;i++) {
            if(this.currentFindings[i].checked) {
              fidlist.push(this.currentFindings[i].FID);
            }
          }*/
          if(fidlist.length < 1) {
            fidlist = [{}];
          }
          let url = "http://jinchispace.com:5001/visit";
          await fetch(url, { //executes the query with a promise to get around asynchronous javascript behavior
            method: 'PUT',
            credentials: "include",
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json;charset=UTF-8',
                "Set-Cookie": "test=value; Path=/; Secure; SameSite=None;",
                'Access-Control-Allow-Origin': 'jinchispace.com:5001',
                'Access-Control-Allow-Credentials': true,
            },
            body:  JSON.stringify({
                'visit_id': this.curVisit.visit_id,
                'note': this.curVisit.note,
                'current_findings': fidlist
            })
            })
            .then((response) => { 
                this.status = response.status;
                return response.json() 
            })
            .then(data => {
                this.response = data; 
                if(this.status == 200) {
                    console.log(this.response); //seems like the query isnt passing back the right visit
                    //this.curVisit = this.response.result[this.response.index];
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
        this.newNodeVal = this.curVisit.note;
        //document.getElementById("currentFindHead").click();
        //document.getElementById("currentFindBody").collapse('show');
        /*eslint-disable */
        //suppress all warnings between comments
        //setTimeout(() => {$('#currentFindBody').collapse('show');}, 400);
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
          let disp = "";
          if(this.newNodeVal.length > 20) {
            disp = this.newNodeVal.substring(0,17) + "...";
          } else {
            disp = this.newNodeVal
          }
          this.curVisit.displaynote = disp;
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
  flex: 1 0 auto;
  margin-top: 0.4em;
  margin-bottom: 0.4em;
}
#middle {
  background-color: rgb(235,236,237);
  flex: 0 1 47.5em;
  font-weight: normal;
  font-size: 14px;
  overflow-y: scroll;
  padding-bottom: 1em;
}
#bot {
  background-color: white;
  font-weight: normal;
  font-size: 14px;
  position: fixed;
  bottom:0;
  width:100%;
  flex: 0 0 2em;
  z-index: 999;
  padding-top: 1em;
  padding-bottom: 1em;
}
#ralTop {
  float: right;
  display: inline;
}
#infoBut {
  margin-right: 0.6em;
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
  .findingsBBody {
    overflow-y: scroll; 
    overflow-x: hidden;
    max-height: 20em;
    width: 100%;
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
    overflow-y: scroll;
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
    max-width: 77%;
    float: right;
    margin-right:1em;
    height: 2.5em;
    margin-top:0.35em;
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
    float: right;
    margin-right: 0.4em;
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
    margin-top: 0.3em;
  }
  #saveBut {
    margin-bottom: 0.6em;
    margin-right: 0.5em;
  }
  #revertBut {
    margin-right: 0.5em;
  }
  #editNameBut {

  }
  #resetBut {
    margin-top: 0.3em;
    margin-right: 0.5em;
  }
  #backBut {
    margin-left: 0.5em;
    margin-top: -0.5em;
  }
  #renameIcon {
    margin-top: -5em;
    position:relative; 
    left: 18em; 
    top: 4.375em;
    z-index: 999;
  }
  #tableAccordion1 {
    
  }
  #editNoteModal {
    z-index: 9999
  }
  #visitNameDiv {
    position: relative;
    top: 0.1em;
    margin-left: 1.8em;
    display: inline;
  }
  #visitNameA {
    position: relative;
    top: 0.1em;
    font-size: 20px;
    color: #0275d8;
  }
</style>
    