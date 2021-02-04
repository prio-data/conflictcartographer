<template>
   <div>
      <input v-model="layer.feature.properties.intensity" type="number">
   </div>
</template>
<style></style>
<script>
export default {
   props: ["layer"],
}
</script>
