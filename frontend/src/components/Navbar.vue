<template>
<div id="navbar">
   <div id = "headline" class = "row">
      <div class="maintitle">
         {{ title }} 
      </div>
      <div class="subtitle">
         {{ projectname }}
      </div>
   </div>
   <div id = "menu" class = "row">
      <button 
         v-on:click="$emit('goback')">Back</button>
      <button id="logout" 
         v-on:click="$emit('logout')">
         Log out
      </button>
   </div>
</div>
</template>

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

         }
      }

   }
</script>

<style scoped lang="sass" type="text/css" media="screen">
@import "../sass/variables.sass"

#navbar
   margin-left: 15px
   height: 100px


#headline
   font-size: 200%
   margin-right: 10px

#headline .maintitle
   float: left

#headline .subtitle
   float: left
   padding-left: 10px
   color: $ui_highlight

#menu button   
   width: auto
   background: $ui_gray 
   margin-right: 5px
   margin-bottom: 5px
   border: none
   font-size: 130%

#menu button:hover
   background: $ui_highlight 
</style>
