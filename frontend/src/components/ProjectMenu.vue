<template>
   <div id="pm-wrapper"> 
      <div id="pm" v-if="loaded">
         <div class="pane infobar">
            <Profile/>
            <MainDescription/>
         </div>
         <div class="pane projects">
            <div class="projectlist">
               <ProjectView class="card"
                  v-for="project in projects"
                  :key="project.url"
                  :project="project"
                  v-on:chosen="chosen(project)">
               </ProjectView>
            </div>
         </div>
      </div>
      <Spinner v-else/>
   </div>
</template>

<style lang="sass" scoped>
@import "@/sass/variables.sass"

div#pm-wrapper
   display: grid
   background: $ui_gray 

div#pm
   display: grid
   grid-template-columns: $menu-col-proportions 
   min-height: 0

div.pane
   margin: $menu-gaps 
   max-height: 100%
   min-height: 0px

div.infobar 
   min-height: 0
   max-height: 100%
   margin-top: $menu-gaps*6

div.projects > div.projectlist 
   background: $ui-background 
   border-radius: $roundedness
   overflow-y: scroll 
   max-height: 100% 
   height: 100%

div.projectlist > .card
   margin: $menu-gaps

</style>

<script charset="utf-8">
   import ProjectView from "./ProjectView.vue"
   import Spinner from "../components/Spinner"
   import Profile from "@/components/Profile"
   import MainDescription from "@/components/MainDescription"

   export default {
      name: "ProjectMenu",

      data(){
         return {
            projects: [],
            loaded: false,
         }
      },

      components: {
         ProjectView,
         Spinner,
         Profile,
         MainDescription
      },

      computed: {
         user(){
            this.$store.state.sessionInfo.uk
         },
      },

      methods: {
         chosen: function(project){
            this.$store.dispatch("chooseProject",project)
         }
      },

      mounted(){
         let api = this.$store.state.api
         api.get("assigned",(r)=>{
            this.projects = r
            this.loaded = true
         })
      }
   }
</script>
