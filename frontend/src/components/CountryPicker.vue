<template>
   <div id="root">
      <div id="selectHolder" v-if="active">
         <select name="country" v-model="selected">
            <option v-for="c in choices" :value="c.pk">{{c.name}}</option>
         </select>
         <div class="divbutton" v-on:click="dispatch">Add</div>
         <div class="divbutton" v-on:click="active = false">X</div>
      </div>
      <button id="addProjects" v-if="!active" v-on:click="activate">+</button>
   </div>
</template>
<style lang="sass" scoped>
@import "@/sass/variables.sass"

#root
   display: grid
   width: 100%

#selectHolder
   display: grid
   grid-gap: $project-menu-card-gaps 
   grid-template-columns: auto $project-menu-card-button-size $project-menu-card-button-size 
   margin-bottom: $menu-gaps

.divbutton
   background: $ui-darkgray
   border-radius: $roundedness
   border-bottom: 4px solid $ui-darkergray
   display: grid
   place-items: center
   font-size: $project-menu-card-font-size 

.divbutton:hover
   background: $ui-highlight 
   cursor: pointer

select
   background: $ui-gray
   height: $project-menu-card-height
   font-size: $project-menu-card-font-size 
select:focus
   border: 1px solid $ui-highlight

button#addProjects
   border: none
   height: $project-menu-card-height 
   display: grid
   place-items: center
   font-size: 80px
   line-height: 0
   color: $ui-darkgray
   background: $ui-lightgray 

button#addProjects:hover
   color: $ui-highlight

</style>
<script>

export default {
   name: "CountryPicker",
   data(){
      return {
         active: false,
         choices: [],
         selected: {} 
      }
   },
   methods: {
      activate(){
         this.choices = this.$store.state.api.gget("projectchoices")
            .then((r)=>{
               this.choices = r.data.projects
               this.selected = this.choices[0]
               this.active=true
            })
            .catch((e)=>{
               this.active=false
            })
      },
      dispatch(){
         this.active = false
         this.$store.state.api.gpost("editprojects/add",{"pk":this.selected})
            .then((r)=>{
               this.$emit("addedProject")
               })
            .catch((e)=>{
               console.log(e)
            })
      }
   }
}
</script>
