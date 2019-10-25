<template>
   <div
      v-on:mouseenter ="$emit('mouseover')"
      v-on:mouseleave ="$emit('onmouseout')">
      <div class="row">
         <p>{{layer.type}}</p>
         <button v-on:click="$emit('deleteMe')">Delete me!</button>
      </div>
      <input type="text" name="layername" value="A layer" id="layername">
      <vue-slider
         ref="slider"
         v-model="sliderval"
      />
   </div>
</template>

<script charset="utf-8">
   import vueSlider from "vue-slider-component" 
   import "vue-slider-component/theme/antd.css"
   export default {
      name: "layer-view",
      props: ["layer"],
      components: {vueSlider},
      data: function(){
         return {
            sliderval: 0
         }
      },
   }
</script>

<style scoped lang="sass" type="text/css" media="screen">
</style>

