
<template> 
   <l-map ref="map" 
      :options="mapOpts"
      id="map"
      :zoomAnimation="false">
      <div 
         v-bind:key="layer.url"
         v-for="layer in layers">
         <l-geo-json
           :geojson="layer.shape.geometry"
           :optionsStyle="computeStyle(layer)">
         </l-geo-json>
      </div>
   </l-map>
</template>

<script charset="utf-8">

   import {LMap, LGeoJson} from "vue2-leaflet"
   import L from "leaflet"
   import "leaflet-draw" 
   import "leaflet-boundary-canvas"
   import bbox from "geojson-bbox"
   import colorGradient from "../util/colorGradient.js"

   export default {
      name: "Leaflet",
      components: {
         LMap,
         LGeoJson
      },

      data: function(){
         return{
            url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
            attrib: "Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community",
            id: "mapbox.streets",
            mapOpts: {
               zoomSnap: 1
            },
         }
      },

      methods: {
         computeStyle: function(layer){
            /*
            let base = {
               color: colorGradient(((layer.intensity + 5)/10), this.color1, this.color2),
               fillOpacity: (((layer.confidence + 5)/10)* 0.5 ) + 0.2
            }
            if(layer.vizId == this.focused){
               base.weight = 5 
               base.fillOpacity = base.fillOpacity + 0.1
            } else {
               base.weight = 0.1 
            }
            */
            let base = {
               color: "red",
               fillOpacity: 0.5
            }
            if(layer.vizId == this.focused){
               base.weight = 5
            } else {
               base.weight = 0.1
            }
            return base
         },
      },

      computed: {
         layers: function(){
            return this.$store.state.layers;
         },
         focused: function(){
            return this.$store.state.infocus;
         },
         color1: function(){
            return this.$store.state.color_low
         },
         color2: function(){
            return this.$store.state.color_high
         },
      },

      mounted: function(){
         const map = this.$refs.map.mapObject;
         map.zoomSnap = 0.1

         const mask = this.$store.getters.projectShape

         this.$nextTick(function(){

            const store = this.$store;
            this.map = map;


            // Disable all movement 
            //this.map.touchZoom.disable();
            //this.map.doubleClickZoom.disable();
            //this.map.scrollWheelZoom.disable();
            //this.map.dragging.disable();

            // Remove zoom control

            //this.map.zoomControl.remove();

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

            // =======================================
            // Disable dragging while drawing 
            map.on(L.Draw.Event.DRAWSTART, function(){
               map.dragging.disable();
            })

            map.on(L.Draw.Event.DRAWSTOP, function(){
               map.dragging.enable();
            })

            // Add event listener
            map.on(L.Draw.Event.CREATED, function(e){
               let layer = e.layer.toGeoJSON()
               store.dispatch("createLayer",layer);
            })
         });

         const osm = new L.TileLayer(this.url, {
            id: "background",
            attribution: this.attrib,
         })

         map.addLayer(osm);

         const masked = new L.TileLayer.BoundaryCanvas(this.url,{
            boundary: mask,
            id: "countrytiles"
         })
         map.addLayer(masked);
         const box = bbox(mask)
         const getbox = (box) => [[box[3],box[0]],[box[1],box[2]]]
         const latlng = L.latLngBounds(getbox(box))

         map.attributionControl.setPosition("bottomleft")

         map.fitBounds(latlng)
         map.setMaxZoom(9)
         map.setMinZoom(6)
         map.setMaxBounds(latlng.pad(2))
         map.setZoom(7)
      }
   }
</script>

<style lang="sass" type="text/css" media="screen">

   @import "../sass/variables.sass"

   #map
      height: $map_height 
      width: $map_width 

   // Tile stuff
   .leaflet-tile-container img
       filter: brightness(0.8)

   .leaflet-tile-container canvas 
       filter: brightness(0.9) contrast(1.1) //saturate(5.5) 

   // Editing dots
   .leaflet-editing-icon
      //width: 5px !important
      //height: 5px !important
      //top: 5px !important 
      //left: 5px !important
      border-radius: 10px
      border: none
      background: $drawcolor

   .leaflet-marker-pane div:nth-child(2)
      background: $ui_highlight

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
