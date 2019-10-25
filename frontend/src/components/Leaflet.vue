
<template> 
   <div id="container">
      <l-map ref="map" :zoom="zoom" :center="center" id="map">
         <l-tile-layer :url="url" :attribution="attrib"></l-tile-layer>
         <l-marker :lat-lng="marker" :icon="icon">
         </l-marker>
         <div v-for="layer in layers" v-bind:key="layer.id">
            <l-geo-json
              :geojson="layer.json"
              :optionsStyle="layer.style">
            </l-geo-json>
         </div>
      </l-map>
   </div>
</template>

<script charset="utf-8">
   import {LMap, LTileLayer, LMarker, LGeoJson} from "vue2-leaflet"
   import L from "leaflet"
   import "leaflet-draw" 

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
            let ndrawn = 0;
            this.map = map 


            this.drawnItems = new L.FeatureGroup();

            this.map.addControl(new L.Control.Draw({
               edit: {
                  featureGroup: this.drawnItems
               }
            }));

            // Add event listener
            map.on(L.Draw.Event.CREATED, function(e){
               let json = e.layer.toGeoJSON();
               let style = {color: "red"}
               //if(e.layerType === "polygon"){
               store.commit("pushLayer",{
                  style: style,
                  type: e.layerType,
                  json: json,
                  id: ndrawn});
               ndrawn ++;
               //}
            })

         });
      }
   }
</script>

<style lang="sass" type="text/css" media="screen">
   #map
      height: 500px
      width: 100vg 
</style>
