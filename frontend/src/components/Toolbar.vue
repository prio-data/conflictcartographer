<template>
   <div>
      <div class="row">
         <div class="six columns">
            <button v-on:click="$emit('pushData')" class="button-primary">Save</button>
         </div>
      </div>

      <div class="row">
         <div v-for="layer in layers" v-bind:key="layer.id">
            <layer-view 
               v-on:mouseover = "focusOn(layer)"
               v-on:onmouseout = "unfocus"
               v-on:deleteMe = "deleteLayer(layer)" 
               :layer="layer"/>
         </div>
      </div>
   </div>
</template>

<script charset="utf-8">
   import LayerView from "./LayerView.vue"

   export default {
      name: "Toolbar",

      methods: {
         deleteLayer: function(layer){
            this.$store.commit("deleteLayer",layer)
         },

         focusOn: function(layer){
            this.$store.commit("focusOn",layer)
         },

         unfocus: function(){
            this.$store.commit("unfocus")
         }
      },

      computed: {
         layers: function(){
            return this.$store.state.layers
         }
      },

      components: {
         LayerView 
      },
   }
</script>

<style scoped lang="sass" type="text/css" media="screen">
button
   margin-top: 5px
   margin-bottom: 5px

</style>

