<template>
   <div
      v-on:mouseenter ="$emit('mouseover')"
      v-on:mouseleave ="$emit('onmouseout')" class="layerview">

      <div class="row">
         <p>Intensity</p>
         <vue-slider
            ref="slider1"
            v-model="layer.fields.intensity"
            :min="intensity_min"
            :max="intensity_max"
            :interval="intensity_interval"
         />
      </div>

      <div class="row">
         <p>Confidence</p>
         <vue-slider
            ref="slider2"
            v-model="layer.fields.confidence"
            :min="confidence_min"
            :max="confidence_max"
            :interval="confidence_interval"
         />
      </div>

      <div class="row">
         <button v-on:click="$emit('deleteMe')">Delete me!</button>
      </div>

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
            confidence_min: -5,
            confidence_max: 5,
            confidence_interval: 1,
            intensity_min: -5,
            intensity_max: 5,
            intensity_interval: 1,
         }
      },
   }
</script>

<style scoped lang="scss">
@import "../sass/variables.sass";
.layerview {
   background: $ui_gray;
   margin: 5px;
   padding: 5px;
   border-radius: 5px;
}
input {
   width: 100%;
}

button {
   width: 100%;
}
</style>

