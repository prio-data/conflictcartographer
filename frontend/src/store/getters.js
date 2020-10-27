
const getters = {
   // Current project
   // ================================================
   // API object and details about the API 
   projectShape(state){
      if(state.projectDetails){
         return state.projectDetails.shape;
      } else {
         return null;
      }
   },
}

export default getters;
