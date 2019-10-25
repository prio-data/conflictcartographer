<template>
   <div>
      <p>{{item.content}}</p>
      <button v-on:click="$emit('deleteMe')">Delete me!</button>
   </div>
</template>

<script charset="utf-8">
   export default {
      name: "item-view",
      props: ["item"]
   }
</script>

<style scoped lang="sass" type="text/css" media="screen">
</style>

