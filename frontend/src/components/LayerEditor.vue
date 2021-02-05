<template>
   <div>
      <h2>Intensity</h2>
      <vue-slider 
         v-model="layer.feature.properties.intensity"
         :min="0"
         :max="5"
         :interval="1"
         >
      </vue-slider>
      <h2>Confidence</h2>
      <vue-slider 
         v-model="layer.feature.properties.confidence"
         :min="0"
         :max="100"
         :interval="1"
         >
      </vue-slider>
   </div>
</template>
<style lang="sass" scoped>
div
   padding: 20px 40px

h2
   margin: 0
</style>
<script>

import VueSlider from "vue-slider-component"
import "vue-slider-component/theme/antd.css"

export default {
   components:{VueSlider},
   props: ["layer"],
}
</script>
