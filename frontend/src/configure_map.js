
import L from "leaflet"

const TILE_URL = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}"

export function shape_to_latlng_box(shape){
   const box = bbox(shape)
   return L.latLngBounds([[box[3],box[0]],[box[1],box[2]]])
}

export function configure_map(map,mask){
   // =======================================
   // Disable dragging while drawing 
   map.on(L.Draw.Event.DRAWSTART, function(){
      map.dragging.disable();
   })

   map.on(L.Draw.Event.DRAWSTOP, function(){
      map.dragging.enable();
   })

   new L.TileLayer(TILE_URL, {
      id: "background",
      ext: "png",
      opacity: 0.3
   }).addTo(map)

   new L.TileLayer.BoundaryCanvas(TILE_URL,{
      boundary: mask, 
      id: "countrytiles"
   }).addTo(map)


   map.zoomSnap = 0.1
   map.setMaxZoom(9)
   map.setMinZoom(6)
   map.attributionControl.remove()
}
