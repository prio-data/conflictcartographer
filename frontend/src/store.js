import Vue from "vue"
import Vuex from "vuex"
import Api from "./api.js"

Vue.use(Vuex);

// Move this out somewhere?=
const defaultStyle = {
   weight: 1
}

const focusedStyle = {
   weight: 3
}

const state = {

   // Deprecated **************************
   djangodata: "", 
   // Deprecated **************************

   api: {},

   // Username (etc?) retrieved from django sesh
   sessionInfo: {},
   apiURL: "/api/",
   
   // The user chooses a location to work on. 
   // drawn shapes are registered on a location. 
   locations: [],

   // Retrieved from the current location, used to
   // focus the leaflet map.
   zoomlvl: 6,
   mapx: 60,
   mapy: 12,

   // Current layers, either drawn or retrieved
   // from server. Is pushed and wiped when switching
   // location.
   layers: [],

   // UI stuff
   
   // Used to highlight a shape when mousing over its
   // control panel.
   infocus: null,

   // Used to figure out which layer to highlight
   vizId: 0,

};

const actions = {
   createLayer(context,created){
      context.commit("createLayer",created)
      context.commit("incrementVizId")
   },
   initializeLayers(context,filter){
      context.commit("initializeLayers",filter)
      state.vizId = state.layers.length + 1
   }
}

const mutations = {
   incrementVizId(state){
      state.vizId = state.vizId + 1;
   },


   // API requests ========================

   initApi(state,api){
      state.api = new Api(api.url,api.header);
   },
  
   // Populate list of "codeable" locations from the API
   initializeLocations(state){
      let populate = (countries) => state.countries = countries
      state.api.get("countries",populate,{})
   },

   // Leaflet layer handling ==============
   initializeLayers(state,filter){
      let populate = function(layers){
         layers.forEach(function(layer,index){
            layer.vizId = index
         })
         state.layers = layers
         state.vizId = layers.length + 1
      }
      state.api.get("shapes",populate,filter)
   },

   updateLayer(state,updated){
      state.api.del("shapes",updated.pk)
      state.api.post("shapes",updated)
   },
   
   createLayer(state,created){
      created.vizId = state.vizId
      state.layers.push(created)
      state.api.post("shapes",created)
   },

   deleteLayer(state,deleted){
      let i = state.layers.findIndex(layer => layer === deleted);
      let id = deleted.pk
      state.layers.splice(i,1) 
      state.api.del("shapes",id)
   },
   
   // Passed data from sesh, passed from django
   // used to show username (etc. ?)
   updateSessionInfo(state,data){
      state.sessionInfo = {...data, ...state.sessionInfo}  
   },


   // UI stuff ============================
   
   // Focus / unfocus when mousing over  
   focusOn(state,focused){
      state.infocus = focused.vizId;
   },

   unfocus(state){
      state.infocus = -1;
   },
};

const store = new Vuex.Store({
   strict: false,
   state,
   mutations,
   actions,
})

export default store;
