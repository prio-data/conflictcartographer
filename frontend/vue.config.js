const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  
   publicPath: "/static/",
   outputDir: './dist/',

   lintOnSave: "warning",
   filenameHashing: false,

   css: {
      extract: false,
   },

   chainWebpack: config => {
      config.optimization
         .splitChunks(false)

      // ##########################
      // Custom CSS for other pages
      config.entry("accounts")
         .add("./src/css/accounts.css")
         .end()

      config.plugin("html").delete()
      config.plugin("preload").delete()
      config.plugin("prefetch").delete()
      }

   };
