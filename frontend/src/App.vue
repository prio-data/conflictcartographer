<template>
   <div id="app" class="container">
      <div id="navbar" class="row twelve columns"> 
         <Navbar title="Conflict Cartographer"/> 
      </div>
      <div id="content" class="row">
         <div id="mainwindow" class="nine columns">
            <Leaflet/> 
         </div>
         <div id="sidebar" class="three columns">
            <Toolbar v-on:pushData="pushData"/>  
         </div>
      </div>
      <div class="row">
         <debug v-bind:data="djangodata"/> 
         <debug v-bind:data="debugNotify"/> 
      </div>
   </div>
</template>

<script>

import Leaflet from './components/Leaflet.vue'
import Toolbar from "./components/Toolbar.vue"
import Navbar from "./components/Navbar.vue"
import Debug from "./components/Debug.vue"

export default {
   name: 'app',
   components: {
      Leaflet,
      Toolbar,
      Navbar,
      Debug,
   },

   data: function(){
   return {
      djangodata: JSON.parse(document.getElementById("dat").textContent),
   }},

   computed: {
      debugNotify: function(){
         return this.$store.state.debugNotify;
      }
   },

   methods: {
      pushData: function(){
         let payload  = {foo: "bar"};
         let csrfToken = this.$cookies.get("csrftoken");
         let config = {
            credentials: "include",
            headers: {"X-CSRFToken": csrfToken}
         };

         this.$http.post("/",payload,config).then(
               response => {window.location = response.url;},
               err => {this.$store.commit("notifyFailure", err["status"])
         })
         //this.$store.commit("pushData");
      },
   },

   mounted: function(){
      //this.$refs.mainmap.initMap();
      //this.map = this.$refs.mainmap.map;
      //this.layers = this.$refs.mainmap.layers;
      this.map = this.$refs.map;
      let djangodata = JSON.parse(document.getElementById("dat").textContent);
      this.$store.commit("initDjango",djangodata);
   },
   delimiters: ["[[","]]"]
}
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
