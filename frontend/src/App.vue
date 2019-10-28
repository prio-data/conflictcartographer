<template>
   <div id="app">
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
   </div>
</template>

<script>

import Leaflet from './components/Leaflet.vue'
import Toolbar from "./components/Toolbar.vue"
import Navbar from "./components/Navbar.vue"

import Layer from "./models/layer.js"

export default {
   name: 'app',
   components: {
      Leaflet,
      Toolbar,
      Navbar,
   },

   methods: {
      pushData: function(){
         let payload  = this.$store.state.layers;
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
      let data = JSON.parse(JSON.parse(document.getElementById("dat").textContent));
      let layers = data.map(function(obj){
         let layer = new Layer(
            obj.fields.geometry,
            obj.fields.intensity,
            obj.fields.confidence
         );
         layer.pk = obj.pk;
         return layer;
      })

      layers.forEach((layer) => this.$store.commit("pushLayer",layer))

      this.$store.commit("initDjango",data);

   },
   delimiters: ["[[","]]"]
}
</script>

<style lang="sass">
#app 
  -webkit-font-smoothing: antialiased
  -moz-osx-font-smoothing: grayscale
  color: #2c3e50
  margin-right: 2vh

#navbar
   height: 10vh

#content
   height: 90vh 
</style>
