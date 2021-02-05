
import VueRouter from "vue-router"
import Vue from "vue"

import LoadingRouter from "@/components/LoadingRouter"
import CountryAssign from "@/components/CountryAssign"
import Menu from "@/components/Menu"
import MapEditor from "@/components/MapEditor"
import ProgressMenu from "@/components/ProgressMenu"

Vue.use(VueRouter)

const EditMeta = {template: `Edit your metadata`}

const routes = [
   {path: "/",component: LoadingRouter},
   {path: "/assign",component: CountryAssign},
   {path: "/ctry/:gwno",component: MapEditor},
   {path: "/profile",component: EditMeta},
   {path: "/menu",component: Menu},
   {path: "/progress",component: ProgressMenu},
]


export default new VueRouter({
   routes
})
