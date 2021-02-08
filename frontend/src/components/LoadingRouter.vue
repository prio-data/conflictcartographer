<!--
This component is responsible for conditional routing of the user,
based on their current participation status. The routing follows a
hand-holding strategy designed to maximize participation.
-->
<template>
   <div id="root">
      <div class="card">
         <h1>Loading...</h1>
         <p class="status">{{ status }}</p>
      </div>
   </div>
</template>
<style scoped>
div {
   height: 100vh;
   width: 100vw;
   display: grid;
   place-items: center;
}
.card {
   height: 200px;
}
</style>
<script>
import Spinner from "@/components/widgets/Spinner"

export default {
   components: {Spinner},

   data(){
      return {
         status: "Doing some stuff"
      }
   },

   mounted(){
      // Figure out where do go by doing some queries
      // TODO
      // Implement stuff in backend (requests)
      // Add routing (see log statements)

      let SIM_DELAY = ()=>{return 250 + (250*Math.random())}

      this.status = "Checking assigned countries"
      this.$store.state.api.get.rel("profile/assigned")
         .then((assigned_countries)=>{
            if(assigned_countries.data.countries.length == 0){
               this.$router.push("/assign")
               return true
            } else {
               return false
            }})

         .then((done)=>{
            if(!done){
               this.status = "Checking status of assigned"
               return this.$store.state.api.get.rel("profile/unfulfilled")
                  .then((unfulfilled)=>{
                     if(unfulfilled.data.countries.length>0){
                        this.$router.push("/progress")
                        return true
                     } else {
                        return false
                     }
                  })
            } else {
               return done 
            }})
         .then((done)=>{
            if(!done){
               this.status = "Checking profile status"
               return this.$store.state.api.get.rel("profile/exists")
                  .then((profile)=>{
                     let hasmeta = profile.data.profile
                     if(!hasmeta){
                        this.$router.push("/questionaire")
                        return true
                     } else {
                        return false
                     }
                  })
            } else {
               return done
            }})

         .then((done)=>{
            if(!done){
               this.status = "Proceeding to menu"
               this.$router.push("/menu")
            } else {
            }
         })

   }
}
</script>
