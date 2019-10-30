<template>
   <div>
      <div class="row">
         <div v-for="layer in layers" v-bind:key="layer.id">
            <layer-view 
               v-on:mouseover = "focusOn(layer)"
               v-on:onmouseout = "unfocus"
               v-on:deleteMe = "deleteLayer(layer)" 
               v-on:change = "updateLayer(layer)"
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
         
         updateLayer: function(layer){
            this.$store.commit("updateLayer",layer)
         },

         focusOn: function(layer){
            this.$store.commit("focusOn",layer)
         },

         unfocus: function(){
            this.$store.commit("unfocus")
         },
         
         valueChange(){
            console.log("something changed")
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
   @import "../sass/variables.sass"
   margin-top: $gaps 
   margin-bottom: $gaps
</style>

