<template>
   <div class="container">
      <div class="card">
         <div class="overlay loading-cover" :class="{loaded: loaded}">
            <Spinner></Spinner>
         </div>
         <div class="holder header">
            <div id="card-header-holder">
               <button v-on:click="go_to_router" id="card-header-back-button">⌂</button>
               <div id="card-header-title">
                  <slot name="header"></slot>
               </div>
               <button v-on:click="go_to_info" id="card-header-help-button">?</button>
            </div>
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

@keyframes fade
   0%
      opacity: 100% 
   100%
      opacity: 0%
      display: none

.overlay.loading-cover
   background: #aaa 
   height: 100%
   width: 100%
   display: grid
   place-items: center
   z-index: 999
   pointer-events: none

.overlay.loading-cover.loaded
   animation-name: fade
   animation-duration: 0.5s 
   animation-fill-mode: forwards

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

#card-header-holder
   display: grid
   grid-template-columns: 60px 1fr  60px

#card-header-holder>button
   border: none
   background: none
   color: $ui-darkergray
   //font-size: 18px
   font-weight: bold

#card-header-back-button
   font-size: 30px

#card-header-holder>button:hover
   color: $ui-highlight

#card-header-title
   text-align: center

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
import Spinner from "@/components/Spinner"
export default {
   name: "Card",
   components:{Spinner},
   props: {
      loaded: {
         type: Boolean,
         default: false 
      }
   },
   methods:{
      go_to_router(){
         this.$router.push("/")
      },
      go_to_info(){
         this.$router.push("/info")
      },
   }
}
</script>
