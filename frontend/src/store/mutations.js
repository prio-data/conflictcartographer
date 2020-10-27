
import debounce from "@/util/debounce"
import Api from "@/api"

const mutations = {
   
   // INITIALIZATION  
   // ================================================
   // Sets stuff before session 

   initApi(state,api){
      state.api = new Api(api.url,api.header);
   },
   
   // Get layers
   // ======================
   initializeLayers(state){
      let filter = {
         project: state.currentProject.pk
      }
      let populate = function(layers){
         layers.forEach(function(layer,index){
            layer.vizId = index
         })
         state.layers = layers
         state.vizId = layers.length + 1
      }
      state.api.get("shapes",populate,filter)
   },
   
   // Merging setter
   // ======================
   setSessionInfo(state,data){
      state.sessionInfo = {...data, ...state.sessionInfo}  
   },

   // PROJECTS
   // ================================================
   // Set / unset project details 

   // Sets current project number 
   setCurrentProject(state,project){
      state.currentProject = project
   },

   // Set project details (e.g country shape, etc.)
   setProjectDetails(state,project){
      const setDetails = function(details){
         state.projectDetails = details
      }
      state.api.getAbs(project.country, setDetails, {})
   },

   // Sets project to null (returns user to menu)
   unsetProject(state){
      state.currentProject = null
      state.projectDetails = null
   },
  
   // LAYERS
   // ================================================
   // Mutations for handling leaflet layers 

   createLayer(state,created){

      // Defaults
      created.intensity = state.defaultIntensity;
      created.confidence = state.defaultIntensity;
      
      // Populate with information from state
      created.author = `${window.location}api/users/${state.sessionInfo.uk}/`
      created.project = state.currentProject.url
      created.vizId = state.vizId

      state.layers.push(created)
      state.api.post("shapes",created)
   },

   updateLayer: debounce(function(state,updated){
      //state.api.del("shapes",updated.pk)
      state.api.putAbs(updated.url,updated)
   },400),

   deleteLayer(state,deleted){
      let i = state.layers.findIndex(layer => layer === deleted);
      state.layers.splice(i,1) 
      state.api.delAbs(deleted.url)
   },

   incrementVizId(state){
      state.vizId = state.vizId + 1;
   },

   // UI stuff 
   // ================================================
   // Focus / unfocus when mousing over  
   
   focusOn(state,focused){
      state.infocus = focused.vizId;
   },

   unfocus(state){
      state.infocus = -1;
   },
};

export default mutations;
