
import Vuex from "vuex";
import Vue from "vue";

import actions from './actions'
import mutations from './mutations'
import getters from './getters'

import STATUS from "../STATUS.js"

Vue.use(Vuex);

const store = new Vuex.Store({
   strict: false,

   // Initialization
   state: {
      
      // ================================================
      // ================================================
      // IMMUTABLE 
      // ================================================
      // ================================================
      
      color_low: "#2b83ba",
      color_high: "#d7191c",

      // API 
      // ================================================
      // API object and details about the API 
      api: {},
      apiURL: "/api/",

      // ================================================
      // ================================================
      // MUTABLE 
      // ================================================
      // ================================================
      
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

      // AJAX state
      // ================================================
      // Used to control what is shown when, when to show
      // a spinner, etc.
      menustatus: STATUS.INIT,
      nowloading: {},
   },
   actions,
   mutations,
   getters,
});

export default store;
