
<template>
   <Card :loaded="loaded">
      <template v-slot:header><h2>Great job!</h2></template>
      <template v-slot:content>
         <div id="thanks-text">
            <h1>
            Thank you for submitting predictions! 
            </h1>
            <p>
               If you don't want to revise your predictions, you can now close the
               browser window.
            </p>

            <p>You have submitted predictions for the period {{start_pred}}-{{end_pred}} for:</p>
            <CountryStatusTable :countries="submitted">
            </CountryStatusTable>
         </div>
      </template>
      <template v-slot:footer>
         <div class="footer-buttons">
            <button v-on:click="to_change_assigned" class="alt">Change assigned</button>
         </div>
      </template>
   </Card>
</template>
<style lang="sass" scoped>
#thanks-text
   padding: 20px

#country-status-table
   width: 100%
</style>
<script>
import Card from "@/components/Card"
import CountryStatusTable from "@/components/CountryStatusTable"
import {format_date} from "@/date_formatting"
export default {
   components: {Card,CountryStatusTable},

   data(){
      return {
         start_pred: "",
         end_pred: "",
         submitted: null,
      }
   },
      
   computed:{
      loaded(){
         return this.start_pred!=="" && this.end_pred!=="" && this.submitted!==null 
      },
   },

   mounted(){
      this.$api.get.rel("period/next")
         .then((r)=>{
            this.start_pred = format_date(r.data.start)
            this.end_pred = format_date(r.data.end)
         })
         .catch((e)=>{
            console.error(e)
         })
      this.$api.get.rel("profile/assigned")
         .then((r)=>{
            this.submitted = r.data.countries
         })
         .catch((e)=>{
            console.error(e)
         })
   },
   methods: {
      to_change_assigned(){
         this.$router.push("/assign")
      }
   }
}
</script>
