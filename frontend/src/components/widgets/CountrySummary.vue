<template>
   <tr>
      <td>
         {{ country.name }}
      </td>
      <td>
         <span v-if="shapes!==undefined">{{shapes}} prediction-areas</span>
      </td>
      <td>
         <span v-if="nonanswer">No conflict</span>
      </td>
      <td>
         <button class="continue" v-if="shapes!==undefined" v-on:click="go_to_editor">
            <span v-if="shapes>0">Revise</span>
            <span v-else>Add</span>
         </button>
      </td>
      <td>
         <button class="alt" v-on:click="clear">Clear</button>
      </td>
   </tr>
</template>
<style lang="sass" scoped>
button
   width: 100%
   font-size: 15px
   border-radius: 2px

td
   min-width: 40px

</style>
<script>
export default {
   props: ["country"],
   data(){
      return {
         shapes: undefined,
         nonanswer: false 
      }
   },
   mounted(){
      this.$api.get.rel(`projects/${this.country.gwno}/status`)
         .then((r)=>{
            this.shapes = r.data.shapes
            this.nonanswer = r.data.nonanswer
         })
         .catch((e)=>{
            console.error(e)
         })
   },
   methods: {
      go_to_editor(){
         this.$router.push(`ctry/${this.country.gwno}`)
      },
      clear(){
         let rq
         if(this.shapes>0){
            rq = this.$api.get.rel(`projects/${this.country.gwno}/clear`)
         } else {
            rq = this.$api.post.rel(`nonanswer/${this.country.gwno}`)
         }
         rq.then(()=>{
               this.$router.push("/")
            })
      },
   }
}
</script>
