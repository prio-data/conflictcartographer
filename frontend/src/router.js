
import VueRouter from "vue-router"
import Vue from "vue"

import LoadingRouter from "@/components/LoadingRouter"
import CountryAssign from "@/components/CountryAssign"
import Menu from "@/components/Menu"

Vue.use(VueRouter)

const CountrySelect = {template: `<div>Select some countries</div>`}
const DataEntry = {template: `Enter some data`}
const EditMeta = {template: `Edit your metadata`}

const routes = [
   {path: "/",component: LoadingRouter},
   {path: "/assign",component: CountryAssign},
   {path: "/ctry/:gwno",component: DataEntry},
   {path: "/profile",component: EditMeta},
   {path: "/menu",component: Menu},
]


export default new VueRouter({
   routes
})
