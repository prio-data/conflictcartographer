<template>
   <Card :loaded="loaded">
      <template v-slot:header>
         <h1>NEXT UP</h1>
      </template>

      <template v-slot:content>
         <div id="status-menu">
            <div id="status-nextup">
               <div v-if="next !== undefined" id="status-nextup-overlay">
                  <h1>
                     {{ next.name }}
                  </h1>
               </div>
               <div id="plot">
               </div>
            </div>
            <div id="status-other">
               <div class="list-category">
                  <p>Pending</p>
                  <div v-if="pending.length>0" class="hlist pending">
                     <div v-for="country in pending " :key="country.gwno">{{country.iso2c}}</div>
                  </div>
               </div>
               <div class="list-category">
                  <p>Fulfilled</p>
                  <div v-if="fulfilled.length>0" class="hlist fulfilled">
                     <div v-for="country in fulfilled" :key="country.gwno">{{country.iso2c}}</div>
                  </div>
               </div>
            </div>
         </div>
      </template>

      <template v-slot:footer>
         <div class="footer-buttons">
            <button v-on:click="go_to_next" class="continue">Add predictions for {{ next? next.name : ""}}</button>
            <button v-on:click="go_to_assign" class="alt">Change Assigned</button>
         </div>
      </template>

   </Card>
</template>

<style lang="sass" scoped>

@import "@/sass/variables"

#status-menu
   display: grid
   grid-template-rows: auto 1fr 
   justify-items: center
   width: 100%
   height: 90%

#status-menu>div
   width: 100%

#status-nextup
   display: grid
   place-items: center
   background: $ui-highlight 
   padding: 10px 0 
   position: relative

#status-nextup-overlay
   position: absolute
   top: 0
   left: 0
   width: 100%
   height: 100%
   display: grid
   place-items: center
   color: black

#plot
   height: 420px
   width: 420px 
   cursor: default

#status-other
   display: grid
   grid-template-rows: 1fr 1fr
   padding: 0 20px

.list-category
   display: grid
   grid-template-rows: 1fr 1fr

.hlist>div
   margin: 0 $menu-gaps/2
   width: 40px
   display: inline-block
   background: $ui-highlight 
   padding: 4px
   font-weight: bold

.hlist
   overflow-x: auto
   overflow-y: hidden
   white-space: nowrap
   //background: #ddd
   border-radius: 2px
   padding: 10px 10px

</style>

<style>
.leaflet-container {
    background: none;
    outline: 0;
}
</style>

<script>
import Card from "@/components/Card"
import CountryView from "@/components/CountryView"
import {mock_countries} from "@/mocking"
//import * as d3 from "d3"
import L from "leaflet"
import "leaflet/dist/leaflet.css"
import {fit_to_geojson,TILE_URL} from "@/configure_map"


export default {
   components: {Card,CountryView},
   data(){
      return {
         next: undefined,
         pending: [],
         fulfilled: [],
         loaded: false 
      }
   },

   computed:{
      all(){
         let all = this.pending.concat(this.fulfilled)
         if(this.next !== undefined){
            all = all.concat([this.next])
         }
         return all
      }
   },

   methods:{
      go_to_next(){
         this.$router.push(`/ctry/${this.next.gwno}`)
      },
      go_to_assign(){
         this.$router.push("/assign")
      }
   },

   mounted(){
      let map = new L.Map("plot")
      map.zoomControl.remove()
      map.attributionControl.remove()
      map.dragging.disable();
      map.touchZoom.disable();
      map.doubleClickZoom.disable();
      map.scrollWheelZoom.disable();
      map.boxZoom.disable();
      map.keyboard.disable();

      this.$store.state.api.get.rel("profile/next")
         .then((rsp)=>{
            if(rsp.data.status != "active"){
               this.$router.push("/")
            } else {
               this.next = rsp.data.next
               fit_to_geojson(map,this.next.shape)
               let layer = L.geoJson(this.next.shape,{
                  style:{
                     color: "black"

                  }
               })
               layer.addTo(map)
               this.loaded = true

               this.$store.state.api.get.rel("profile/pending")
                  .then((r)=>{
                     let not_next = r.data.countries.filter((ctry)=>ctry.gwno != this.next.gwno)
                     this.pending = not_next 
                  })
               this.$store.state.api.get.rel("profile/fulfilled")
                  .then((r)=>{
                     this.fulfilled = r.data.countries
                  })
            }
         })
   }
}
</script>
