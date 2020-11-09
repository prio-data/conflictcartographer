<template>
<div id="navbar">
   <div id="title">
      <span>{{ title }} / </span>
      <span class="sub">{{ projectname }}</span>
   </div>
   <div></div>
   <div id="navbar-buttons">
      <button v-on:click="$emit('goback')">Back</button>
      <button v-on:click="$emit('logout')">Log out</button>
      <button v-on:click="$emit('helpme')">?</button>
   </div>
   <div></div>
</div>
</template>

<style scoped lang="sass" type="text/css" media="screen">
@import "../sass/variables.sass"

#navbar
   display: grid
   grid-template-areas: "one one" "two three"
   grid-template-columns: $menu-proportions
   margin-left: $menu-gaps 

#navbar > #title
   font-size: 25px 
   grid-area: one

#navbar > #title > span.sub
   color: $ui_highlight

#navbar-buttons
   display: grid
   grid-template-columns: 2fr 2fr 1fr
   column-gap: 10px
   grid-area: two 

#navbar-buttons > button
   background: $ui_gray
   border: none
   height: 40px 
   padding: 0

#navbar-buttons > button:hover
   background: $ui_highlight

</style>

<script charset="utf-8">
   export default {

      name: "Toolbar",
      props: ["title"],

      computed: {
         username: function(){
            return this.$store.state.sessionInfo.username
         },
         projectname: function(){
            let project = this.$store.state.currentProject
            return project ? project.name : "Menu"

         },

         anyLoading: function(){
            return this.$store.state.menustatus != 0
         }
      }

   }
</script>

