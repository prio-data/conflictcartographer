<template>
   <Card>
      <template v-slot:header>
         <h1>PROGRESS</h1>
      </template>

      <template v-slot:content>
         <div class="menu">
            <div class="nextup">
               <h2>Next up: {{ next? next.name : ""}}</h2>
               <div class="next panel">
                  <CountryView v-if="next !== undefined" :country="next">
                  </CountryView>
               </div>
               <button v-on:click="go_to_next" class="continue">Add predictions for {{ next? next.name : ""}}</button>
            </div>

            <div class="category pending">
               <h2>Pending: {{ Math.round(((pending.length) / all.length)*100,2)}}%</h2>
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
   grid-template-rows: 30px 2fr 1fr

.mock-ctry
   display: inline-block
   height: 100% 
   width: 100px
   background: red

.category
   display: grid
   grid-template-rows: 30px 1fr

h2
   line-height: 10px

.next div
   width: 200px

.hlist div
   margin: 0 $menu-gaps/2
   width: 100px
   display: inline-block

.hlist
   overflow-x: auto
   overflow-y: hidden
   white-space: nowrap
   height: 100px 

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
      }
   },

   mounted(){
      this.$store.state.api.get.rel("profile/assigned")
         .then((all)=>{
            return this.$store.state.api.get.rel("profile/unfulfilled")
               .then((unfulfilled)=>{
                  console.log(unfulfilled)
                  this.pending = unfulfilled.data.countries
                  let pending_names = this.pending.map((ctry)=>ctry.name)
                  this.fulfilled = all.data.countries.filter((ctry)=>{
                     return !pending_names.includes(ctry.name) 
                  })
                  this.next = this.pending.pop()
                  if(this.next === undefined){
                     this.$router.push("/")
                  }

               })
         })
   }
}
</script>
