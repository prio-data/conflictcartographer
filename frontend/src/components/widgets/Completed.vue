<template>
   <div v-if="loaded && completed">
      ✔️
   </div>
</template>
<style lang="sass" scoped>
@import "@/sass/variables"
div
   display: grid
   place-items: center
</style>
<script>
export default {
   name: "CompletedWidget",
   props: ["project"],
   data(){
      return {
         loaded: false,
         completed: false 
      }
   },
   mounted() {
      this.$store.state.api.gget(`pinfo/completed/${this.project.gwno}`)
         .then((r)=>{
            this.completed = r.data.completed
            this.loaded = true
         })
         .catch((e)=>{
            console.log(e)
         })

   }
}
</script>
