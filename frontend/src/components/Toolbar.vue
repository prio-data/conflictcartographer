<template>
   <div>
      <div class="viewcontainer">
         <h1>Drawn areas:</h1>
         <div v-for="layer in layers" v-bind:key="layer.url">
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
@import "../sass/variables.sass"

$padding: 5px
$darken: 0.4

h1
   color: white

div.viewcontainer
   padding: 0px $padding

   height: $map_height
   width: 220px 

   position: absolute
   top: $navbar_height 
   right: 0

   background: rgba(0,0,0,$darken)

</style>

