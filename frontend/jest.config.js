
//const {defaults} = require("jest-config")

module.exports = {
   verbose: true,
   roots: ["<rootDir>/tests/","<rootDir>/src/"],
   moduleFileExtensions: ["js","vue"],
   moduleNameMapper: {
      "^@/(.*)$": "<rootDir>/src/$1"
   },
   transform: {
      "^.+\\.js$": "babel-jest",
      "^.+\\.vue$": "vue-jest",
   }
}
