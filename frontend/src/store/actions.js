const actions = {
  
   // INITIALIZATION 
   // ================================================
   // Creates a layer, giving it default values and pushing
   // it to the API / Vuex state.
   
   initializeLayers(context){
      context.commit("initializeLayers")
   },

   // SESSION STATE
   // ================================================
   // Sets project number AND requests project details
   chooseProject(context,project){
      context.commit("setCurrentProject",project)
      context.commit("setProjectDetails",project)

   },

   backToMenu(context){
      context.commit("unsetProject")
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
