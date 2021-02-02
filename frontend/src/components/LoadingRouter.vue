<!--
This component is responsible for conditional routing of the user,
based on their current participation status. The routing follows a
hand-holding strategy designed to maximize participation.
-->
<template>
   <div>
   LOADING
   </div>
</template>
<style scoped>
div {
   height: 100vh;
   width: 100vw;
   display: grid;
   place-items: center;
}
</style>
<script>

export default {
   mounted(){
      // Figure out where do go by doing some queries
      // TODO
      // Implement stuff in backend (requests)
      // Add routing (see log statements)

      this.$store.state.api.get.rel("assigned")
      Promise.resolve({data:[1,2,3]})
         .then((assigned_countries)=>{
            if(assigned_countries.data.length == 0){
               console.log("Routing to cselect")
               return true
            } else {
               return false
            }})
         .then((done)=>{
            if(!done){
               return Promise.resolve({data:{status:"finished"}})//this.$store.state.api.get.rel("next")
                  .then((next)=>{
                     if(next.data.status == "active"){
                        console.log("Routing to next project")
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
               return Promise.resolve({data:{meta:{foo:"bar"},prompted:true}})//this.$store.state.api.get.rel("profile")
                  .then((profile)=>{

                     let hasmeta = Object.keys(profile.data.meta).length > 0
                     let prompted = profile.data.prompted

                     if(!(hasmeta | prompted)){
                        console.log("Routing to metadata select")
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
               console.log("Routing to menu")
            } else {
            }
         })
   }
}
</script>
