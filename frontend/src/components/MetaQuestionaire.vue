<template>
<Card>
   <template v-slot:header>
      <h1>PERSONALIA</h1>
   </template>
   <template v-slot:content>
      <div id="content-root">
         <div id="prompt">
            <p>Please add some details about yourself</p>
         </div>
         <div id="questions">
            <Question v-for="question in questions" :question="question" :key="question.title"></Question>
         </div>
      </div>
   </template>
   <template v-slot:footer>
      <div class="footer-buttons">
         <button v-on:click="to_router" class="continue">Submit</button>
         <button class="alt">Skip</button>
      </div>
   </template>
</Card>
</template>
<style lang="sass" scoped>
@import "@/sass/variables"
@import "@/sass/global"

#content-root
   display: grid
   grid-template-rows: 100px auto
   height: 100%
   padding: 10px

</style>

<script>
import Card from "@/components/Card"
import Question from "@/components/Question"

const QUESTIONS = [
   {
      "title":"Profession",
      "description":"What is your current profession?",
      "value":"",
   },
   {
      "title":"Institution",
      "description":"What is your institutional affiliation?",
      "value":"",
   },
]

export default {
   data(){
      return {
         questions: QUESTIONS
      }
   },
   methods: {
      to_router(){
         // Post metadata to API
         this.$router.push("/")
      }
   },
   components: {Card,Question}
}
</script>
