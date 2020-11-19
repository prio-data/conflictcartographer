import Api from "../api"

const mutations = {
   initApi(state,token){
      state.api = new Api(token);
   },
};

export default mutations;
