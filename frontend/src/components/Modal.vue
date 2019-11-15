<template>
   <div 
      v-if="show"
      class="modalwrapper">
      <div class="modalmessage">
         <div class="contentwrapper">
            <slot></slot>
         </div>
         <div class="closewrapper">
            <button 
               v-on:click="toggle"
               class="closebutton">Close</button>
         </div>
      </div>
   </div>
</template>

<script charset="utf-8">
export default {
   name: "modalmessage",
   data(){
      return {
         show: true
      }
   },
   methods: {
      toggle(){
         this.show = !this.show
         this.$emit("toggle")
      }
   }

}
</script>

<style scoped lang="sass">
.modalwrapper
   position: absolute !important
   overflow: auto !important
   top: 0
   left: 0
   width: 100vw
   height: 100vh
   text-align: center
   background: rgba(0,0,0,0.5)

.modalmessage
   display: inline-block
   margin-top: 5vh 
   padding: 50px
   background: white 
   border-radius: 15px

.contentwrapper
   text-align: left
   height: 75vh 
   width: 50vw 
   overflow: auto


.closewrapper
   text-align center

.closebutton
   display: inline-block
   
   

</style>
