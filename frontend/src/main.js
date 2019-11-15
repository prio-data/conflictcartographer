import Vue from 'vue'
import VueCookies from "vue-cookies"
import VueResource from "vue-resource"
import vueDebounce from "vue-debounce"

import "leaflet/dist/leaflet.css"
import "leaflet-draw/dist/leaflet.draw.css"

import App from './App.vue'
import store from "./store/store.js"

import "./skeleton/skeleton.css"
import "./skeleton/normalize.css"
import "./sass/style.sass"

import {Icon} from "leaflet"

delete Icon.Default.prototype._getIconUrl;

Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png")
});

Vue.config.productionTip = false
Vue.use(VueResource)
Vue.use(VueCookies)
Vue.use(vueDebounce)

new Vue({
   el: "#app",
   store,
   delimiters: ["[[","]]"],
   render: h => h(App),
}).$mount('#app')

