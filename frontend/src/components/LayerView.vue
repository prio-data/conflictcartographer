<template>
   <div
      v-on:mouseenter ="$emit('mouseover')"
      v-on:mouseleave ="$emit('onmouseout')" class="layerview">
      <div class="header">
         <button v-on:click="$emit('deleteMe')"></button>
      </div>
      <div class="controls">
         <div class="sliders">
            <p>Intensity</p>
            <vue-slider
               ref="slider1"
               v-on:drag-end = "$emit('change')"
               v-model="layer.intensity"
               :min="intensity_min"
               :max="intensity_max"
               :interval="intensity_interval"
            />
         </div>
         <div class="row">
            <p>Confidence</p>
            <vue-slider
               ref="slider2"
               v-on:drag-end = "$emit('change')"
               v-model="layer.confidence"
               :min="confidence_min"
               :max="confidence_max"
               :interval="confidence_interval"
            />
         </div>
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

<style scoped lang="sass">
@import "../sass/variables.sass"

.layerview
   width: 200px 
   background: $ui_gray

   margin-bottom: $gaps
   margin-top: $gaps
   margin-right: $gaps
   padding: $gaps

   border-radius: $roundedness 


.header button
   width: 25px 
   height: 25px
   padding: 0px 

   border: none

   float: right

   background: $ui_remove_1

.header:hover button
   background: $ui_remove_2 

.controls
   font-size: 20px
   line-height: 2

.controls p
   margin-bottom: 0px

// Slider
.vue-slider-ltr
   margin-right: 5px
   margin-left: 5px

//div.controls
   display: none

.layerview:hover div.controls
   display: inline

</style>

