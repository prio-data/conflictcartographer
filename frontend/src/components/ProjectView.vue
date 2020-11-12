<template>
   <div id="container">
      <div v-on:click="$emit('chosen')" id="project-card">
         <p class="projecttitle">{{ project.name }}</p>
      </div>
      <div id="deselectButton" v-on:click="deselect">X</div>
   </div>
</template>

<script charset="utf-8">
export default { name: "ProjectView",
   props: ["project"],
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
   grid-template-columns: $project-menu-ratio 
   grid-gap: $menu-gaps * 0.5

#deselectButton
   background: $ui-darkgray
   display: grid
   place-items: center
   border-bottom: 4px solid $ui-darkergray
   border-radius: $roundedness

#deselectButton:hover
   background: $ui-highlight

div#project-card
   padding: $menu-gaps
   height: 80px 
   background: $ui_darkgray
   border-radius: $roundedness
   border-bottom: 4px solid $ui-darkergray 
   color: $ui_lightgray
   font-size: 30px
   cursor: pointer

div#project-card:hover
   background: $ui_highlight
</style>
