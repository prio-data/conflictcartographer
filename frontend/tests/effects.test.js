import { mount } from "@vue/test-utils"
import LayerView from "@/components/LayerView"
import flushPromises from "flush-promises"

test("Layer view nagging @ default values", async () =>{
   let c = mount(LayerView,{
      propsData:  {
         layer: {
            shape: {},
            values: {
               intensity: 0,
               confidence: 50,
            },
            url: "http://foo.bar"
         }
      }
   })

   await flushPromises()
   expect(c.findAll(".noticeme").wrappers).toHaveLength(1)

   c = mount(LayerView,{
      propsData:  {
         layer: {
            shape: {},
            values: {
               intensity: 3,
               confidence: 25,
            },
            url: "http://foo.bar"
         }
      }
   })

   await flushPromises()
   expect(c.findAll(".noticeme").wrappers).toHaveLength(0)
})
