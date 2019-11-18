<template>
   <div> 
      <div class="menu six columns" v-if="loaded">
         <div class="row">
            <div class="profile six columns">
               <h1>Hello {{profile.name}}!</h1>
               <p>
               You are participating in {{nProjects}} projects.
               </p>
            </div>

            <div class="projects six columns">
               <ProjectView 
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

<script charset="utf-8">
   import ProjectView from "./ProjectView.vue"
   import Spinner from "@/components/Spinner"

   export default {
      name: "ProjectMenu",

      data(){
         return {
            profile: {
               "name":"",
               "projects":[]
            },
            loaded: false,
         }
      },

      components: {
         ProjectView,
         Spinner,
      },

      computed: {
         projects(){
            return this.profile.projects
         },
         nProjects(){
            return this.projects.length
         }
      },

      methods: {
         chosen: function(project){
            this.$store.dispatch("chooseProject",project)
         }
      },

      mounted(){
         let user = this.$store.state.sessionInfo.uk
         let api = this.$store.state.apiURL
         let url = `${api}profile/${user}/`

         this.$http.get(url)
            .then(function(response){
               this.profile = response.body
               this.loaded = true 
            })
            .catch(function(){
               this.profile = {"name":"","projects":[]} 
            })
      }
   }
</script>
<style lang="sass" scoped> 
@import "../sass/variables.sass"

div.projects
   overflow-y: scroll
   height: $map_height / 1.1
   background: white
   padding: 15px
   border-radius: $roundedness
   border: 1px solid lightgray

div.menu
   width: 100%
   padding: 50px
   background: $ui_gray 
   height: $map_height
</style>
