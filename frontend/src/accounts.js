import "@/sass/accounts.sass"
import Vue from "vue"
import VueCookies from "vue-cookies"
import ConsentModal from "@/components/ConsentModal"

let regbase = document.querySelector("#regbase")
regbase.style.display = "block"

Vue.use(VueCookies)
window.$cookies.config("7d")

new Vue({
   el: "#consentmodal",
   render: h=>h(ConsentModal)
}).$mount()
