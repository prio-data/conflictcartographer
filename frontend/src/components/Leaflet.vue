
<template> 
   <div id="container">
      <div id="map">
      </div>
   </div>
</template>

<script charset="utf-8">
   import * as L from "leaflet";
   import "leaflet-draw" 

   let mapbox = {
   API: "https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}",
   attrib: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
   id: "mapbox.streets",
   token: "pk.eyJ1IjoicGVkZXIyOTExIiwiYSI6ImNrMjFrdmo1bDAxazMzYm1yMHdyMjl0ZzcifQ.ECjId0WT7V9njkA8OLe2Lg"
   }
   let init = function(){
      // Map setup
      // Namespacing stuff...
      let layers = [];
      let map = L.map("map").setView([60, 10],7);

      L.tileLayer(mapbox.API, {
            attribution: mapbox.attrib,
            maxZoom : 18,
            id: mapbox.id,
            accessToken: mapbox.token}).addTo(map)

      const drawnItems = L.featureGroup().addTo(map)

      map.addControl(new L.Control.Draw({
         edit: {
            featureGroup: drawnItems,
            poly: {
               allowIntersection: false
            }
         },
         draw: {
            polygon: {
               allowIntersection: false,
               showArea: true
            }
         }
      }));

      map.on(L.Draw.Event.CREATED, function(e){
         //let type = e.layerType;
         let layer = e.layer;

         layers.push(layer);

         map.addLayer(layer);
      })
   }

   export default {
      name: "Leaflet",
      methods: {
         initMap: init
      }
   }
</script>

<style lang="sass" type="text/css" media="screen">
   #map
      :height 500px
      :width 100vg 
</style>
