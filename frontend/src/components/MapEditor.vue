<template>
   <div id="mapeditor" class="row">
      <div id="mainwindow">
         <Leaflet
            v-if="projectDetails"
            /> 
         <div class="loadingwrapper"
            v-else>
            <div style="display:inline-block">
               <div class="lds-default">
                  <div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div>
               </div>
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

.lds-default 
  display: inline-block
  position: relative
  width: 64px
  height: 64px

.lds-default div 
  position: absolute
  width: 5px
  height: 5px
  background: #fff
  border-radius: 50%
  animation: lds-default 1.2s linear infinite

.lds-default div:nth-child(1) 
  animation-delay: 0s
  top: 29px
  left: 53px

.lds-default div:nth-child(2) 
  animation-delay: -0.1s
  top: 18px
  left: 50px

.lds-default div:nth-child(3) 
  animation-delay: -0.2s
  top: 9px
  left: 41px

.lds-default div:nth-child(4) 
  animation-delay: -0.3s
  top: 6px
  left: 29px

.lds-default div:nth-child(5) 
  animation-delay: -0.4s
  top: 9px
  left: 18px

.lds-default div:nth-child(6) 
  animation-delay: -0.5s
  top: 18px
  left: 9px

.lds-default div:nth-child(7) 
  animation-delay: -0.6s
  top: 29px
  left: 6px

.lds-default div:nth-child(8) 
  animation-delay: -0.7s
  top: 41px
  left: 9px

.lds-default div:nth-child(9) 
  animation-delay: -0.8s
  top: 50px
  left: 18px

.lds-default div:nth-child(10) 
  animation-delay: -0.9s
  top: 53px
  left: 29px

.lds-default div:nth-child(11) 
  animation-delay: -1s
  top: 50px
  left: 41px

.lds-default div:nth-child(12) 
  animation-delay: -1.1s
  top: 41px
  left: 50px

@keyframes lds-default 
  0%, 20%, 80%, 100% 
    transform: scale(1)
  
  50% 
    transform: scale(1.5)

.lds-default div
   background: $ui_highlight

.lds-default
   margin-left: 45vw
   margin-top: 35vh
</style>
