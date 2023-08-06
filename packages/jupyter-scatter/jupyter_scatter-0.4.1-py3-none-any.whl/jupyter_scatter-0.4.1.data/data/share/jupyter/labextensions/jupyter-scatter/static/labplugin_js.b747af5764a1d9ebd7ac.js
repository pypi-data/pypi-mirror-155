(self["webpackChunkjupyter_scatter"] = self["webpackChunkjupyter_scatter"] || []).push([["labplugin_js"],{

/***/ "./index.js":
/*!******************!*\
  !*** ./index.js ***!
  \******************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

// Export widget models and views, and the npm package version number.
module.exports = __webpack_require__(/*! ./src/index.js */ "./src/index.js");
module.exports.version = __webpack_require__(/*! ./package.json */ "./package.json").version;


/***/ }),

/***/ "./labplugin.js":
/*!**********************!*\
  !*** ./labplugin.js ***!
  \**********************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

const plugin = __webpack_require__(/*! ./index */ "./index.js");
const base = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const name = __webpack_require__(/*! ./package.json */ "./package.json").name;

module.exports = {
  id: 'jupyter.extensions.' + name,
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
    widgets.registerWidget({
      name: name,
      version: plugin.version,
      exports: plugin
    });
  },
  autoStart: true
};


/***/ })

}]);
//# sourceMappingURL=labplugin_js.b747af5764a1d9ebd7ac.js.map