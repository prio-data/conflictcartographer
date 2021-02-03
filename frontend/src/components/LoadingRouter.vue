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
      this.$store.state.api.get.rel("assigned")
      new Promise(r=>setTimeout(r,SIM_DELAY(),{data:[1,2,3]}))

         .then((assigned_countries)=>{
            if(assigned_countries.data.length == 0){
               this.$router.push("/assign")
               return true
            } else {
               return false
            }})

         .then((done)=>{
            if(!done){
               this.status = "Checking status of assigned"
               return new Promise(r=>setTimeout(r,SIM_DELAY(),{data:{status:"finished"}}))//this.$store.state.api.get.rel("next")
                  .then((next)=>{
                     if(next.data.status == "active"){
                        // this.$router.push(`/ctry/${next.gwno}`)
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
               return new Promise(r=>setTimeout(r,SIM_DELAY(),{data:{meta:{foo:"bar"},prompted:true}}))//this.$store.state.api.get.rel("profile")
                  .then((profile)=>{

                     let hasmeta = Object.keys(profile.data.meta).length > 0
                     let prompted = profile.data.prompted

                     if(!(hasmeta | prompted)){
                        this.$router.push("/profile")
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
