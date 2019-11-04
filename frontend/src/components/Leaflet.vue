
<template> 
   <l-map ref="map" 
      :options="mapOpts"
      id="map"
      zoomControl="false">
      <div v-for="layer in layers" v-bind:key="layer.pk">
         <l-geo-json
           :geojson="layer.geometry"
           :optionsStyle="computeStyle(layer)">
         </l-geo-json>
      </div>
   </l-map>
</template>

<script charset="utf-8">

   import {LMap, LTileLayer, LGeoJson} from "vue2-leaflet"
   import L from "leaflet"
   import "leaflet-draw" 
   import "leaflet-boundary-canvas"
   import Layer from "@/models/layer.js"
   import bbox from "geojson-bbox"

   import * as R from "ramda"


   export default {
      name: "Leaflet",
      components: {LMap,LTileLayer,LGeoJson},

      data: function(){
         return{
            //url: "http://{s}.tile.osm.org/{z}/{x}/{y}.png",
            //url: "https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}{r}.png",
            url: "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
            //url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
            attrib: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
            id: "mapbox.streets",
            mapOpts: {
               zoomSnap: 1
            }
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
         const map = this.$refs.map.mapObject;
         map.zoomSnap = 0.1
         const mask = this.$store.state.projectDetails.shape
         this.$nextTick(function(){

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
                  marker: false,
                  polygon: {
                     shapeOptions: {
                        color: "grey"
                     }
                  }
               },
               edit: {
                  featureGroup: this.drawnItems,
                  edit: false,
                  remove: false
               }
            }));

            // Add tiles

            // Add event listener
            map.on(L.Draw.Event.CREATED, function(e){
               let layer = e.layer.toGeoJSON()
               layer.intensity = 0
               layer.confidence = 0
               store.dispatch("createLayer",layer);
            })
         });

         const osm = new L.TileLayer(this.url,{
            id: "background"
         })
         map.addLayer(osm);

         console.log(mask)
         const masked = new L.TileLayer.BoundaryCanvas(this.url,{
            boundary: mask,
            id: "countrytiles"
         })
         map.addLayer(masked);
         const box = bbox(mask)
         console.log(box)
         const padding = 10 
         map.fitBounds([[box[3],box[0]],[box[1],box[2]]],{
            paddingTopLeft: [padding,padding],
            paddingBottomRight: [padding,padding]
         })
      }
   }
</script>

<style lang="sass" type="text/css" media="screen">

   @import "../sass/variables.sass"

   #map
      height: $map_height 
      width: $map_width 

   .leaflet-tile-container img
       //box-shadow: 0 0 10px rgba(0, 0, 0, 0.05)
       filter: brightness(0.8)

   .leaflet-tile-container canvas 
       filter: saturate(5.5) brightness(0.9) contrast(1.1)

   .leaflet-editing-icon
      //width: 5px !important
      //height: 5px !important
      //top: 5px !important 
      //left: 5px !important
      border-radius: 10px
      border: none
      background: $drawcolor

   .leaflet-touch .leaflet-control-zoom-display 
     width: $tbsize + 8px
     height: $tbsize + 8px
     font-size: 18px
     line-height: $tbsize - ($tbsize / 4) 

   .leaflet-touch .leaflet-bar a, .leaflet-touch .leaflet-toolbar-0 > li > a 
     width: $tbsize + 4px
     height: $tbsize + 4px
     font-size: $tbsize / 2 
     line-height: $tbsize + 5px
     background-size: 314px 30px

   .leaflet-touch .leaflet-draw-toolbar.leaflet-bar a 
     background-position-y: 6px

   .leaflet-touch .leaflet-draw-actions a, .leaflet-touch .leaflet-control-toolbar .leaflet-toolbar-1 > li > .leaflet-toolbar-icon 
     font-size: $tbsize / 2 
     line-height: $tbsize + 4px
     height: $tbsize + 4px

   .leaflet-touch .leaflet-draw-actions, .leaflet-touch .leaflet-toolbar-1 
     left: $tbsize + 5px

   .leaflet-touch .leaflet-control-layers, .leaflet-touch .leaflet-bar
      border: none

</style>
