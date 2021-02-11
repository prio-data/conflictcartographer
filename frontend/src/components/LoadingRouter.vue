<!--
This component is responsible for conditional routing of the user,
based on their current participation status. The routing follows a
hand-holding strategy designed to maximize participation.
-->
<template>
<Card>
</Card>
</template>
<script>
import Spinner from "@/components/widgets/Spinner"
import Card from "@/components/Card"

export default {
   components: {Card,Spinner},

   data(){
      return {
         status: "Doing some stuff"
      }
   },

   mounted(){
      this.status = "Checking assigned countries"
      if(!this.$cookies.get("informed")){
         this.$router.push("/info")
      } else {
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
                  this.$router.push("/status")
               } else {
               }
            })
      }
   }
}
</script>
