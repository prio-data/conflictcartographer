<template>
   <div class="sbwidget">
      <button class="closed" id="activatebutton" v-if="mode=='inactive'" v-on:click="toggle">
         Share this app
      </button>
      <div class="open" id="form" v-if="mode=='active'">
         <button v-on:click="toggle">Submit</button>
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
</style>

<script>
import SbWidget from "@/mixins/SbWidget"
export default {
   name: "Share",
   mixins: [SbWidget],
}
</script>
