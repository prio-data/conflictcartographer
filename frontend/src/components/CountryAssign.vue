<template>
   <Card>
      <template v-slot:header>
         <h1>COUNTRY ASSIGNMENTS</h1>
      </template>
      <template v-slot:content>
         <div class="assignments-layout">
            <multiselect 
               v-model="value" 
               :options="options" 
               :searchable="true"
               :close-on-select="false"
               :multiple="true"
               :max-height="500"
               @open="removeHelp"
               >
            </multiselect>
         </div>
      </template>
      <template v-slot:footer>
         <div class="footer-container">
            <button class="continue">Proceed</button>
         </div>
      </template>
      <template v-slot:overlay>
         <div id="help-overlay">
            <p>
               {{ helptext }}
            </p>
         </div>
      </template>
   </Card>
</template>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style lang="sass" scoped>

div.assignments-layout
   height: 100%
   margin: 0 10px
   overflow: hidden

div.footer-container
   height: 100%
   width: 100%
   display: grid

button.continue
   margin: 10px

#help-overlay
   display: grid
   width: 100% 
   height: 100% 
   place-items: center
   color: gray
   visibility: hidden 

#help-overlay p
   font-size: 30px
   margin: 20px
   //transform: translate(0,-100px)

@media only screen and (min-height: 600px)
   #help-overlay
      visibility: visible

</style>
<script>
import Card from "@/components/Card"
//import AssignedCountry from "@/components/AssignedCountry"
import Multiselect from "vue-multiselect"
import "@/sass/global.sass"

export default {
   name: "CountryAssign",
   components: {Card,Multiselect},

   data(){
      return {
         countries: [
         ],
         value: "",
         helptext: "Please select the countries that you consider yourself an expert on by clicking the above list.",
      }
   },

   computed:{
      options(){
         return this.countries.map(c=>c.name)
      }
   },
   
   methods: {
      unassignCountry(c){
         // Make an API call
         let unassigned = this.countries.findIndex(ctry=>ctry.gwno == c.gwno)
         if(unassigned > -1){
            this.countries.splice(unassigned,1)
         }
      },
      removeHelp(c){
         this.helptext = "Great! Thanks. Now click the button below to proceed"
      }
   },

   mounted(){
      // Mocking
      let randomName = (length)=>{
         let letters = "abcdefghijklmnopqrstuvwxyz"
         if(length === undefined){
            length = 8
         }
         let current = ""
         for(let i = 0; i < length; i++){
            current = current + letters[Math.abs(Math.round(Math.random()*letters.length)-1)]
         }
         return current
      }

      for(let i = 0; i < 32; i++){
         this.countries.push({
            url: `http://www.foo.bar/${i}`,
            name: randomName(),
            gwno: i
         })
      }
   }
}
</script>
