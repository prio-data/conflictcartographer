<template>
   <table cellspacing=0 cellpadding=0 id="country-status-table">
      <CountryProgressSummary :country="country" v-for="country in countries" :key="country.gwno">
      </CountryProgressSummary>
   </table>
</template>
<style lang="sass">
@import "@/sass/variables"

table
   border-radius: 4px
   border: none
   background: #ddd
   padding-top: 10px
   padding-bottom: 20px

td
   border-bottom: 1px solid #f0f0f0 
   padding: 2px 4px

th
   text-align: left
   padding-left: 5px

</style>
<script>
import CountryProgressSummary from "@/components/CountryProgressSummary"
export default {
   props: ["countries"],
   components: {CountryProgressSummary},
}
</script>
