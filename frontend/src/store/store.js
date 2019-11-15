
import Vuex from "vuex";
import Vue from "vue";

import actions from './actions'
import mutations from './mutations'
import getters from './getters'

import STATUS from "@/STATUS.js"

Vue.use(Vuex);

const store = new Vuex.Store({
   strict: false,

   // Initialization
   state: {

      // API 
      // ================================================
      // API object and details about the API 
      api: {},
      apiURL: "/api/",
      menustatus: STATUS.INIT,

      // SESSION
      // ================================================
      // Display personalized info?
      sessionInfo: {},
      profile: {},

      // PROJECTS
      // ================================================
      // List of projects (available to user) and 
      // details about selected project.
      projects: [],
      currentProject: null,
      projectDetails: null,

      // LAYERS
      // ================================================
      // Current set of layers, blit onto leaflet map 
      layers: [],

      // Default scale values
      defaultIntensity: 0,
      defaultConfidence: 0,

      // UI Stuff
      // ================================================
      // Colors, currently focused, "vizId", etc. 
      infocus: null,

      vizId: 0,

      color_low: "#50bfca",
      color_high: "#ff9524",
   },

   actions,
   mutations,
   getters,
});

export default store;
