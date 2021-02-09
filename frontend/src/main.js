import Vue from 'vue'
/*
import VueCookies from "vue-cookies"
import VueResource from "vue-resource"
import vueDebounce from "vue-debounce"
*/

import "leaflet/dist/leaflet.css"
import "leaflet-draw/dist/leaflet.draw.css"

//import App from './App.vue'
import store from "./store/store.js"
import "./sass/style.sass"
import Router from "@/router"
import VueCookies from "vue-cookies"

// Leaflet fixing
import {Icon} from "leaflet"
delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png")
});

Vue.use(VueCookies)

// API setup
//let csrf_token = /(?<=csrftoken\=)[^;]+/.exec(document.cookie)
let csrf_token = Vue.cookies.get("csrftoken")
if(!csrf_token !== null){
   store.commit("initApi",csrf_token[0])
} else {
   console.log("No CSRF token found...")
}

let app = document.querySelector("#app")
let rv = document.createElement("router-view")
app.appendChild(rv)

new Vue({
   router:Router,
   store:store,
}).$mount('#app')
