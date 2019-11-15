import Vue from "vue"

const actions = {
  
   // INITIALIZATION 
   // ================================================
   // Creates a layer, giving it default values and pushing
   // it to the API / Vuex state.
   
   initializeLayers(context,filter){
      context.commit("initializeLayers")
   },

   async initializeProjectMenu({state, dispatch, commit}){

      let getProjects = function(){
         return Vue.http.get(
            `${state.apiURL}projects`
         )
      }

      let getProfile = function(){
         return Vue.http.get(
            `${state.apiURL}profile/${state.sessionInfo.uk}/`
         )
      }

      let prof = await getProfile()
      commit("initializeProfile", await getProfile())
      commit("initializeProjects", await getProjects())
   },

   async awaitProjectMenu({dispatch,commit}){
      commit("projectMenuWaiting")
      await dispatch("initializeProjectMenu")
      commit("projectMenuLoaded")
   },

   // SESSION STATE
   // ================================================
   // Sets project number AND requests project details
   chooseProject(context,project){
      context.commit("setCurrentProject",project)
      context.commit("setProjectDetails",project)

   },

   async backToMenu({commit, dispatch}){
      await dispatch("awaitProjectMenu")
      commit("unsetProject")
   },
   
   // MANIPULATION
   // ================================================
   // Creates a layer, giving it default values and pushing
   // it to the API / Vuex state.
   
   createLayer(context,shape){
      let created = {shape: shape}

      // Pushes to state and API
      context.commit("createLayer",created)
      context.commit("incrementVizId")
   },
}

export default actions;
