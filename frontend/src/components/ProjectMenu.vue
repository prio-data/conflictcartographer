<template>
   <div id="pm-wrapper" v-if="loaded"> 
      <div id="pm" v-if="profile.waiver">
         <div class="pane infobar">
            <Profile :profile="profile"/>
            <MainDescription/>
         </div>
         <div class="pane projects">
            <h1 id="menuheader">Countries</h1>
            <div class="projectlist">
               <ProjectView class="card"
                  v-for="project in projects"
                  :key="project.url"
                  :project="project"
                  v-on:chosen="chosen(project)">
               </ProjectView>
               <button id="addProjects">+</button>
            </div>
         </div>
      </div>
      <Waiver v-else/>
   </div>
   <Spinner v-else/>
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

button#addProjects
   width: 100%
   border: none
   height: 70px 
   display: grid
   place-items: center
   //background: #f0f0f0
   font-size: 80px
   line-height: 0
   color: $ui-darkgray

button#addProjects:hover
   color: $ui-highlight

h1#menuheader
   line-height: 20px 

</style>

<script charset="utf-8">
   import ProjectView from "./ProjectView.vue"
   import Spinner from "../components/Spinner"
   import Profile from "@/components/Profile"
   import Waiver from "@/components/Waiver"
   import MainDescription from "@/components/MainDescription"

   export default {
      name: "ProjectMenu",

      data(){
         return {
            projects: [],
            projectsLoaded: false,
            profileLoaded: false,
            profile: {}
         }
      },

      components: {
         ProjectView,
         Spinner,
         Profile,
         MainDescription,
         Waiver
      },

      computed: {
         user(){
            return this.$store.state.sessionInfo.uk
         },
         loaded(){
            return this.projectsLoaded && this.profileLoaded
         }
      },

      methods: {
         chosen: function(project){
            this.$store.dispatch("chooseProject",project)
         },
      },

      mounted(){
         let api = this.$store.state.api

         api.get("assigned",(r)=>{
            this.projects = r
            this.projectsLoaded = true
         })

         api.gget("whoami")
            .then((r)=>{
               this.profile = r.data
               this.profileLoaded = true
            })
            .catch((e)=>{
               this.profile = {name: e}
            })
      }
   }
</script>
