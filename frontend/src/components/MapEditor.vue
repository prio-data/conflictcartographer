<template>
   <div id="mapeditor" class="row">
      <div id="mainwindow">
         <Leaflet
            v-if="projectDetails"
            /> 
      </div>
      <div id="toolbar">
         <Toolbar/> 
      </div>
   </div>
</template>

<script>

import Leaflet from './Leaflet.vue'
import Toolbar from "./Toolbar.vue"
import Navbar from "./Navbar.vue"

// ?
import * as R from "ramda"

export default {
   name: 'MapEditor',
   components: {
      Leaflet,
      Toolbar,
      Navbar,
   },
   
   props: ["user","project"],

   computed: {
      projectDetails(){
         return this.$store.state.projectDetails;
      }
   },

   methods: {
   },

   mounted: function(){
      this.$store.dispatch("initializeLayers",
         {author: this.user,
          project: this.project.pk})
   },
}
</script>

<style scoped lang="sass">
@import "../sass/variables.sass"

#mapeditor
  -webkit-font-smoothing: antialiased
  -moz-osx-font-smoothing: grayscale
  color: #2c3e50

#mainwindow
   float: left
</style>
