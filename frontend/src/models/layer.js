
import * as R from "ramda"

const hash = function(string){
   const red = (x,y) => Math.imul(31,x) + y.charCodeAt(0) | 0
   const hashfun = R.reduce(red, 1)
   return(hashfun(string.split("")))
}

export default function Layer(json,intensity,confidence){
   this.pk = 0 
   this.model = "cartographer.drawnshape"
   this.fields = {
      geometry: json,
      intensity: intensity,
      confidence: confidence
   }
   this.hash = hash(JSON.stringify(json))
}
