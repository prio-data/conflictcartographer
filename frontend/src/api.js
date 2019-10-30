import Vue from "vue"
import VueResource from "vue-resource"

Vue.use(VueResource);

const Api = function(url, header){
   this.url = url

   this.header = header
   this._path = (...args) => [...args].join("/") + "/"

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

   this.post = function(obj,payload){
      let url = this._path(this.url,obj);
      Vue.http.post(url,payload,this.header)
         .then(
            function(response){
               if(typeof(payload) !== "list"){
                  console.log("adding body")
                  payload.pk = Number(response.body)
               }
            },
            function(error){
               console.log(error)
               console.log(payload)
            });
   }

   this.del = function(obj,pk){
      let url = this._path(this.url,obj,pk);
      Vue.http.delete(url,this.header).then(
            function(response){
               //
            },
            function(error){
               console.log(error)
            });
   }
};

export default Api
