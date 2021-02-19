<template>
   <Card :loaded="loaded">
      <template v-slot:header>
         <h1>MENU</h1>
      </template>
      <template v-slot:content>
         <div id="content-holder">
            <div id="profile-pic-holder">
               <account-box :size="200"></account-box>
            </div>
            <div id="menu-links-holder">
               <div id="menu-links">
                  <button title="Add new predictions"
                    v-on:click="$router.push('/')"
                    v-if="is_open">
                     <checkbox-multiple-marked :size="40"></checkbox-multiple-marked>
                     Participate
                  </button>
                  <button title="View evaluation"
                     v-on:click="$router.push('/results')">
                     <scale-balance :size="40"></scale-balance>
                     Evaluation
                  </button>
                  <button title="Change assigned countries"
                     v-on:click="$router.push('/assign')">
                     <map-plus :size="40"></map-plus>
                     Countries
                  </button>
                  <button title="Edit profile information"
                     v-on:click="$router.push('/questionaire')">
                     <account-edit :size="40"></account-edit>
                     Profile
                  </button>
               </div>
            </div>
         </div>
      </template>
      <template v-slot:footer>
         <div class="footer-buttons">
            <button title="Add new predictions"
               v-if="is_open && unfulfilled" v-on:click="$router.push('/')" 
               id="participate-button" class="progress">
               Participate
            </button>
            <button title="View evaluation"
               v-else v-on:click="$router.push('results')" 
               id="eval-button" class="alt">
               Evaluation
            </button>
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

#profile-pic-holder
   display: grid
   place-items: center

#menu-links-holder
   display: grid
   place-items: center

#menu-links
   padding: 40px 0
   display: grid
   grid-auto-flow: column
   grid-gap: 10px
   place-items: left 

#menu-links button
   display: grid
   background: $ui-darkgray
   padding: 20px 0
   height: 100px
   width: 100px 
   font-size: 16px

</style>
<script>
import Card from "@/components/Card"
import AccountBox from "vue-material-design-icons/AccountBox"
import AccountEdit from "vue-material-design-icons/AccountEdit"
import MapPlus from "vue-material-design-icons/MapPlus"
import CheckboxMultipleMarked from "vue-material-design-icons/CheckboxMultipleMarked"
import ScaleBalance from "vue-material-design-icons/ScaleBalance"
export default {
   components: {Card,AccountBox,AccountEdit,MapPlus,CheckboxMultipleMarked,ScaleBalance},
   computed:{
      loaded(){
         return this.unfulfilled !== undefined && 
            this.is_open !== undefined &&
            this.username !== undefined
      }
   },
   data(){
      return {
         is_open: undefined,
         unfulfilled: undefined,
         username: undefined,
      }
   },
   methods:{
      check_open(){
         this.$api.get.rel("period/open")
            .then((r)=>{
               this.is_open = r.data.open
            })
      },
      check_fulfilled(){
         this.$api.get.rel("profile/unfulfilled")
            .then((r)=>{
               this.unfulfilled = r.data.countries.length > 0
            })
      },
      fetch_username(){
         this.$api.get.rel("profile/whoami")
            .then((r)=>{
               this.username = r.data.name
            })
      },
   },
   mounted(){
      this.check_open()
      this.check_fulfilled()
      this.fetch_username()
   }
}
</script>
