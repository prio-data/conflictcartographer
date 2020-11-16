<template>
   <div id="pm-wrapper">
      <div id="pm" v-if="profile.waiver">
         <div class="pane infobar" v-if="profileLoaded">
            <Profile :profile="profile"/>
            <MainDescription/>
            <Calendar/>
         </div>
         <Spinner v-else/>
         <div class="pane projects">
            <h1 id="menuheader">Countries</h1>
            <div id="projectlist" v-if="projectsLoaded">
               <div v-for="project in projects" class="pmcard">
                  <ProjectView class="card"
                     :key="project.url"
                     :project="project"
                     v-on:chosen="chosen(project)"
                     v-on:deselected="refreshProjects">
                  </ProjectView>
               </div>
               <div class="pmcard">
                  <CountryPicker v-on:addedProject="refreshProjects"/>
               </div>
            </div>
            <Spinner v-else/>
         </div>
      </div>
      <Waiver v-else/>
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
   margin: $menu-gaps*6 0 0 $menu-gaps
   margin-top: $menu-gaps*6

.infobar > *
   margin-bottom: $menu-gaps

#projectlist
   background: $ui-background 
   border-radius: $roundedness
   overflow-y: scroll 
   max-height: 100% 
   height: 100%

.pmcard
   margin: $menu-gaps $menu-gaps 0 $menu-gaps

h1#menuheader
   line-height: 20px 

</style>

<script charset="utf-8">
   import ProjectView from "./ProjectView.vue"
   import Spinner from "../components/Spinner"
   import Profile from "@/components/Profile"
   import Waiver from "@/components/Waiver"
   import MainDescription from "@/components/MainDescription"
   import CountryPicker from "@/components/CountryPicker"
   import Calendar from "@/components/Calendar"

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
         Waiver,
         CountryPicker,
         Calendar
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
         refreshProjects(){
            this.projectsLoaded = false
            this.$store.state.api.get("assigned",(r)=>{
               this.projects = r
               this.projectsLoaded = true
            })
         }
      },

      mounted(){
         let api = this.$store.state.api

         this.refreshProjects()
         /*
         api.get("assigned",(r)=>{
            this.projects = r
            this.projectsLoaded = true
         })
         */

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
