<template>
   <div id="profile-view">
      <div id="profile-centered">
         <div id="profile-image">
            <img :src="profile"  alt="">
         </div>
         <p id="profile-name">{{this.name}}</p>
      </div>
   </div>
</template>

<style lang="sass" scoped>
#profile-view
   max-height: 300px

#profile-centered
   display: grid
   place-items: center

#profile-image > img
   max-height: 100px
   clip-path: circle(50px at center)

</style>

<script>
import profile from "@/images/prof.jpg"

export default {
   name: "Profile",

   data() {
      return {
         name: "",
         profile: profile
      }
   },

   mounted(){
      let api = this.$store.state.api
      api.gget("whoami")
         .then((r)=>{
            this.name = r.data.name
         })
         .catch((e)=>{
            console.log(e)
            this.name = "error"
         })
   }
}

</script>
