<template>
   <div id="app" class="container">
      <div id="navbar" class="row twelve columns"> 
         <Navbar title="Conflict Cartographer"/> 
      </div>
      <div id="content" class="row">
         <div id="mainwindow" class="nine columns">
            <Leaflet ref="mainmap"/>
         </div>
         <div id="sidebar" class="three columns">
            <Toolbar/>  
         </div>
      </div>
   </div>
</template>

<script>

import Leaflet from './components/Leaflet.vue'
import Toolbar from "./components/Toolbar.vue"
import Navbar from "./components/Navbar.vue"

export default {
   name: 'app',
   components: {
      Leaflet,
      Toolbar,
      Navbar,
   },
   mounted: function(){
      this.$refs.mainmap.initMap();
   }
}
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
