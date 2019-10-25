<template>
   <div class = "container">
      <code>{{JSON.stringify(data)}}</code>
   </div>
</template>

<script charset="utf-8">
   export default {
      name: "Message",
      props: ["data"],
      delimiters: ["[[","]]"]
   }
</script>

<style scoped lang="sass" type="text/css" media="screen">
</style>

