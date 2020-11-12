<template>
   <div
      v-on:mouseenter ="$emit('mouseover')"
      v-on:mouseleave ="$emit('onmouseout')" class="layerview">
      <div class="header">
         <button v-on:click="$emit('deleteMe')">
            <img class="trashicon" :src="trashicon">
         </button>
      </div>
      <div class="controls">
         <div class="sliders">
            <p>Expected no. of casualties</p>
            <div id="intensity" v-for="choice in choices" v-bind:key="choice.key">
               <input 
                  v-on:change= "$emit('change')" 
                  v-model="layer.intensity" 
                  :name="choice.key" 
                  :value="choice.value" 
                  type="radio">
               <label :for="choice.key">{{choice.key}} casualties</label>
            </div>
            <p>Confidence: {{layer.confidence}}%</p>
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

// Radio controls
div#intensity
   display: grid
   grid-template-columns: 30px auto
   font-size: 18px
   align-items: center
   height: 29px
   line-height: 1px

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
            choices: [
               {key:"0-1",value:0},
               {key:"2-25",value:1},
               {key:"26-99",value:2},
               {key:"100-999",value:3},
               {key:">1000",value:4},
            ]
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
