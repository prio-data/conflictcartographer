
<template> 
   <l-map ref="map" 
      :zoom="mapZoom" 
      :center="mapCenter" 
      id="map"
      zoomControl="false">
      <l-tile-layer :url="url" :attribution="attrib"></l-tile-layer>
      <div v-for="layer in layers" v-bind:key="layer.pk">
         <l-geo-json
           :geojson="layer.geometry"
           :optionsStyle="computeStyle(layer)">
         </l-geo-json>
      </div>
   </l-map>
</template>

<script charset="utf-8">

   import {LMap, LTileLayer, LMarker, LGeoJson} from "vue2-leaflet"
   import L from "leaflet"
   import "leaflet-draw" 
   import Layer from "@/models/layer.js"

   import * as R from "ramda"


   export default {
      name: "Leaflet",
      components: {LMap,LTileLayer,LMarker, LGeoJson},

      data: function(){
         return{
            url: "http://{s}.tile.osm.org/{z}/{x}/{y}.png",
            attrib: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
            id: "mapbox.streets",
         }
      },

      methods: {
         computeStyle: function(layer){
            let base = {
               color: this.rgbToHex(layer.intensity,
                                    -4,-4),

               fillOpacity: ((layer.confidence + 5)/10)
            }
            if(layer.vizId == this.focused){
               base.weight = 2 
               base.fillOpacity = base.fillOpacity + 0.2
            } else {
               base.weight = 0.1 
            }
            return base
         },

         scaleValueToHex: function(x){
            // Turns a number between 0 and 100 into a hex value
            x = ((x+5)/10) * 100

            const ceil = (x,y) => x > y ? y : x;

            const toHex = (x) => Number(x).toString(16)

            const normalize = R.pipe((x) => x*2.55, 
                                     R.curry(ceil)(R.__,255),
                                     Math.round)

            return toHex(normalize(x))

         }, 

         rgbToHex: function(r,g,b){
            let hexValues = R.map(this.scaleValueToHex,[r,g,b])
            return "#" + hexValues.join("")
         },


      },

      computed: {
         layers: function(){
            return this.$store.state.layers;
         },
         focused: function(){
            return this.$store.state.infocus;
         },
         mapZoom: function(){
            return this.$store.state.zoomlvl;
         },
         mapx: function(){
            return this.$store.state.mapx;
         },
         mapy: function(){
            return this.$store.state.mapy;
         },
         mapCenter: function(){
            return L.latLng(this.mapx,this.mapy)
         },
      },

      mounted: function(){

         this.$nextTick(function(){

            const map = this.$refs.map.mapObject;
            const store = this.$store;
            this.map = map;

            // Disable all movement 
            this.map.touchZoom.disable();
            this.map.doubleClickZoom.disable();
            this.map.scrollWheelZoom.disable();
            this.map.dragging.disable();

            // Remove zoom control

            this.map.zoomControl.remove();


            // Add draw control
            this.drawnItems = new L.FeatureGroup();
            this.map.addControl(new L.Control.Draw({
               draw: {
                  rectangle: false,
                  circle: false,
                  circlemarker: false,
                  polyline: false,
               },
               edit: {
                  featureGroup: this.drawnItems,
                  edit: false,
                  remove: false
               }
            }));

            // Add event listener
            map.on(L.Draw.Event.CREATED, function(e){
               let layer = e.layer.toGeoJSON()
               layer.intensity = 0
               layer.confidence = 0
               layer.author = "http://localhost:8000/api/users/1/"
               store.dispatch("createLayer",layer);
            })
         });
      }
   }
</script>

<style lang="sass" type="text/css" media="screen">
   @import "../sass/variables.sass"
   #map
      height: $map_height 
      width: 100% 
</style>
