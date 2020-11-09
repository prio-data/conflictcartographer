<template>
   <div id="profile-view">
      <div id="profile-centered">
         <div id="profile-image">
            <img :src="img"  alt="">
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
import defaultImage from "@/images/prof.jpg"

export default {
   name: "Profile",
   props: ["profile"],
   data() {
      return {
         img: defaultImage
      }
   },

   computed: {
      name(){
         return this.profile.name
      }
   },
}

</script>
