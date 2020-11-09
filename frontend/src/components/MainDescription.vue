<template>
   <div id="project-description">
      <h1>{{ title }}</h1>
      <p v-html="description"></p>
   </div>
</template>
<style lang="sass" scoped>
@import "@/sass/variables.sass"
#project-description
   padding: 0px $menu-gaps 0px $menu-gaps
   min-height: 0px
</style>
<script>
export default {
   name: "MainDescription",
   data(){
      return {
         title: "",
         description: ""
      }
   },
   mounted(){
      this.$store.state.api.gget("currentproject")
         .then((r)=>{
            this.title = r.data.title
            this.description = r.data.description
         })
         .catch((e)=>{
            console.log(e)
            this.title = "Error"
            this.description = "Error fetching project description.".repeat(20)
         })
   }
}
</script>
