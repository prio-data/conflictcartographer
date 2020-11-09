<template>
   <div id="holder">
      <img id="spinner" :src="path" alt="">
      <div id="errmsg">
         <slot/>
      </div>
   </div>
</template>

<script>
import spinner from "../images/spinner.gif"

export default {
   name: 'Spinner',
   data(){
      return {
         path: spinner
      }
   }
}
</script>

<style scoped lang="sass">
#holder
   height: 100%
   width: 100%
   display: grid
   place-items: center
#errmsg
   color: red
   font-size: 28px
</style>
