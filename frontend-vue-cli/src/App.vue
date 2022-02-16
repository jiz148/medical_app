<template>
  <HelloWorld />
  <router-view></router-view>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  components: {
    HelloWorld
  }
}
</script>

<style>
#app {
    font-weight: bold;
    font-size: 18px;
    font-family: "Century Gothic";
    background-color: rgb(252, 255, 255);
  }
</style>
