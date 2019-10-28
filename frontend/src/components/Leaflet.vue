
<template> 
   <l-map ref="map" :zoom="zoom" :center="center" id="map">
      <l-tile-layer :url="url" :attribution="attrib"></l-tile-layer>
      <l-marker :lat-lng="marker" :icon="icon">
      </l-marker>
      <div v-for="layer in layers" v-bind:key="layer.id">
         <l-geo-json
           :geojson="layer.fields.geometry"
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
            marker: L.latLng(60,10),
            center: L.latLng(60,10),
            zoom: 5,
            icon: L.icon({
               iconUrl: "http://icons.iconarchive.com/icons/graphicloads/100-flat/256/home-icon.png",
               iconSize: [32,32],
               iconAnchor: [16,37]
            })
         }
      },

      methods: {
         computeStyle: function(layer){

            let red = 75;
            let green = 25;
            let blue = 25; 

            layer.style.color = this.rgbToHex(red,green,blue);
            return layer.style
         },

         scaleValueToHex: function(x){
            // Turns a number between 0 and 100 into a hex value

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
         }
      },

      mounted: function(){

         this.$nextTick(function(){
            // Add draw control
            const map = this.$refs.map.mapObject;
            const store = this.$store;

            this.map = map 


            this.drawnItems = new L.FeatureGroup();

            this.map.addControl(new L.Control.Draw({
               edit: {
                  featureGroup: this.drawnItems
               }
            }));

            // Add event listener
            map.on(L.Draw.Event.CREATED, function(e){
               let layer = new Layer(
                  e.layer.toGeoJSON(), 0,0
               );
               layer.pk = layer.hash 
               store.commit("pushLayer",layer);
            })
         });
      }
   }
</script>

<style lang="sass" type="text/css" media="screen">
   #map
      height: 90vh 
      width: 100% 
</style>
