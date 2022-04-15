<template>
  <div id="disclaimer">
    <div id="dischead">
      Disclaimer
    </div>
    <div id="alert" class="card" v-show="showAlert">
      <div class="card-body">
        {{ alertMess }}
      </div>
    </div>
    <div id="error" class="card" v-show="showError">
      <div class="card-body">
        {{ errorMess }}
      </div>
    </div>
    <div id="message" class="card"> 
      <div class="card-body">
        This application is designed primarily as a reminder system for use by qualified physicians and other medical professionals. By using this site you understand and accept that this application shall not be used as a diagnostic decision-making system and must not be used to make a clinical diagnosis or replace or overrule a licensed health care professional's judgment or clinical diagnosis.
TO THE FULL EXTENT PERMISSIBLE UNDER THE APPLICABLE LAW, ISMARTSOFT INC SHALL NOT BE LIABLE FOR ANY DAMAGES OR EXPENSES OF ANY KIND, LOSS OF DATA, LOST REVENUE, LOSS OF USE, DIRECT, INDIRECT, INCIDENTAL, PUNITIVE LOSSES, SPECIAL OR CONSEQUENTIAL DAMAGES RESULTING FROM THE USE OR INABILITY TO USE THE SOFTWARE OR WHETHER ARISING IN TORT (INCLUDING NEGLIGENCE), CONTRACT OR ANY OTHER LEGAL THEORY, EVEN IF A PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
      </div>
    </div>
    <button id="button" class="btn btn-success" type="submit" @click="goregister" >Acknowledge</button>
    <button id="buttonclose" class="btn btn-danger" type="submit" @click="closeapp" >Reject</button>
  </div>
</template>

<script>
export default { //controls form input
    name: 'DisclaimerPage',
    props: {
        msg: String
    },
    data() {
      return {
        showError: false,
        errorMess: "",
        alertMess: "",
        showAlert: false
      }
    },
    beforeCreate: function() {
        
    },
    created: function() {
        this.alertMess = this.$route.query.msg;
        if(this.alertMess) {
            this.showAlert = true;
        }
        setTimeout(() => { 
          this.showAlert = false;
        }, 5000);
    },
    methods: {
        goregister() {
            let url = "http://jinchispace.com:5001/disclaimer";
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
                  this.$router.push('/login');
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
        closeapp() {
          this.errorMess = "You must acknowledge the disclaimer to proceed.";
          this.showError = true;
        }
    }
}
</script>


<style>
  #dischead {
    color: rgb(255, 10, 67);
    margin-left: 0.6em;
    margin-top: 0.4em;
    margin-bottom: 0.2em;
  }
  #message {
    font-size: 14px;
    font-weight: normal;
    margin-top: 0.2em;
    margin-bottom: 0.2em;
    margin-left: 0.6em;
    margin-right: 0.6em;
  }
  #button {
    margin-left: 0.6em;
    margin-top: 0.3em;
    display: inline-block;
  }
  #buttonclose {
    margin-left: 0.2em;
    margin-top: 0.3em;
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
</style>
