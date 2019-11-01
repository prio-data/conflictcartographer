<template>
   <div v-on:click="$emit('chosen')" class="card">
      <p>{{ project.name }}</p>
   </div>
</template>

<script charset="utf-8">
   export default {
      name: "ProjectView",

      props: ["project"],

      components: {
      },

      methods: {
      },

      computed: {
      },

      data: function() {
         return {}
      },
   }
</script>

<style lang="sass" scoped> 
@import "../sass/variables.sass"

div.card
   width: 400px
   height: $map_height - 30px

   display: inline-block
   margin-right: 5px

   background: $ui_gray 
   border-radius: $roundedness

div.card:hover
   background: $ui_highlight

div.card p
   line-height: 1
   font-size: 50px
   padding: 15px
</style>
