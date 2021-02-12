<template>
   <div class="layerview" :class="{noticeme: nagging}" v-on:mouseover="focus">
      <div class="header">
         <button v-on:click="deleteme">
            <img class="trashicon" :src="trashicon">
         </button>
      </div>
      <div class="controls">
         <div class="sliders">
            <p>Expected no. of casualties</p>
            <div class="intensityControl" v-for="choice in choices" v-bind:key="choice.key">
               <input 
                  v-on:change= "changed" 
                  v-model="layer.values.intensity" 
                  :value="choice.value" 
                  type="radio">
               <label :for="choice.key">{{choice.key}} casualties</label>
            </div>
            <p>Confidence: {{layer.values.confidence}}%</p>
            <vue-slider
               ref="slider2"
               v-on:change = "changed"
               v-model="layer.values.confidence"
               :min="confidence_min"
               :max="confidence_max"
               :interval="confidence_interval"
            />
         </div>
      </div>
   </div>
</template>

<style scoped lang="sass">
@import "@/sass/variables.sass"
@import "@/sass/animations.sass"
@import "@/sass/vueslider"

#mousesensor
   display: k

.layerview
   display: grid
   background: $ui_gray
   padding: $menu-gaps 
   border-radius: $roundedness 
   margin-bottom: $menu-gaps
   border-bottom: 4px solid $ui-darkgray

.noticeme
   animation: nagging 1s ease-in-out infinite

.header button
   width: 25px 
   height: 25px
   padding: 0px 
   border: none
   float: right
   background: $ui_remove_1

.controls
   font-size: 20px
   line-height: 2

.controls p
   margin-bottom: 0px

// Radio controls
div.intensityControl
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

.trashicon
   display:none
   padding-top: 2px
   max-width: 80%
   max-height: 80%
   filter: opacity(0)

button:hover>.trashicon
   filter: opacity(0.4)
button:hover
   background: $ui_remove_2 

</style>


<script charset="utf-8">
   import vueSlider from "vue-slider-component" 
   import "vue-slider-component/theme/antd.css"
   import trashicon from "../images/trash2.svg"
   import debounce from "@/util/debounce"

   export default {
      name: "LayerView",
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
            ],
            nagging: false 
         }
      },

      methods: {
         changed: debounce(function(){
            this.$store.state.api.put.abs(this.layer.url,{data: this.layer})
               .then(()=>{
                  if(this.nagging){
                     this.nagging = false
                  }
               })
               .catch((e)=>{
                  console.error(e)
               })

         }, 500),

         deleteme(){
            this.$store.state.api.del.abs(this.layer.url)
               .then(()=>{
                  this.$emit("deleted",this.layer.url)
               })
               .catch((e)=>{
                  console.error(e)
               })
         },

         focus(e){
            if(e.target == this.$el){
               this.$emit("focus",this.layer)
            }
         },
      },

      mounted(){
         if(this.layer.values.confidence == 50 && this.layer.values.intensity == 0){
            this.nagging = true
         }
      },


   }
</script>
