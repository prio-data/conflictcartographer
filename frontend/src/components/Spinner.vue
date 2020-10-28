<template>
   <div id="holder">
      <img id="spinner" :src="path" alt="">
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
   width: 100% 
   text-align: center
#spinner
   margin: 30vh 0px
   display: inline-block
</style>
