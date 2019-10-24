import Vue from 'vue'
import App from './App.vue'
import "leaflet/dist/leaflet.css"
import "leaflet-draw/dist/leaflet.draw.css"
import "./skeleton/skeleton.css"
import "./skeleton/normalize.css"
import "./sass/style.sass"

Vue.config.productionTip = false

new Vue({
  delimiters: ["[[","]]"],
  render: h => h(App),
}).$mount('#app')

