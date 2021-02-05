<template>
   <Card>
      <template v-slot:header>
         <h1>PROGRESS</h1>
      </template>

      <template v-slot:content>
         <div class="menu">

            <div class="category nextup">
               <h2>Next up: {{ next.name }}</h2>
               <div class="next panel">
                  <CountryView v-if="next !== undefined" :country="next">
                  </CountryView>
               </div>
               <button class="continue">Add predictions for {{next.name}}</button>
            </div>

            <div class="category pending">
               <h2>Pending: {{ Math.round(((pending.length+1) / all.length)*100,2)}}%</h2>
               <div class="hlist panel">
                  <CountryView v-for="country in pending" :key="country.gwno" :country="country">
                  </CountryView>
               </div>
            </div>

            <div class="category pending">
               <h2>Fulfillled: {{ Math.round((fulfilled.length / all.length)*100,2) }}%</h2>
               <div class="fulfilled hlist panel">
                  <CountryView v-for="country in fulfilled" :key="country.gwno" :country="country">
                  </CountryView>
               </div>
            </div>

         </div>
      </template>

      <template v-slot:footer>
         <div class="controls-holder">
            <button class="alt fill">Change Assigned</button>
         </div>
      </template>

   </Card>
</template>
<style lang="sass" scoped>

@import "@/sass/variables"

div
   grid-gap: $menu-gaps

.controls-holder
   padding: $menu-gaps
   height: 100%
   width: 100%

.menu
   display: grid
   grid-template-rows: 2fr 1fr 1fr
   grid-template-columns: 100% 
   width: 100% 
   height: 100%
   padding: 0 $menu-gaps

.nextup
   display: grid
   grid-template-rows: auto 2fr 1fr

.mock-ctry
   display: inline-block
   height: 100% 
   width: 100px
   background: red

.category h2
   line-height: 10px

.next div
   width: 200px

.hlist div
   margin: 0 $menu-gaps/2
   width: 100px
   display: inline-block

.hlist
   overflow: auto
   white-space: nowrap

.next
   display: grid
   height: 100%
   place-items: center

.panel
   padding: 10px
   background: #aaa
   border-radius: 10px

</style>
<script>
import Card from "@/components/Card"
import CountryView from "@/components/CountryView"
import {mock_countries} from "@/mocking"
export default {
   components: {Card,CountryView},
   data(){
      return {
         next: undefined,
         pending: [],
         fulfilled: [],
      }
   },

   computed:{
      all(){
         return [this.next].concat(this.pending).concat(this.fulfilled)
      }
   },

   mounted(){
      // ask for next
      this.next = mock_countries()

      // ask for pending
      this.pending = mock_countries(5)

      // ask for fulfilled
      this.fulfilled = mock_countries(8)
   }
}
</script>
