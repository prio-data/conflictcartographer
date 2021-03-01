<template>
   <Card :loaded="true">
      <template v-slot:header>
         <h1>MENU</h1>
      </template>
      <template v-slot:content>
         <div id="content-holder">
            <div id="profile-pic-holder">
               <scale-balance :size="200"></scale-balance>
            </div>
            <p>
               We're working on implementing evaluation of conflict predictions. Check this page in June to see your results!
            </p>
         </div>
      </template>
      <template v-slot:footer>
         <div class="footer-buttons">
         </div>
      </template>
   </Card>
</template>
<style lang="sass" scoped>
@import "@/sass/variables"

#participate-button
   background-color: $ui-highlight

#eval-button
   background-color: $ui-progress-alt

#content-holder
   padding: 0 10px

#profile-pic-holder
   display: grid
   place-items: center

</style>
<script>
import Card from "@/components/Card"
import ScaleBalance from "vue-material-design-icons/ScaleBalance"
export default {
   components: {Card,ScaleBalance},
   computed:{
      loaded(){
         return is_open !== undefined
      }
   },
   data(){
      return {
         is_open: undefined
      }
   },
   methods:{
      check_open(){
         this.$api.get.rel("period/open")
            .then((r)=>{
               this.is_open = r.data.open
            })
      }
   },
   mounted(){
      this.check_open()
   }
}
</script>
