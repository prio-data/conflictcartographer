<template>
   <div>
      <h1>Hello world!!</h1>
      <p>{{msg}}</p>
   </div>
</template>

<script charset="utf-8">
   export default {
      name: "TestComponent",
      props: {
         msg: String
      }
   }
</script>

<style scoped lang="sass" type="text/css" media="screen">
   @import "../variables.sass"
   h1
      :color $maincolor_1
   p
      :color $maincolor_2 
</style>
