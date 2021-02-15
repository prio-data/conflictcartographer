//jest.mock("@/util/debounce")

import {mount} from "@vue/test-utils"
import flushPromises from "flush-promises"
import {Api} from "@/testutils"
import {mock_countries} from "@/mocking"

import LoadingRouter from "@/components/LoadingRouter"

function mockRouter(){
   this.path = undefined
   this.push = (path)=>{
      this.path = path
   }
}

let respres=[
   {
      responses:{
         get:{
            "profile/assigned":{
               countries:[]
            },
            "profile/unfulfilled":{
               countries:[]
            },
            "profile/exists":{
               profile: false 
            },
         },
      },
      result_path: "/assign"
   },
   {
      responses:{
         get:{
            "profile/assigned":{
               countries:[mock_countries(3)]
            },
            "profile/unfulfilled":{
               countries:[mock_countries(3)]
            },
            "profile/exists":{
               profile: false 
            },
         },
      },
      result_path: "/progress"
   },
   {
      responses:{
         get:{
            "profile/assigned":{
               countries:[mock_countries(3)]
            },
            "profile/unfulfilled":{
               countries:[]
            },
            "profile/exists":{
               profile: false 
            },
         },
      },
      result_path: "/questionaire"
   },
   {
      responses:{
         get:{
            "profile/assigned":{
               countries:[mock_countries(3)]
            },
            "profile/unfulfilled":{
               countries:[]
            },
            "profile/exists":{
               profile: true
            },
         },
      },
      result_path: "/status"
   },
]

test("Shows info",()=>{
   let mr = new mockRouter()
   mount(LoadingRouter,{
      mocks:{$cookies:{get(){return false}},$router:mr}
   })
   expect(mr.path).toMatch("/info")
})

respres.forEach((pair)=>{
   let {responses,result_path}=pair
   test(`Reaches ${result_path}`,async ()=>{
      let api = new Api(responses)
      let mr = new mockRouter()
      mount(LoadingRouter,{
         mocks:{
            $cookies:{get(){return true}},
            $api:api,
            $router: mr 
         }
      })
      await flushPromises()
      expect(mr.path).toMatch(new RegExp(result_path))
   })
})
