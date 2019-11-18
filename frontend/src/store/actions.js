const actions = {
  
   // INITIALIZATION 
   // ================================================
   // Creates a layer, giving it default values and pushing
   // it to the API / Vuex state.
   
   initializeLayers(context){
      context.commit("initializeLayers")
   },

   //async initializeProjectMenu({state, commit}){

      //let getProjects = function(){
         //return Vue.http.get(`${state.apiURL}projects`)
            //.then(function(response){return response.body})
            //.catch(function(){
               //return []
            //})
      //}
//
      //let getProfile = function(){
         //return Vue.http.get(`${state.apiURL}profile/${state.sessionInfo.uk}/`)
            //.then(function(response){return response.body})
            //.catch(function(){
               //return {name:"NONAME",projects:[]}
            //})
      //}
//
      //commit("initializeProfile", await getProfile())
      //commit("initializeProjects", await getProjects())
   //},

   //async awaitProjectMenu({dispatch,commit}){
      //commit("projectMenuWaiting")
      //await dispatch("initializeProjectMenu")
      //commit("projectMenuLoaded")
   //},

   // SESSION STATE
   // ================================================
   // Sets project number AND requests project details
   chooseProject(context,project){
      context.commit("setCurrentProject",project)
      context.commit("setProjectDetails",project)

   },

   backToMenu({commit, dispatch}){
      //await dispatch("awaitProjectMenu")
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
