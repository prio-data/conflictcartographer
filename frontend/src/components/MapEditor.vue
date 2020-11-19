<template>
   <div id="mapeditor" class="row">
      <div v-if="projectShape">
         <div id="mainwindow">
            <Leaflet id="map"
               v-on:created="created"
               :layers="layers"
               :infocus="infocus"
               :mask="projectShape"
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
         infocus: "",
         layers: [],
         projectShape: undefined 
      }
   },

   mounted: function(){
      this.$store.state.api.get.abs(this.project.url)
         .then((r)=>{
            this.projectShape = r.data.shape
            this.$store.state.api.get.rel("shapes",{params: {country: this.project.gwno}})
               .then((r)=>{
                  this.layers = r.data
               })
               .catch((e)=>{
                  console.log(e)
               })

         })
         .catch((e)=>{
            console.log(e)
         })
   },

   methods: {
      deleteLayer(layer){
         let i = this.layers.indexOf(this.layers.find((lyr)=>lyr.url == layer.url))
         if(i > -1){
            this.layers.splice(i,1)
         } else {
            console.log(i)
         }
      },

      created(feature){
         let toPost = {
            shape: feature, 
            values: {
               intensity: this.$store.state.defaultIntensity,
               confidence: this.$store.state.defaultConfidence,
            },
            country: this.project.url 
         }

         this.$store.state.api.post.rel("shapes",{data:toPost})
            .then((r)=>{
               toPost.url = r.data
               this.layers.push(toPost)
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
