<template>
   <div class="sbwidget">
      <button class="closed" id="activatebutton" v-if="mode=='inactive'" v-on:click="toggle">
         Share this app
      </button>
      <div class="open" id="form" v-if="mode=='active'">
         <label for="email">Email</label>
         <input name="email" type="text" v-model="email" placeholder="example@email.com">
         <label for="message">Message</label>
         <input name="message" type="text" v-model="message" placeholder="Check out this awesome app!">
         <button v-on:click="share">Submit</button>
      </div>
      <div class="thanks" v-if="mode=='thanks'">
         <p v-if="error == ''">
            Thanks!
         </p>
         <p v-else>
            {{ error }}
         </p>
      </div>
   </div>
</template>

<style lang="sass" scoped>
@import "@/sass/variables"
@import "@/sass/sidebarwidget"
@import "@/sass/generic"
</style>

<script>
import SbWidget from "@/mixins/SbWidget"
export default {
   name: "Share",
   mixins: [SbWidget],
   data(){
      return {
         error:"",
         email:"",
         message:""
      }
   },
   methods: {
      share(){
         this.$store.state.api.post.rel("share",{data: {email: this.email, message: this.message}})
            .then((r)=>{
               this.toggle()
            })
            .catch((e)=>{
               this.error = e
               this.toggle()
            })
      }
   }
}
</script>
