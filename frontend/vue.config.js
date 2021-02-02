const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  
   publicPath: "/static/",
   outputDir: './dist/',

   lintOnSave: "warning",
   filenameHashing: false,

   css: {
      extract: false,
   },

   devServer: {
      public: "http://0.0.0.0:1337",
      host: "0.0.0.0",
      port: 1337,
      watchOptions: {
         poll : 1000
      },
      https: false,
      headers: {
         "Access-Control-Allow-Origin": ["\*"]
      }
   },

   configureWebpack: {
      optimization:{
         splitChunks: false
      }
   },
   chainWebpack: config => {
      config.entry("accounts")
         .add("./src/accounts.js")
         .end()
   },
   runtimeCompiler: true
   };
