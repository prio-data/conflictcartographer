
import VueRouter from "vue-router"
import Vue from "vue"

import LoadingRouter from "@/components/LoadingRouter"
import App from "@/App"

Vue.use(VueRouter)

const CountrySelect = {template: `<div>Select some countries</div>`}
const DataEntry = {template: `Enter some data`}
const EditMeta = {template: `Edit your metadata`}

const routes = [
   {path: "/",component: LoadingRouter},
   {path: "/assign",component: CountrySelect},
   {path: "/ctry/:gwno",component: DataEntry},
   {path: "/meta",component: EditMeta},
   {path: "/menu",component: App},
]


export default new VueRouter({
   routes
})
