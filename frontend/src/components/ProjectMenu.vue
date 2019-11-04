<template>
   <div class="menu">
      <ProjectView 
         v-bind:project="project" 
         v-for="project in projects"
         v-on:chosen="chosen(project)">
      </ProjectView>
   </div>
</template>

<script charset="utf-8">
   import ProjectView from "./ProjectView.vue"

   export default {
      name: "ProjectMenu",

      props: ["projects"],

      components: {
         ProjectView,
      },
      
      methods: {
         chosen: function(project){
            this.$store.dispatch("chooseProject",project)
         }
      }
   }
</script>
<style lang="sass" scoped> 
@import "../sass/variables.sass"

div.menu
   overflow-x: scroll 
   overflow-y: hidden 
   white-space: nowrap
   height: $map_height
   width: 100%
</style>
