<template>
   <div id="mapeditor" class="row">
      <div v-if="projectDetails">
            
         <div id="mainwindow">
            <Leaflet id="map"
               v-if="projectDetails"
               v-on:created="created"
               :layers="layers"
               :infocus="infocus"
               /> 
         </div>
         <div id="toolbarContainer">
            <div></div>
            <div id="toolbar">
               <h1>Drawn areas:</h1>
               <div v-for="layer in layers" v-bind:key="layer.url">
                  <LayerView
                     v-on:focus="focus"
                     v-on:deleted="deleteLayer(layer)" 
                     :layer="layer"/>
               </div>
            </div>
         </div>
      </div>
      <Spinner v-else/>
   </div>
</template>

<style scoped lang="sass">
@import "../sass/variables.sass"

$darken: 0.4

#mapeditor
  -webkit-font-smoothing: antialiased
  -moz-osx-font-smoothing: grayscale
  color: #2c3e50

#mainwindow
   float: left


h1
   color: white

div#toolbarContainer
   position: absolute
   top: 0
   right: 0
   display: grid
   grid-template-rows: $menu-el-height $map_height auto
   width: 300px
   margin: 0px

div#toolbar
   overflow-y: scroll
   background: rgba(0,0,0,$darken)
   padding: 0px $menu-gaps 0px $menu-gaps
   margin: 0px
</style>

<script>

//import Toolbar from "@/components/Toolbar.vue"

import Leaflet from '@/components/Leaflet.vue'
import Spinner from "@/components/Spinner"
import LayerView from "@/components/LayerView"

export default {
   name: 'MapEditor',
   components: {
      Leaflet,
      //Toolbar,
      Spinner,
      LayerView,
   },
   
   props: ["project"],

   data(){
      return {
         defaultValues: {
            intensity: 5,
            confidence: 5
         },
         infocus: "",
      }
   },

   computed: {
      projectDetails(){
         return this.$store.state.projectDetails
      },
      layers(){
         return this.$store.state.layers
      }
   },

   mounted: function(){
      this.$store.dispatch("initializeLayers")
   },

   methods: {
      deleteLayer(layer){
         let layers = this.$store.state.layers
         let i = layers.indexOf(layers.find((lyr)=>lyr.url == layer.url))
         if(i > -1){
            layers.splice(i,1)
         } else {
            console.log(i)
         }
      },

      created(feature){
         let state = this.$store.state
         //state.vizId ++

         let toPost = {
            shape: feature, 
            values: {
               intensity: state.defaultIntensity,
               confidence: state.defaultConfidence,
            },
            author: `${window.location}api/users/state.sessionInfo.uk/`,
            country: state.currentProject.url,
            //vizId: state.vizId
         }

         this.$store.state.api.gpost("shapes",toPost)
            .then((r)=>{
               toPost.url = r.data
               this.$store.state.layers.push(toPost)
            })
            .catch((e)=>{
            })
      },
      focus(layer){
         if(this.infocus == layer.url){
            this.infocus = ""
         } else {
            this.infocus = layer.url
         }
      },
   }
}
</script>
