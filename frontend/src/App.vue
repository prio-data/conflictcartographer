<template>
   <div id="app">
      <div id="main" v-if="state=='loaded'">
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
            v-on:projectSelected="projectSelected"
            v-else/>
         <Monogram/>
         <Modal 
            v-if="showMenuInfo"
            v-on:toggle="toggleMenuInfo">
            <menu_tutorial/>
         </Modal>
      </div>
      <div v-else-if="state=='error'">
         {{ error }}
      </div>
      <div v-else>
         <Spinner/>
      </div>
   </div>
</template>

<style lang="sass">
   @import "./sass/variables.sass"

   div#main
      background: $ui-background 
      display: grid

      grid-template-rows: $menu-row-proportions 
      height: 100vh 

</style>

<script>

import ProjectMenu from "./components/ProjectMenu.vue"
import MapEditor from "./components/MapEditor.vue"
import Navbar from "./components/Navbar.vue"
import Modal from "./components/Modal.vue"
import Monogram from "./components/Monogram.vue"
import Spinner from "./components/Spinner"

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
      Spinner
   },

   data: function(){
      return {
         showMenuInfo: false,
         state: "loading",
         error: "",
         currentProject: null
      }
   },

   methods: {
      backToMenu: function(){
         this.currentProject = null
      },

      projectSelected(p){
         this.currentProject = p
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
      this.$store.commit("initApi",this.$cookies.get("csrftoken"))
      this.$store.state.api.get.rel("currentproject",{params:{verbose:false}})
         .then((r)=>{
            this.state = "loaded"
         })
         .catch((e)=>{
            this.state = "error"
            this.error = e
         })


      let sessionInfo = JSON.parse(document.getElementById("sessionInfo").textContent);
   },

   mounted: function(){
   },
}
</script>
