jest.mock("@/util/debounce")

import flushPromises from "flush-promises"

import {mount,shallowMount} from "@vue/test-utils"
import { Api } from "@/testutils"


import Calendar from "@/components/Calendar"
import LayerView from "@/components/LayerView"
import MapEditor from "@/components/MapEditor"

test("Calendar API mocking POC", async ()=>{
   let api = new Api({
      get:{
         calendar: {
            "year": 1999,
            "quarter": 1
         }
      }
   })

   const wrapper = mount(Calendar,{
      mocks: {
         $store: {
            state: {
               api: api 
            },
         }
      }
   })

   await flushPromises()

   let descrip = wrapper.get(".year").text()
   expect(descrip).toMatch(/1999/)
   expect(descrip).toMatch(/Q2/)

   descrip = wrapper.get(".months").text()
   let months = [/Apr/,/May/,/Jun/]
   months.forEach((m)=>{
      expect(descrip).toMatch(m)
   })

   let gets = api.gets()
   expect(gets).toHaveLength(1)
   expect(gets[0].path).toBe("calendar")
})

test("Layer view update posting", async ()=>{
   let stupidUrl = "http://foo.bar.baz/1/"

   let api = new Api({
      get: {
         "shape": {}
      },
      put: {
         "http://foo.bar.baz/1/": ""
      }
   })

   const wrapper = mount(LayerView,{
      propsData: {
         layer: {
            shape: {},
            values: {
               intensity: 0,
               confidence: 50
            },
            url: stupidUrl, 
         }
      },
      mocks: {
         $store: {
            state: {
               api: api 
            }
         }
      }
   })

   let wrappers = wrapper.findAll("input").wrappers
   while(wrappers.length > 0){
      let input = wrappers.pop()
      input.setChecked()

      await flushPromises()
      expect(api.puts()).toHaveLength(1)

      let payload = api.calls.pop().args.data
      expect(payload.url).toBe(stupidUrl)
      expect(payload.values.confidence).toBe(50)
   }
})

test("Test api post on layer create", async ()=>{
   let api = new Api({
      get: {
         "http://get.my.shape/1/":{
            shape: {
               type: "MultiPolygon",
               coordinates: [[[[-110.33,24.40],[-110.31,24.43],[-110.29,24.48],[-110.37,24.58],[-110.40,24.56],[-110.33,24.40]]]]
            },
            url: "http://get.my.shape/1/"
            },
         "shapes": [],
         "shapes/?country=1":{data:[]}
      },
      post: {
         "shapes": {url: "http://posted.shape/1/"}
      }
   })

   let c = shallowMount(MapEditor,{
      propsData: {
         project: {
            url: "http://get.my.shape/1/",
            gwno: 10,
            name: "Somewhere"
         },
      },
      mocks: {
         $store: {
            state: {
               api: api,
               defaultConfidence: 50,
               defaultIntensity: 0,
               color_low: "#2b83ba",
               color_high: "#d7191c",
            },
         }
      },
   })
   await flushPromises()

   let lmap = c.get("#map")
   let f = {"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-80.396942,21.94384],[-80.451892,20.849762],[-81.891572,21.310885],[-81.781673,22.167767],[-80.396942,21.94384]]]}}
   lmap.vm.$emit("created",f)

   await flushPromises()
   expect(c.vm.layers).toHaveLength(1)
   expect(api.posts()).toHaveLength(1)

   let payload = api.posts()[0].args.data
   expect(payload).toMatchObject({
      country: "http://get.my.shape/1/",
      shape: f,
      values: {
         intensity: 0,
         confidence: 50
      },
      url: "http://posted.shape/1/"
   })
})
