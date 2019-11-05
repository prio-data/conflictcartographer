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
      <button id="logout" 
         v-on:click="$emit('helpme')">
         ? 
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

.imgwrapper
   display: inline-block

.imgcontainer
   vertical-align: middle

img
   padding: 10px 20px
   margin-left: auto
   margin-right: 0
   max-width: 100% 
   height: auto

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
