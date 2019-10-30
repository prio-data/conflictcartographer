<template>
   <div id="app">
      <div id="navbar" class="row twelve columns"> 
         <Navbar title="Conflict Cartographer"/> 
      </div>
      <div id="content" class="row">
         <div id="mainwindow" class="nine columns">
            <Leaflet/> 
         </div>
         <div id="toolbar" class="three columns">
            <Toolbar/> 
         </div>
      </div>
   </div>
</template>

<script>

import Leaflet from './components/Leaflet.vue'
import Toolbar from "./components/Toolbar.vue"
import Navbar from "./components/Navbar.vue"

import Layer from "./models/layer.js"
import * as R from "ramda"

export default {
   name: 'app',
   components: {
      Leaflet,
      Toolbar,
      Navbar,
   },

   //data: function(){
   //},

   computed: {
   },

   methods: {
   },


   mounted: function(){
      const csrfToken = this.$cookies.get("csrftoken");

      const apiDef = {
         url: "/api",
         header: {credentials: "include",
            headers: {"X-CSRFToken": csrfToken}
         }
      }

      this.map = this.$refs.map;
      let sessionInfo = JSON.parse(document.getElementById("sessionInfo").textContent);
      this.$store.commit("updateSessionInfo",sessionInfo);

      this.$store.commit("initApi",apiDef)
      this.$store.commit("initializeLocations")
      this.$store.dispatch("initializeLayers",{})

      // Csrftoken for AJAX  

      // ****************************************************
      // This is deprecated

      //let data = JSON.parse(JSON.parse(document.getElementById("dat").textContent));

      //let layers = data.map(function(obj){
         //let layer = new Layer(
            //obj.fields.geometry,
            //obj.fields.intensity,
            //obj.fields.confidence
         //);
         //layer.pk = obj.pk;
         //return layer;
      //})

      //layers.forEach((layer) => this.$store.commit("pushLayer",layer))

      // ****************************************************
   },
   delimiters: ["[[","]]"]
}
</script>

<style lang="sass">
@import "./sass/variables.sass"

#app 
  -webkit-font-smoothing: antialiased
  -moz-osx-font-smoothing: grayscale
  color: #2c3e50
  margin-right: 2vh

#toolbar
   margin: $gaps 

#navbar
   height: 10vh

#content
   height: 90vh 

#map
   border-radius: 25px
</style>
