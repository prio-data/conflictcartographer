<template>
   <div 
      v-on:click="$emit('chosen')" 
      class="card">
      <p class="projecttitle">{{ project.name }}</p>
      <span
         v-if="profileInfo">
         <p>You have drawn {{ shapes }} shapes.</p>
         <div
            v-if="hasDrawn"
            class="checkmark">
            &#x2714;
         </div>
         <p>This project ends on {{ ends }}</p>
      </span>
   </div>
</template>

<script charset="utf-8">
   export default {
      name: "ProjectView",

      props: ["project"],

      components: {
      },

      computed: {
         profileInfo(){
            return this.$store.state.profile.projects[this.project.pk.toFixed()]
         },
         shapes(){
            return this.profileInfo.shapes
         },
         hasDrawn(){
            return this.shapes > 0
         },
         last(){
            return this.profileInfo.last
         },
         first(){
            return this.profileInfo.first
         },
         ends(){
            let dt = new Date(this.project.startdate)
            return dt.toDateString()
         }
      },

      methods: {
      }, 
   }
</script>

<style lang="sass" scoped> 
@import "../sass/variables.sass"

p.projecttitle
   font-size: 25px

div.checkmark
   float: right 
   position: relative 
   font-size: 40px
   color: green

div.card
   width: 400px
   height: 100px 

   margin-bottom: $gaps 
   padding: 15px

   background: $ui_gray 
   border-radius: $roundedness

div.card:hover
   background: $ui_highlight

div.card p
   line-height: 0.1
   font-size: 20px
</style>
