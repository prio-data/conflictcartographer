import Vue from "vue"
import Vuex from "vuex"

Vue.use(Vuex);

const defaultStyle = {
   weight: 1
}

const focusedStyle = {
   weight: 3
}

const state = {

   djangodata: "", 

   layers: [],
   infocus: null,

   hello: "world",
   debugNotify: "",
   count: 1,
};

const mutations = {
   reverseGreeting(state){
      state.hello = state.hello.split("").reverse().join("");
   },
   notifySuccess(state){
      state.debugNotify = "It got pushed!";
   },
   notifyFailure(state,err){
      state.debugNotify = err; 
   },
   increment(state){
      state.count ++
   },
   initDjango(state,data){
      state.djangodata = data;
   },

   pushLayer(state,pushed){
      pushed["style"] = defaultStyle
      state.layers.push(pushed)
   },

   updateLayer(state,updated){
      let i = state.layers.findIndex(layer => layer === updated);
      state.layers[i] = updated
   },

   deleteLayer(state,deleted){
      let i = state.layers.findIndex(layer => layer === deleted);
      state.layers.splice(i,1) 
   },

   focusOn(state,focused){
      let focusedLayer = state.layers.findIndex(layer => layer == focused)
      state.layers[focusedLayer]["style"] = focusedStyle 
      state.infocus = focused;
   },

   unfocus(state){
      let focused = state.infocus
      let focusedLayer = state.layers.findIndex(layer => layer === focused)
      if(typeof state.layers[focusedLayer] !== "undefined"){
         state.layers[focusedLayer]["style"] = defaultStyle 
         state.infocus = null;
      }
   }

};

const store = new Vuex.Store({
   strict: false,
   state,
   mutations
})

export default store;
