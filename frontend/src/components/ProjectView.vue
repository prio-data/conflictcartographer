<template>
   <div id="container">
      <div id="actions">
         <div class="divbutton" v-on:click="$emit('chosen')">Draw shapes</div>
         <div class="divbutton">No conflict</div>
      </div>
      <div id="display">
         <div class="header">
            {{ project.name }}
         </div>
         <div id="displaywidgets">
            <CompletedWidget :project="project"/>
         </div>
      </div>
      <div class="divbutton" id="deselectButton" v-on:click="deselect">X</div>
   </div>
</template>

<script charset="utf-8">
import CompletedWidget from "@/components/widgets/Completed"

export default { name: "ProjectView",
   props: ["project"],
   components: {
      CompletedWidget,
   },
   methods: {
      deselect(){
         this.$store.state.api.gpost("editprojects/remove",{"pk":this.project.gwno})
            .then((r)=>{
               this.$emit("deselected")
            })
            .catch((e)=>{
               console.log(e)
            })
      }
   }
}
</script>

<style lang="sass" scoped> 
@import "../sass/variables.sass"

#container
   display: grid
   grid-template-columns: $project-menu-card-button-size*2 auto $project-menu-card-button-size 
   grid-gap: $project-menu-card-gaps 
   height: $project-menu-card-height 
   background: $ui-gray
   border-radius: $roundedness
   padding: 0 $project-menu-card-gaps

#actions
   display: grid
   margin-bottom: $project-menu-card-gaps
   //grid-template-rows: 1fr
   //grid-gap: $project-menu-card-gaps
   //grid-auto-flow: column

.divbutton
   font-size: $project-menu-card-font-size 
   background: $ui-darkgray
   display: grid
   place-items: center
   border-bottom: 4px solid $ui-darkergray
   border-radius: $roundedness
   cursor: pointer
   margin: $project-menu-card-gaps 0
   margin-top: $project-menu-card-gaps - 2px

#actions > .divbutton
   margin-bottom: 0

.divbutton:hover
   background: $ui-highlight

#display
   display: grid
   grid-template-rows: 40px auto 
   margin: $project-menu-card-gaps+(-2) 0 

#displaywidgets
   display: flex
   background: $ui-lightgray
   border-radius: $roundedness
   margin-bottom: 2px 
   padding: 0 $project-menu-card-gaps

.mockwidget
   background: $ui-highlight
   margin: $project-menu-card-gaps 0 $project-menu-card-gaps $project-menu-card-gaps
   width: 60px
   border-radius: $roundedness

.header
   padding-left: $project-menu-card-gaps
   //background: $ui-lightgray
   border-radius: $roundedness
   font-size: $project-menu-card-font-size 
</style>
