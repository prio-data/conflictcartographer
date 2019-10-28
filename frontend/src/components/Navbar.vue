<template>
   <div>
      <h1>{{ title }}</h1>
   </div>
</template>

<script charset="utf-8">
   export default {
      name: "Toolbar",
      props: ["title"],
      methods: {
         y: function(){} 
      },
   }
</script>

<style scoped lang="sass" type="text/css" media="screen">
h1
   margin-left: 15px
</style>

