<template>
   <div class="sbwidget">
      <button class="closed" id="activatebutton" v-if="mode=='inactive'" v-on:click="toggle">
         Give us some feedback!
      </button>
      <div class="open" id="form" v-if="mode=='active'">
         <div class="label">Feedback text</div>
         <textarea v-model="feedback"/>
         <div class="label">Star rating</div>
         <div id="stars">
            <input v-model="stars" value=1 type="radio">
            <input v-model="stars" value=2 type="radio">
            <input v-model="stars" value=3 type="radio">
            <input v-model="stars" value=4 type="radio">
            <input v-model="stars" value=5 type="radio">
         </div>
         <button v-on:click="submit">Submit</button>
      </div>
      <div class="thanks" v-if="mode=='thanks'">
         <p>
            Thanks!
         </p>
      </div>
   </div>
</template>
<style lang="sass" scoped>
@import "@/sass/variables"
@import "@/sass/sidebarwidget"
@import "@/sass/generic"

#form
   display: grid
   place-items: center
   grid-template-rows: 30px 2fr 30px 20px 50px

#form>textarea
   height: 100%
   width: 100%
   border-top: 2px solid $ui-darkergray 
   border-right: 1px solid $ui-darkergray 
   border-left: 1px solid $ui-darkergray 
   border-radius: $roundedness

#form>button
   width: 100%

#stars
   display: grid
   width: 100%
   grid-template-rows: 1fr
   grid-template-columns: repeat(5, 1fr)
   place-items: center

</style>
<script>
import SbWidget from "@/mixins/SbWidget"

export default {
   name: "Feedback",
   mixins: [SbWidget],
   data(){
      return {
         feedback: "Type your feedback here",
         stars: 3,
      }
   },
   methods: {
      submit(){
         this.$store.state.api.post.rel("feedback",{
            data: {
               message: this.feedback,
               stars: this.stars
            }})
            .then((r)=>{
               this.toggle()
            })
            .catch((e)=>{
               console.log(e)
            })
      }
   }
}
</script>
