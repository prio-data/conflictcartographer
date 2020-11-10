<template>
   <div
      v-on:mouseenter ="$emit('mouseover')"
      v-on:mouseleave ="$emit('onmouseout')" class="layerview">
      <div class="header">
         <button v-on:click="$emit('deleteMe')">
            <img class="trashicon" :src="trashicon">
         </button>
      </div>
      <div>
         Estimation: {{ lower_deaths }} - {{ upper_deaths }} casualties
      </div>
      <div class="controls">
         <div class="sliders">
            <p>Intensity</p>
            <vue-slider
               ref="slider1"
               v-on:change = "$emit('change')"
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
               v-on:change = "$emit('change')"
               v-model="layer.confidence"
               :min="confidence_min"
               :max="confidence_max"
               :interval="confidence_interval"
            />
         </div>
      </div>
   </div>
</template>

<style scoped lang="sass">
@import "../sass/variables.sass"

.layerview
   display: grid
   background: $ui_gray
   padding: $menu-gaps 
   border-radius: $roundedness 
   margin-bottom: $menu-gaps
   border-bottom: 4px solid $ui-darkgray

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

.trashicon
   display:none
   padding-top: 2px
   max-width: 80%
   max-height: 80%
   filter: opacity(0)

button:hover .trashicon
   filter: opacity(0.4)

</style>


<script charset="utf-8">
   import vueSlider from "vue-slider-component" 
   import "vue-slider-component/theme/antd.css"
   import trashicon from "../images/trash2.svg"

   export default {
      name: "layer-view",
      props: ["layer"],
      components: {vueSlider},
      data: function(){
         return {
            trashicon: trashicon,
            confidence_min: 0,
            confidence_max: 100,
            confidence_interval: 1,
            intensity_min: 0,
            intensity_max: 1000,
            intensity_interval: 100,
         }
      },

      computed: {
         lower_deaths(){
            return this.layer.intensity 
         },
         upper_deaths(){
            return this.layer.intensity
         }
      }
   }
</script>
