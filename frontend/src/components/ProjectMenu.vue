<template>
   <div> 
      <div class="menu six columns">
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
                  :project="project"
                  v-on:chosen="chosen(project)">
               </ProjectView>
            </div>
         </div>
      </div>
      <div class="six columns"></div>
   </div>
</template>

<script charset="utf-8">
   import ProjectView from "./ProjectView.vue"

   export default {
      name: "ProjectMenu",

      props: ["projects"],

      components: {
         ProjectView,
      },

      computed: {
         profile(){
            return this.$store.state.profile
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
