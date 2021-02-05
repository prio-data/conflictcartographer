<template>
   <div class="overlay editor-overlay">
      <div class="overlay-viewport"></div>
         <div class="popup">
            <div v-if="mode!==1" class="active">
               <div class="control-panel">
                  <slot name="editor-panel"></slot>
               </div>
               <div class="control-panel button-panel">
                  <button v-on:click="$emit('reset')">Back</button>
               </div>
            </div>
            <div v-else class="controls">
               <div class="control-panel edit-actions button-panel" v-if="value">
                  <button v-on:click="$emit('startdraw')">Draw</button>
                  <button v-on:click="$emit('startdelete')">Erase</button>
               </div>
               <div class="control-panel shape-actions" v-else>
               </div>
            </div>
         </div>
         <div class="control-panel navigation-controls button-panel">
            <button v-on:click="go_to_router" class="continue">Submit</button>
            <button class="alt" v-on:click="toggle">Help</button>
         </div>
   </div>
</template>
<style lang="sass" scoped>
@import "@/sass/variables"

.editor-overlay
   display: grid
   grid-template-rows: auto $tray-size*2 $tray-size 

.button-panel
   padding: 10px

.control-panel
   pointer-events: auto
   display: grid
   //padding: 0 20px
   grid-gap: 10px
   background: #ffa 

.edit-actions
   grid-template-columns: 2fr 1fr

.navigation-controls
   grid-template-columns: 2fr 1fr

.control-panel.shape-actions
   height: 100%

.popup
   display: flex
   flex-direction: column-reverse

@media only screen and (min-width: $mob-width)
   .overlay
      justify-items: center
   .overlay div
      width: $mob-width

</style>
<script>
export default {
   props: ["mode"],

   data(){
      return {
         value: true 
      }
   },
   methods:{
      toggle(){
         this.value = !this.value
      },
      go_to_router(){
         this.$router.push("/")
      }
   },
}
</script>
