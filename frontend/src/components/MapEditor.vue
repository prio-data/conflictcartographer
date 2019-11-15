<template>
   <div id="mapeditor" class="row">
      <div id="mainwindow">
         <Leaflet
            v-if="projectDetails"
            /> 
         <div class="loadingwrapper"
            v-else>
            <div style="display:inline-block">
               <spinner/>
            </div> </div>
      </div>
      <div 
         v-if="projectDetails"
         id="toolbar">
         <Toolbar/> 
      </div>
   </div>
</template>

<script>

import Leaflet from './Leaflet.vue'
import Toolbar from "./Toolbar.vue"
import Navbar from "./Navbar.vue"
import spinner from "./eyecandy/spinner"

import {mapGetters} from "vuex"

export default {
   name: 'MapEditor',
   components: {
      Leaflet,
      Toolbar,
      Navbar,
      spinner,
   },
   
   props: ["project"],

   computed: {
      projectDetails(){
         return this.$store.state.projectDetails
      },
      ...mapGetters([
         "projectShape",
      ])

   },

   methods: {
   },

   mounted: function(){
      this.$store.dispatch("initializeLayers")
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
