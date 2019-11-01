<template>
   <div id="app">
      <Navbar 
         v-on:goback="backToMenu"
         v-on:logout="logout"
         title="Conflict Cartographer"/> 
      <ProjectMenu 
         v-if="currentProject === null"         
         v-bind:projects="projects"/>
      <MapEditor
         v-else
         v-bind:user="currentUser"
         v-bind:project="currentProject"
         />
   </div>
</template>

<script>

import ProjectMenu from "./components/ProjectMenu.vue"
import MapEditor from "./components/MapEditor.vue"
import Navbar from "./components/Navbar.vue"

import * as R from "ramda"

export default {
   name: 'app',
   components: {
      Navbar,
      ProjectMenu,
      MapEditor,
   },

   data: function(){
      return {
      }
   },

   computed: {
      projects: function(){
         return this.$store.state.projects;
      },
      currentUser: function(){
         return this.$store.state.sessionInfo.uk;
      },
      currentProject: function(){
         return this.$store.state.currentProject;
      },
   },

   methods: {
      backToMenu: function(){
         this.$store.dispatch("backToMenu")
      },
      logout: function(){
         window.location = window.location + "accounts/logout"
      }
   },

   beforeMount: function(){
      let sessionInfo = JSON.parse(document.getElementById("sessionInfo").textContent);
      this.$store.commit("updateSessionInfo",sessionInfo);

      const csrfToken = this.$cookies.get("csrftoken");
      const apiDef = {
         url: "/api",
         header: {credentials: "include",
            headers: {"X-CSRFToken": csrfToken}
         }
      }
      this.$store.commit("initApi",apiDef)

   },

   mounted: function(){
      this.$store.dispatch("initializeProjects")
   },
}
</script>

<style lang="sass">
   @import "./sass/variables.sass"

   #toolbar
      margin: $gaps 
</style>
