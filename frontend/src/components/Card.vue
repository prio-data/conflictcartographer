<template>
   <div class="container">
      <div class="card">
         <div class="holder header">
            <slot name="header"></slot>
         </div>
         <div class="holder content">
            <slot name="content"></slot>
         </div>
         <div class="holder footer">
            <slot name="footer"></slot>
         </div>
         <div class="overlay">
            <slot name="overlay"></slot>
         </div>
      </div>
   </div>
</template>
<style lang="sass" scoped>
@import "@/sass/variables"

.holder
   overflow: hidden

.container
   width: 100vw
   height: 100vh

.card
   height: 100%
   width: 100%
   display: grid
   grid-template-rows: 60px 1fr 100px 
   position: relative

.content
   overflow-y: auto 

.header 
   text-align: center

   h1
      font-size: 20px

.overlay
   position: absolute 
   top: 0
   left: 0
   height: 100%
   width: 100%
   pointer-events: none

@media only screen and (min-width: $mob-width)
   .card
      width: $mob-width*1.1
      height: $mob-height*1.1
      margin: 20px 0
      box-shadow: 0px 3px 5px 2px #eee
      border: 1px solid gray

   .container
      display: grid
      justify-items: center

   .container
      overflow-y: scroll

</style>
<script>
export default {
   name: "Card"
}
</script>
