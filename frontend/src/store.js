import Vue from "vue"
import Vuex from "vuex"

Vue.use(Vuex);

const defaultStyle = {
   color: "red"
}

const focusedStyle = {
   color: "blue"
}

const state = {

   djangodata: "", 

   layers: [],
   infocus: null,

   hello: "world",
   debugNotify: "",
   count: 1,

   randomList: [
      {  
         id: "1",
         content: "Hello"
      },
      {  
         id: "2",
         content: "World"
      },
      {  
         id: "3",
         content: "Howdy"
      },
   ]
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

   deleteRandomItem(state,item){
      let i = state.randomList.findIndex(layer => layer.id == item.id);
      state.randomList.splice(i,1) 
   },

   pushLayer(state,pushed){
      pushed["style"] = defaultStyle
      state.layers.push(pushed)
   },

   deleteLayer(state,deleted){
      let i = state.layers.findIndex(layer => layer.id == deleted.id);
      state.layers.splice(i,1) 
   },

   focusOn(state,focused){
      let focusedLayer = state.layers.findIndex(layer => layer.id === focused.id)
      state.layers[focusedLayer]["style"] = focusedStyle 
      state.infocus = focused.id;
   },

   unfocus(state){
      let focused = {id: state.infocus}
      let focusedLayer = state.layers.findIndex(layer => layer.id === focused.id)
      state.layers[focusedLayer]["style"] = defaultStyle 
      state.infocus = null;
   }

};

const store = new Vuex.Store({
   strict: true,
   state,
   mutations
})

export default store;
