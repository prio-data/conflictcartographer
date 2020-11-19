
import Vuex from "vuex";
import Vue from "vue";

import mutations from './mutations'

Vue.use(Vuex);
Vue.config.devtools = true;

const store = new Vuex.Store({
   strict: false,

   // Initialization
   state: {
      color_low: "#2b83ba",
      color_high: "#d7191c",

      defaultIntensity: 0,
      defaultConfidence: 50,

      // API 
      // ================================================
      // API object and details about the API 
      api: {},
   },
   mutations,
});

export default store;
