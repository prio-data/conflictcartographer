const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  
   publicPath: "/frontend/dist/",
   outputDir: './dist/',

   lintOnSave: "warning",
   filenameHashing: false,

   chainWebpack: config => {
      config.optimization
         .splitChunks(false)

      // ##########################
      // Custom CSS for other pages
      config.entry("accounts")
         .add("./src/css/accounts.css")
         .end()

      config
         .plugin('BundleTracker')
         .use(BundleTracker, [{filename: './webpack-stats.json'}])

      config.devServer
         .public('http://0.0.0.0:1337')
         .host('0.0.0.0')
         .port(1337)
         .hotOnly(true)
         .watchOptions({poll: 1000})
         .https(false)
         .headers({"Access-Control-Allow-Origin": ["\*"]})

      config.plugin("html").delete()
      config.plugin("preload").delete()
      config.plugin("prefetch").delete()
      }

   };
