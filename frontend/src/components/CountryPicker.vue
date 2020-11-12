<template>
   <div id="root">
      <div class="pvlike" id="selectHolder" v-if="active">
         <select name="country" v-model="selected">
            <option v-for="c in choices" :value="c.pk">{{c.name}}</option>
         </select>
         <div id="button" v-on:click="dispatch">OK</div>

      </div>
      <button class="pvlike" id="addProjects" v-on:click="activate">+</button>
   </div>
</template>
<style lang="sass" scoped>
@import "@/sass/variables.sass"

.pvlike 
   border: none
   height: 70px 

#root
   display: grid
   width: 100%

#selectHolder
   display: grid
   grid-template-columns: $project-menu-ratio 
   margin-bottom: $menu_gaps

#selectHolder > #button
   background: $ui-darkgray
   margin-right: $menu_gaps
   border-radius: $roundedness
   border-bottom: 4px solid $ui-darkergray
   display: grid
   place-items: center

#selectHolder > #button:hover
   background: $ui-highlight 
   cursor: pointer

select
   background: $ui-lightgray
   margin: 0px $menu_gaps
   height: 80px

button#addProjects
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

</style>
<script>

export default {
   name: "CountryPicker",
   data(){
      return {
         active: false,
         choices: [],
         selected: ""
      }
   },
   methods: {
      activate(){
         this.active=true
         this.choices = this.$store.state.api.gget("projectchoices")
            .then((r)=>{
               this.choices = r.data.projects
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
