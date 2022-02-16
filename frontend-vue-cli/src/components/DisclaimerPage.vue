<template>
  <div id="disclaimer">
    <div id="dischead">
      Disclaimer
    </div>
    <div id="message" class="card"> 
      <div class="card-body">
        This application is designed primary as a reminder system for use by qualified physicians and other medical professionals.
        ... Didn't copy the rest, but it should be somewhere in the code the professor shared with us.
      </div>
    </div>
    <button id="button" class="btn btn-success" type="submit" @click="goregister" >Acknowledge</button>
    <button id="buttonclose" class="btn btn-danger" type="submit" @click="closeapp" >Reject</button>
  </div>
</template>

<script>
export default { //controls form input
    name: 'DisclaimerPage',
    props: {},
    methods: {
        goregister() {
            this.$router.push('/login');
        },
        closeapp() {
          //should quit the app, to be implemented
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
</style>
