<template>
   <div id="app">
      <Navbar 
         v-on:goback="backToMenu"
         v-on:logout="logout"
         v-on:helpme="toggleMenuInfo"
         title="Conflict Cartographer"/> 
      <MapEditor
         v-if="currentProject !== null"
         v-bind:project="currentProject"
         />
      <ProjectMenu 
         :projects="projects"
         v-else/>
      <Monogram/>
      <Modal 
         v-if="showMenuInfo"
         v-on:toggle="toggleMenuInfo">
         <menu_tutorial/>
      </Modal>
   </div>
</template>

<script>

import ProjectMenu from "./components/ProjectMenu.vue"
import MapEditor from "./components/MapEditor.vue"
import Navbar from "./components/Navbar.vue"
import Modal from "./components/Modal.vue"
import Monogram from "./components/Monogram.vue"

import menu_tutorial from "./content/menu_tutorial.vue"

export default {
   name: 'app',
   components: {
      Navbar,
      ProjectMenu,
      MapEditor,
      Modal,
      Monogram,
      menu_tutorial,
   },

   data: function(){
      return {
         showMenuInfo: false,
      }
   },

   computed: {

      currentUser: function(){
         return this.$store.state.sessionInfo.uk;
      },

      currentProject: function(){
         return this.$store.state.currentProject;
      },

      menustatus: function(){
         return this.$store.state.menustatus;
      },

      projects: function(){
         return this.$store.state.projects
      }

   },

   methods: {
      backToMenu: function(){
         this.$store.dispatch("backToMenu")
      },

      logout: function(){
         window.location = window.location + "accounts/logout"
      },

      // Modal info stuff
      toggleMenuInfo:  function(){
         this.showMenuInfo = !this.showMenuInfo
      }
   },

   beforeMount: function(){
      const csrfToken = this.$cookies.get("csrftoken");
      const apiDef = {
         url: "/api",
         header: {credentials: "include",
            headers: {"X-CSRFToken": csrfToken}
         }
      }

      this.$store.commit("initApi",apiDef)

      let sessionInfo = JSON.parse(document.getElementById("sessionInfo").textContent);
      this.$store.commit("setSessionInfo",sessionInfo);
   },

   mounted: function(){
   },
}
</script>

<style lang="sass">
   @import "./sass/variables.sass"

   #toolbar
      margin: $gaps 
</style>
