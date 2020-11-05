<template>
   <div v-on:click="$emit('chosen')" id="project-card">
      <p class="projecttitle">{{ project.name }}</p>
   </div>
</template>

<script charset="utf-8">
   export default {
      name: "ProjectView",
      props: ["project"]
   }
</script>

<style lang="sass" scoped> 
@import "../sass/variables.sass"
div#project-card
   padding: $menu-gaps
   height: 80px 
   background: $ui_darkgray
   border-radius: $roundedness
   color: $ui_lightgray
   font-size: 30px

div#project-card:hover
   background: $ui_highlight
</style>
