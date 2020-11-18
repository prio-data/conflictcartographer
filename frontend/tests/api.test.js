jest.mock("@/util/debounce")

import flushPromises from "flush-promises"

import {mount} from "@vue/test-utils"
import { Api } from "@/testutils"


import Calendar from "@/components/Calendar"
import LayerView from "@/components/LayerView"

test("Calendar API mocking POC", async ()=>{
   let api = new Api({
      calendar: {
         "year": 1999,
         "quarter": 1
      }
   })

   const wrapper = mount(Calendar,{
      mocks: {
         $store: {
            state: {
               api: api 
            }
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
      "shape": {}
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

      let payload = api.calls.pop().args[0]
      expect(payload.url).toBe(stupidUrl)
      expect(payload.values.confidence).toBe(50)
   }
})
