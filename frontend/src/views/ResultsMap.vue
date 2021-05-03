<template>
   <div id="results-map-root">
      <div id="map-element"></div>
      <div id="map-overlay"></div>
   </div>
</template>
<style lang="sass">
#results-map-root
   height: 100vh
   width: 100vw
   position: relative

#map-element
   height: 100vh
#map-overlay
   pointer-events: none
   position: absolute
   top: 0
   left: 0
   height: 100vh
   width: 100vw
   //background: rgba(0,255,0,0.2) 
   z-index: 9999

</style>
<script>
import * as L from "leaflet"
import {TILE_URL,ll_gj_box} from "@/configure_map"
import bbox from "geojson-bbox"

function fetch_country(map,api,gwno){
   api.get.rel(`countries/${gwno}`)
      .then((r)=>{
         new L.TileLayer.BoundaryCanvas(TILE_URL,{
            boundary: r.data.shape,
            id: "countrytiles",
            opacity: 0.9
         }).addTo(map)

         map.fitBounds(ll_gj_box(r.data.shape))
      })
}

function fetch_ged(map,api,gwno,shift){
   let cfg = {
      onEachFeature: (ftr,lyr)=>{
         lyr.bindPopup(JSON.stringify(ftr.properties))
      }
   }
   let ged_points = L.geoJSON(undefined,cfg).addTo(map)
   let ged_buffered = L.geoJSON(undefined,cfg).addTo(map)

   api.get.rel(`eval/ged/points/${gwno}/${shift+1}`)
      .then((r)=>{
         ged_points.addData(r.data)
      })

   api.get.rel(`eval/ged/buffered/${gwno}/${shift+1}`)
      .then((r)=>{
         ged_buffered.addData(r.data)
      })
}

function fetch_predictions(map,api,gwno,shift){
   let predictions = L.geoJSON(undefined,{
      onEachFeature: (ftr,lyr)=>{
         api.get.rel(`eval/preds/${ftr.id}`)
            .then((r)=>{
               console.log(r)
               lyr.bindPopup(JSON.stringify(r.data.properties))
            })
         }
   }).addTo(map)
   api.get.rel(`eval/countries/${gwno}/preds/${shift}`)
      .then((r)=>{
         predictions.addData(r.data)
      })
}

export default {
   data(){
      return {
         map: undefined,
         country: undefined,
         ged_points: undefined,
         ged_buffered: undefined,
      }
   },
   computed: {
      shift(){
         return Number.parseInt(this.$route.params.shift)
      },
   },

   mounted(){
      this.map = L.map("map-element")

      L.tileLayer(TILE_URL,{
         id: "background",
         ext: "png",
         opacity: 0.8
      }).addTo(this.map)

      fetch_country(this.map,this.$api,this.$route.params.gwno)
      fetch_ged(this.map,this.$api,this.$route.params.gwno,this.shift)
      fetch_predictions(this.map,this.$api,this.$route.params.gwno,this.shift)
   }
}
</script>
