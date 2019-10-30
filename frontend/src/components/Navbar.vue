<template>
   <div>
      <div class = "row">
         <div class = "six columns">
            <h1 id = "title">{{ title }}</h1>
         </div>
         <div class = "six columns">
            <div id= "userinfo">
               Logged in as: {{ username }}
            </div>
         </div>
      </div>
   </div>
</template>

<script charset="utf-8">
   export default {
      name: "Toolbar",
      props: ["title"],
      methods: {
         y: function(){} 
      },
      computed: {
         username: function(){
            return this.$store.state.sessionInfo.username
         }
      }
   }
</script>

<style scoped lang="sass" type="text/css" media="screen">

h1
   margin-left: 15px
div#userinfo
   padding: 25px
   float: right
</style>

