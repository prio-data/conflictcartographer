<template>
   <div id="mapeditor">
      <div id="map"></div>
      <EditorOverlay 
         v-on:startdraw="startdraw"
         v-on:startdelete="startdelete"
         v-on:reset="neutral"
         :mode="mode"
         >
         <template v-if="mode===4 && selectedLayer !== undefined" v-slot:editor-panel>
            <LayerEditor :layer="selectedLayer"></LayerEditor>
         </template>
      </EditorOverlay>
      <HelptextOverlay>
         <h1>
            {{ this.helptexts[this.mode].title }}
         </h1>
         {{ this.helptexts[this.mode].text }}
      </HelptextOverlay>
   </div>
</template>

<style scoped lang="sass">
@import "../sass/variables.sass"

$darken: 0.4

#map
   height: 100vh
   width: 100vw

#mapeditor
  -webkit-font-smoothing: antialiased
  -moz-osx-font-smoothing: grayscale
  color: #2c3e50
</style>

<script>
//import {LMap, LGeoJson} from "vue2-leaflet"
import L from "leaflet"

import "leaflet-draw" 
import "leaflet-boundary-canvas"
import bbox from "geojson-bbox"

import colorGradient from "@/util/colorGradient.js"
import Spinner from "@/components/Spinner"
import EditorOverlay from "@/components/EditorOverlay"
import HelptextOverlay from "@/components/HelptextOverlay"
import LayerEditor from "@/components/LayerEditor"

import {configure_map,shape_to_latlng_box} from "@/configure_map"

import debounce from "@/util/debounce"

const COLORS={
   low: "#2b83ba",
   high: "#d7191c",
}

const MODES={
   neutral: 1,
   drawing: 2,
   deleting: 3,
   editing: 4
}

const HELPTEXTS={
   1: {
      title:"Data entry",
      text:"Click draw to begin",
   },
   2: {
      title:"Draw",
      text:"Draw a shape by clicking to place vertices.",
   },
   3: {
      title:"Erase",
      text:"Click shapes to erase them",
   },
   4: {
      title:"Editing",
      text:"Change the values of a shape",
   }
}

const BASE_STYLE = {
   fillOpacity: 0.3,
   opacity: 0.2,
   weight: 3
}

