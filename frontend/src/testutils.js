
function Api(endpoints){
   this.calls = []

   this.typeGetterFactory = (type)=>{
      return ()=>{
         return this.calls.filter((c)=>{
            return c.type == type 
         })
      }
   }

   this.mockResponseFactory = (type) => {
      return async function(path, ...args){
         
         this.calls.push({
            path: path,
            type: type,
            args: args,
            response: endpoints[path]
         })

         return Promise.resolve({data: endpoints[path]})
      }
   }

   this.gget = this.mockResponseFactory("get")
   this.get_abs = this.gget
   this.gets = this.typeGetterFactory("get")

   this.gpost = this.mockResponseFactory("post")
   this.post_abs = this.gpost
   this.posts = this.typeGetterFactory("post")

   this.put = this.mockResponseFactory("put")
   this.put_abs = this.put
   this.puts = this.typeGetterFactory("put")
}


module.exports.Api = Api
