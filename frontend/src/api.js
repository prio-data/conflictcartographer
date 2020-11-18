import Vue from "vue"
import VueResource from "vue-resource"
import Axios from "axios"

Vue.use(VueResource);

const Api = function(url, header){
   this.url = url

   this.header = header
   this._path = (...args) => [...args].join("/") + "/"
   this.geturl = (path) => this._path(this.url,path)

   this.get = function(obj,callback,parameters){
      let url = this._path(this.url,obj);
      Vue.http.get(url,{params: {format: "json", ...parameters}},this.header)
         .then(
            function(response){
               callback(response.body);
            },
            function(error){
               console.log(error)
            });
   }

   this.gget = function(path,parameters){
      return Axios.get(this.geturl(path),parameters)
   }

   this.base_gpost = function(url,payload,parameters){
      return Axios.post(
         url,
         JSON.stringify(payload),
         {...parameters, ...this.header}
      )
   }
   this.agpost = this.gpost
   this.gpost = function(path,...args){
      return this.base_gpost(this.geturl(path),...args)
   }

   this.base_put = function(url,payload,parameters){
      return Axios.put(
         url,payload,{...parameters, ...this.header}
      )
   }
   this.put_abs = this.base_put
   this.put = function(path,...args){
      return this.base_put(this.geturl(path),...args)
   }

   this.base_del= function(url,parameters){
      return Axios.delete(
         url,{...parameters, ...this.header}
      )
   }
   this.del_abs = this.base_del
   this.del = function(path,...args){
      return this.base_del(this.geturl(path),...args)
   }

   this.getAbs = function(url, callback, parameters){
      Vue.http.get(url,{params: {format: "json", ...parameters}},this.header)
         .then(
            function(response){
               callback(response.body);
            },
            function(error){
               console.log(error)
            });
   }

   this.post = function(obj,payload){
      let url = this._path(this.url,obj);
      Vue.http.post(url,payload,this.header)
         .then(
            function(response){
               if(typeof(payload) !== "list"){
                  payload.url = response.body
               }
            },
            function(error){
               console.log(error)
               console.log(payload)
            });
   }

};

export default Api
