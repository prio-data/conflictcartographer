
import VueRouter from "vue-router"
import Vue from "vue"

import LoadingRouter from "@/components/LoadingRouter"
import CountryAssign from "@/components/CountryAssign"
import Menu from "@/components/Menu"
import MapEditor from "@/components/MapEditor"
import ProgressMenu from "@/components/ProgressMenu"
import MetaQuestionaire from "@/components/MetaQuestionaire"
import ProjectInfo from "@/components/ProjectInfo"

Vue.use(VueRouter)

const routes = [
   {path: "/",component: LoadingRouter},
   {path: "/assign",component: CountryAssign},
   {path: "/ctry/:gwno",component: MapEditor},
   {path: "/questionaire",component: MetaQuestionaire},
   {path: "/menu",component: Menu},
   {path: "/progress",component: ProgressMenu},
   {path: "/info",component: ProjectInfo},
]


export default new VueRouter({
   routes
})
