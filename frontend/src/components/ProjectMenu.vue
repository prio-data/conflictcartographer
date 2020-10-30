<template>
   <div class="menucontainer"> 
      <div class="menu" v-if="loaded">
         <div class = "container">
            <div class="profile six columns">
               <h1>Greetings {{profile.name}}!</h1>
               <p>
               <!-- You are participating in {{nProjects}} projects.-->
               </p>
               The variables to code are 
               <span class="emphasis">intensity</span>
               and
               <span class="emphasis">confidence</span>.
               Please refer to the documentation regarding the definition of these variables.
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
   import Spinner from "../components/Spinner"

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
      },

      methods: {
         chosen: function(project){
            this.$store.dispatch("chooseProject",project)
         }
      },

      mounted(){
         let user = this.$store.state.sessionInfo.uk
         let api = this.$store.state.api
         api.get("assigned",(r)=>{
            this.profile = {"name":"noname","projects": r}
            this.loaded = true
         })
      }
   }
</script>
<style lang="sass" scoped> 
@import "../sass/variables.sass"

span.emphasis
   color: $ui_highlight

.container
   padding: 10px 20px
   width: 100%
   max-width: 85vw

.menucontainer
   width: 100vw
   height: $map_height / 1.1

div.projects
   height: $map_height / 1.1 - ($gaps * 4)
   overflow-y: scroll
   background: white
   border-radius: $roundedness
   border: 1px solid lightgray
   padding: 10px 20px

div.menu
   height: 100%
   width: 100%
   background: $ui_gray 

</style>
