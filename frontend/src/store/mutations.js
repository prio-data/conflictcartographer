
import debounce from "../util/debounce"
import Api from "../api"

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
      state.api.gget("shapes",{params:{country:state.currentProject.gwno}})
         .then((r)=>{
            let layers = r.data.map(function(layer,index){
               layer.intensity = layer.values.intensity
               layer.confidence = layer.values.confidence
               layer.vizId = index
               return layer
            })
            state.layers = layers
            state.vizId = layers.length + 1
         })
         .catch((e)=>{
            console.log(e)
         })
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
      state.api.getAbs(project.url, setDetails, {})
   },

   // Sets project to null (returns user to menu)
   unsetProject(state){
      state.currentProject = null
      state.projectDetails = null
   },

   // PROJECT INFO
   // ================================================
   // Setting information text about current active project.

   setProjectInfo(state,projectInfo){
      state.projectTitle = projectInfo.title
      state.projectDescription = projectInfo.description
      state.projectLongDescription = projectInfo.long_description
   },
  
   // LAYERS
   // ================================================
   // Mutations for handling leaflet layers 

   createLayer(state,created){

      // Defaults
      created.intensity = state.defaultIntensity;
      created.confidence = state.defaultConfidence;
      
      // Populate with information from state
      created.author = `${window.location}api/users/${state.sessionInfo.uk}/`
      created.country = state.currentProject.url
      created.vizId = state.vizId

      created.values = {
         intensity: created.intensity,
         confidence: created.confidence
      }
      state.layers.push(created)
      state.api.post("shapes",created)
   },

   updateLayer: debounce(function(state,updated){
      updated.values = {
         intensity: updated.intensity,
         confidence: updated.confidence
      }
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