export default {
   name: 'MapEditor',
   components: {
      HelptextOverlay,
      EditorOverlay,
      Spinner,
      LayerEditor,
   },
   
   props: ["project"],

   data(){
      return {
         infocus: "",
         layers: [],

         projectShape: undefined,
         absUrl: undefined,

         map: undefined,

         drawnItems: new L.geoJSON(undefined),
         pendingItems: new L.featureGroup(),

         mode: MODES.neutral,

         selectedLayer: undefined,

         helptexts: HELPTEXTS,

         drawing: undefined,
      }
   },

   computed:{
      project_url(){
         return `countries/${this.$route.params.gwno}`
      },
      gwno(){
         return this.$route.params.gwno
      },
      selectedProps(){
         if(this.selectedLayer !== undefined){
            return this.selectedLayer.feature.properties
         }
      }
   },

   watch: {
      selectedProps: {
         handler(){
            this.updated(this.selectedLayer)
         },
         deep: true
      }
   },

   mounted: function(){
      // =======================================
      // When drawn,  

      this.$store.state.api.get.rel(this.project_url)
         .then((r)=>{
            this.projectShape = r.data.shape
            this.absUrl = r.data.url

            this.map = new L.Map("map")
            configure_map(this.map,this.projectShape)

            this.map.on(L.Draw.Event.CREATED,(e)=>{
               this.created(e.layer)
            })

            const box = bbox(this.projectShape)
            const getbox = (box) => [[box[3],box[0]],[box[1],box[2]]]
            const bbox_latlng = L.latLngBounds(getbox(box))

            this.map.fitBounds(bbox_latlng)
            this.map.setMaxBounds(bbox_latlng.pad(2))

            this.pendingItems.addTo(this.map)

            this.$store.state.api.get.rel("shapes",{params: {country: this.gwno}})
               .then((r)=>{
                  this.layers = r.data
                  let features = r.data.map((db_shape)=>{
                     let feature = db_shape.shape
                     feature.properties = db_shape.values 
                     feature.properties.url = db_shape.url
                     return feature 
                  })

                  this.drawnItems.addData(features)
                  this.drawnItems.addTo(this.map)

                  this.drawnItems.on("click",(e)=>{this.clicked(e.layer)})

                  this.restyle()
               })
               .catch((e)=>{
                  console.log(e)
               })

         })
         .catch((e)=>{
            console.log(e)
         })

         document.addEventListener("keydown",(e)=>{
            if(e.key=="Escape"){
               this.neutral()
            }
         })
   },

   methods: {
      neutral(){
         this.mode = MODES.neutral
         if(this.drawing !== undefined){
            this.drawing.disable()
         }
         this.selectedLayer.feature.properties.selected = undefined 
         this.restyle()
      },

      startdraw(){
         this.mode = MODES.drawing
         if(this.map !== undefined){
            this.drawing = new L.Draw.Polygon(this.map,{})
            this.drawing.enable()
         } else {
         }
      },

      startdelete(){
         this.mode = MODES.deleting 
      },

      clicked(layer){
         if(this.mode == MODES.deleting){
            this.deleted(layer)
         } else {
            this.selected(layer)
         }
      },

      deleted(layer){
         if(this.mode == MODES.deleting){
            this.drawnItems.removeLayer(layer)
            this.$store.state.api.del.abs(layer.feature.properties.url)
               .then((r)=>{
                  this.drawnItems.removeLayer(layer)
               })
               .catch((e)=>{
                  this.drawnItems.addLayer(layer)
               })
         }
      },

      created(layer){
         this.pendingItems.clearLayers()
         this.pendingItems.addLayer(layer.setStyle({color:"gray",opacity:0.5}))
         this.map.addLayer(this.pendingItems)

         let geojson = layer.toGeoJSON()
         let values = {
            intensity: this.$store.state.defaultIntensity,
            confidence: this.$store.state.defaultConfidence,
         }

         let toPost = {
            shape: geojson, 
            values: values,
            country: this.absUrl 
         }

         this.$store.state.api.post.rel("shapes",{data:toPost})
            .then((r)=>{
               geojson.properties = values
               geojson.properties.url = r.data.url

               this.drawnItems.addData(geojson)
               let newlyCreated = this.drawnItems.getLayers().find((lyr)=>lyr.feature.properties.url==r.data.url)
               this.map.removeLayer(this.pendingItems)
               this.selected(newlyCreated)
               this.restyle(newlyCreated)
            })
            .catch((e)=>{
               console.log(e)
            })
      },

      selected(layer){
         if(this.selectedLayer !== undefined){
            this.selectedLayer.feature.properties.selected = undefined
         }

         layer.feature.properties.selected = true
         this.selectedLayer = layer
         this.mode = MODES.editing

         this.restyle()
      },

      updated(layer){
         // API call
         this.restyle()

         let values ={
            intensity: layer.feature.properties.intensity,
            confidence: layer.feature.properties.confidence,
         }

         let to_post = {
            shape: layer.feature,
            values: values,
            country: this.absUrl,
         }

         this.post_update(layer.feature.properties.url,to_post)
      },

      post_update: debounce(function(url,data){
         this.$store.state.api.put.abs(url,{data:data})
            .then((r)=>{
               console.log(r)
            })
            .catch((e)=>{
               console.log(e)
            })
      }, 500),

      restyle(layer){
         let toStyle = layer

         if(toStyle === undefined){
            toStyle = this.drawnItems
         }

         toStyle.setStyle((feature)=>{
            let style = BASE_STYLE
            style.color = colorGradient((feature.properties.intensity)/5,COLORS.low,COLORS.high)
            if(feature.properties.selected !== undefined){
               style.opacity = 0.9 
               style.weight = 9
            } else {
               style.weight = 2
            }
            return style
         })

      },

      computeStyle: function(layer){
         let base = {
            color: colorGradient((layer.feature.properties.intensity)/5,COLORS.low,COLORS.high), 
            fillOpacity: 0.4+((layer.feature.properties.confidence / 100)*0.4)
         }
         if(layer.url == this.infocus){
            base.weight = 5
         } else {
            base.weight = 0.1
         }
         return base
      },
   }
}
</script>
