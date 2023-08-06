var _JUPYTERLAB;
/******/ (function() { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "webpack/container/entry/metanno":
/*!***********************!*\
  !*** container entry ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

var moduleMap = {
	"./index": function() {
		return Promise.all([__webpack_require__.e("vendors-node_modules_css-loader_dist_runtime_api_js-node_modules_style-loader_lib_addStyles_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("lib_containers_TableView_index_js-lib_containers_TextView_index_js-webpack_sharing_consume_de-5d1d96"), __webpack_require__.e("lib_index_js")]).then(function() { return function() { return (__webpack_require__(/*! ./lib/index.js */ "./lib/index.js")); }; });
	},
	"./extension": function() {
		return Promise.all([__webpack_require__.e("vendors-node_modules_css-loader_dist_runtime_api_js-node_modules_style-loader_lib_addStyles_js"), __webpack_require__.e("vendors-node_modules_regenerator-runtime_runtime_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("lib_containers_TableView_index_js-lib_containers_TextView_index_js-webpack_sharing_consume_de-5d1d96"), __webpack_require__.e("lib_jupyter_plugin_js")]).then(function() { return function() { return (__webpack_require__(/*! ./lib/jupyter/plugin */ "./lib/jupyter/plugin.js")); }; });
	}
};
var get = function(module, getScope) {
	__webpack_require__.R = getScope;
	getScope = (
		__webpack_require__.o(moduleMap, module)
			? moduleMap[module]()
			: Promise.resolve().then(function() {
				throw new Error('Module "' + module + '" does not exist in container.');
			})
	);
	__webpack_require__.R = undefined;
	return getScope;
};
var init = function(shareScope, initScope) {
	if (!__webpack_require__.S) return;
	var name = "default"
	var oldScope = __webpack_require__.S[name];
	if(oldScope && oldScope !== shareScope) throw new Error("Container initialization failed as it has already been initialized with a different share scope");
	__webpack_require__.S[name] = shareScope;
	return __webpack_require__.I(name, initScope);
};

// This exports getters to disallow modifications
__webpack_require__.d(exports, {
	get: function() { return get; },
	init: function() { return init; }
});

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			id: moduleId,
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = __webpack_modules__;
/******/ 	
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = __webpack_module_cache__;
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	!function() {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = function(module) {
/******/ 			var getter = module && module.__esModule ?
/******/ 				function() { return module['default']; } :
/******/ 				function() { return module; };
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	!function() {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = function(exports, definition) {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/ensure chunk */
/******/ 	!function() {
/******/ 		__webpack_require__.f = {};
/******/ 		// This file contains only the entry chunk.
/******/ 		// The chunk loading function for additional chunks
/******/ 		__webpack_require__.e = function(chunkId) {
/******/ 			return Promise.all(Object.keys(__webpack_require__.f).reduce(function(promises, key) {
/******/ 				__webpack_require__.f[key](chunkId, promises);
/******/ 				return promises;
/******/ 			}, []));
/******/ 		};
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/get javascript chunk filename */
/******/ 	!function() {
/******/ 		// This function allow to reference async chunks
/******/ 		__webpack_require__.u = function(chunkId) {
/******/ 			// return url for filenames based on template
/******/ 			return "" + chunkId + "." + {"vendors-node_modules_css-loader_dist_runtime_api_js-node_modules_style-loader_lib_addStyles_js":"f454588afcf19a21a965","webpack_sharing_consume_default_react":"10487e8e9f07b5a2d285","webpack_sharing_consume_default_react-dom":"748ac8656b791541fcaa","lib_containers_TableView_index_js-lib_containers_TextView_index_js-webpack_sharing_consume_de-5d1d96":"4a382cfb77e17b001562","lib_index_js":"a5421732c845341bcfd6","vendors-node_modules_regenerator-runtime_runtime_js":"a8f97b123007ddb518a1","lib_jupyter_plugin_js":"9a9d282bd8d8e026e920","node_modules_clsx_dist_clsx_m_js":"392079cc04db80d7a173","react-data-grid_node_modules_clsx_dist_clsx_m_js":"706bc437b11b2e67f5ed","vendors-node_modules_color_index_js":"9dc89c47dc6afbb6a556","vendors-node_modules_immer_dist_immer_esm_js":"56dbdb7b786a69b71c1b","vendors-node_modules_jupyterlab_toastify_lib_index_js":"e8fe9da17961e0824096","webpack_sharing_consume_default_prop-types_prop-types-_7bc8":"79ed28b27f9a2d81380f","vendors-node_modules_fortawesome_react-fontawesome_node_modules_prop-types_index_js":"0fac80b90b0cc2657495","vendors-node_modules_react-autosuggest_node_modules_prop-types_index_js":"a6413166927c7888ce8d","vendors-node_modules_react-autowhatever_node_modules_prop-types_index_js":"8f6158a4533370d267bb","vendors-node_modules_react-redux_node_modules_prop-types_index_js":"48112e6acb9bc5717b4a","vendors-node_modules_react-autosuggest_dist_index_js":"e94957b58c7d08866a63","webpack_sharing_consume_default_prop-types_prop-types-webpack_sharing_consume_default_prop-ty-9754ad":"410437661cc5180e9f34","react-data-grid_lib_bundle_js":"db84f0910fd39f85d544","vendors-node_modules_react-dnd-html5-backend_dist_esm_index_js":"df4c8004860319cf4151","vendors-node_modules_react-dnd_dist_esm_index_js":"65c8d5a056e24525cc9a","webpack_sharing_consume_default_redux_redux":"a0132f08c3f79b507d19","node_modules_react-fast-compare_index_js":"d865c4413f0193d598f0","vendors-node_modules_react-redux_es_index_js":"5589a32a4a7a811e2ee2","webpack_sharing_consume_default_prop-types_prop-types-_0f41":"daccdef461cd9279207e","vendors-node_modules_redux_es_redux_js":"0f409237e13fad7d68f6","vendors-node_modules_dnd-core_node_modules_redux_es_redux_js":"d41ba38a0de59807df55","node_modules_sourcemap-codec_dist_sourcemap-codec_es_js":"cde4c87ba31e30e626e9","vendors-node_modules_react-toastify_dist_react-toastify_esm_js":"0fb97bfc48e9a92c2616","webpack_sharing_consume_default_clsx_clsx":"f3623bc6b8be9ee8eacf"}[chunkId] + ".js";
/******/ 		};
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/global */
/******/ 	!function() {
/******/ 		__webpack_require__.g = (function() {
/******/ 			if (typeof globalThis === 'object') return globalThis;
/******/ 			try {
/******/ 				return this || new Function('return this')();
/******/ 			} catch (e) {
/******/ 				if (typeof window === 'object') return window;
/******/ 			}
/******/ 		})();
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	!function() {
/******/ 		__webpack_require__.o = function(obj, prop) { return Object.prototype.hasOwnProperty.call(obj, prop); }
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/load script */
/******/ 	!function() {
/******/ 		var inProgress = {};
/******/ 		var dataWebpackPrefix = "metanno:";
/******/ 		// loadScript function to load a script via script tag
/******/ 		__webpack_require__.l = function(url, done, key, chunkId) {
/******/ 			if(inProgress[url]) { inProgress[url].push(done); return; }
/******/ 			var script, needAttach;
/******/ 			if(key !== undefined) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				for(var i = 0; i < scripts.length; i++) {
/******/ 					var s = scripts[i];
/******/ 					if(s.getAttribute("src") == url || s.getAttribute("data-webpack") == dataWebpackPrefix + key) { script = s; break; }
/******/ 				}
/******/ 			}
/******/ 			if(!script) {
/******/ 				needAttach = true;
/******/ 				script = document.createElement('script');
/******/ 		
/******/ 				script.charset = 'utf-8';
/******/ 				script.timeout = 120;
/******/ 				if (__webpack_require__.nc) {
/******/ 					script.setAttribute("nonce", __webpack_require__.nc);
/******/ 				}
/******/ 				script.setAttribute("data-webpack", dataWebpackPrefix + key);
/******/ 				script.src = url;
/******/ 			}
/******/ 			inProgress[url] = [done];
/******/ 			var onScriptComplete = function(prev, event) {
/******/ 				// avoid mem leaks in IE.
/******/ 				script.onerror = script.onload = null;
/******/ 				clearTimeout(timeout);
/******/ 				var doneFns = inProgress[url];
/******/ 				delete inProgress[url];
/******/ 				script.parentNode && script.parentNode.removeChild(script);
/******/ 				doneFns && doneFns.forEach(function(fn) { return fn(event); });
/******/ 				if(prev) return prev(event);
/******/ 			}
/******/ 			;
/******/ 			var timeout = setTimeout(onScriptComplete.bind(null, undefined, { type: 'timeout', target: script }), 120000);
/******/ 			script.onerror = onScriptComplete.bind(null, script.onerror);
/******/ 			script.onload = onScriptComplete.bind(null, script.onload);
/******/ 			needAttach && document.head.appendChild(script);
/******/ 		};
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	!function() {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = function(exports) {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/sharing */
/******/ 	!function() {
/******/ 		__webpack_require__.S = {};
/******/ 		var initPromises = {};
/******/ 		var initTokens = {};
/******/ 		__webpack_require__.I = function(name, initScope) {
/******/ 			if(!initScope) initScope = [];
/******/ 			// handling circular init calls
/******/ 			var initToken = initTokens[name];
/******/ 			if(!initToken) initToken = initTokens[name] = {};
/******/ 			if(initScope.indexOf(initToken) >= 0) return;
/******/ 			initScope.push(initToken);
/******/ 			// only runs once
/******/ 			if(initPromises[name]) return initPromises[name];
/******/ 			// creates a new share scope if needed
/******/ 			if(!__webpack_require__.o(__webpack_require__.S, name)) __webpack_require__.S[name] = {};
/******/ 			// runs all init snippets from all modules reachable
/******/ 			var scope = __webpack_require__.S[name];
/******/ 			var warn = function(msg) { return typeof console !== "undefined" && console.warn && console.warn(msg); };
/******/ 			var uniqueName = "metanno";
/******/ 			var register = function(name, version, factory, eager) {
/******/ 				var versions = scope[name] = scope[name] || {};
/******/ 				var activeVersion = versions[version];
/******/ 				if(!activeVersion || (!activeVersion.loaded && (!eager != !activeVersion.eager ? eager : uniqueName > activeVersion.from))) versions[version] = { get: factory, from: uniqueName, eager: !!eager };
/******/ 			};
/******/ 			var initExternal = function(id) {
/******/ 				var handleError = function(err) { warn("Initialization of sharing external failed: " + err); };
/******/ 				try {
/******/ 					var module = __webpack_require__(id);
/******/ 					if(!module) return;
/******/ 					var initFn = function(module) { return module && module.init && module.init(__webpack_require__.S[name], initScope); }
/******/ 					if(module.then) return promises.push(module.then(initFn, handleError));
/******/ 					var initResult = initFn(module);
/******/ 					if(initResult && initResult.then) return promises.push(initResult['catch'](handleError));
/******/ 				} catch(err) { handleError(err); }
/******/ 			}
/******/ 			var promises = [];
/******/ 			switch(name) {
/******/ 				case "default": {
/******/ 					register("clsx", "1.1.1", function() { return __webpack_require__.e("node_modules_clsx_dist_clsx_m_js").then(function() { return function() { return __webpack_require__(/*! ./node_modules/clsx/dist/clsx.m.js */ "./node_modules/clsx/dist/clsx.m.js"); }; }); });
/******/ 					register("clsx", "1.1.1", function() { return __webpack_require__.e("react-data-grid_node_modules_clsx_dist_clsx_m_js").then(function() { return function() { return __webpack_require__(/*! ../react-data-grid/node_modules/clsx/dist/clsx.m.js */ "../react-data-grid/node_modules/clsx/dist/clsx.m.js"); }; }); });
/******/ 					register("color", "3.2.1", function() { return __webpack_require__.e("vendors-node_modules_color_index_js").then(function() { return function() { return __webpack_require__(/*! ./node_modules/color/index.js */ "./node_modules/color/index.js"); }; }); });
/******/ 					register("immer", "9.0.6", function() { return __webpack_require__.e("vendors-node_modules_immer_dist_immer_esm_js").then(function() { return function() { return __webpack_require__(/*! ./node_modules/immer/dist/immer.esm.js */ "./node_modules/immer/dist/immer.esm.js"); }; }); });
/******/ 					register("jupyterlab_toastify", "4.2.1", function() { return Promise.all([__webpack_require__.e("vendors-node_modules_css-loader_dist_runtime_api_js-node_modules_style-loader_lib_addStyles_js"), __webpack_require__.e("vendors-node_modules_jupyterlab_toastify_lib_index_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_prop-types_prop-types-_7bc8")]).then(function() { return function() { return __webpack_require__(/*! ./node_modules/jupyterlab_toastify/lib/index.js */ "./node_modules/jupyterlab_toastify/lib/index.js"); }; }); });
/******/ 					register("metanno", "0.0.8", function() { return Promise.all([__webpack_require__.e("vendors-node_modules_css-loader_dist_runtime_api_js-node_modules_style-loader_lib_addStyles_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("lib_containers_TableView_index_js-lib_containers_TextView_index_js-webpack_sharing_consume_de-5d1d96"), __webpack_require__.e("lib_index_js")]).then(function() { return function() { return __webpack_require__(/*! ./lib/index.js */ "./lib/index.js"); }; }); });
/******/ 					register("prop-types", "15.8.1", function() { return __webpack_require__.e("vendors-node_modules_fortawesome_react-fontawesome_node_modules_prop-types_index_js").then(function() { return function() { return __webpack_require__(/*! ./node_modules/@fortawesome/react-fontawesome/node_modules/prop-types/index.js */ "./node_modules/@fortawesome/react-fontawesome/node_modules/prop-types/index.js"); }; }); });
/******/ 					register("prop-types", "15.8.1", function() { return __webpack_require__.e("vendors-node_modules_react-autosuggest_node_modules_prop-types_index_js").then(function() { return function() { return __webpack_require__(/*! ./node_modules/react-autosuggest/node_modules/prop-types/index.js */ "./node_modules/react-autosuggest/node_modules/prop-types/index.js"); }; }); });
/******/ 					register("prop-types", "15.8.1", function() { return __webpack_require__.e("vendors-node_modules_react-autowhatever_node_modules_prop-types_index_js").then(function() { return function() { return __webpack_require__(/*! ./node_modules/react-autowhatever/node_modules/prop-types/index.js */ "./node_modules/react-autowhatever/node_modules/prop-types/index.js"); }; }); });
/******/ 					register("prop-types", "15.8.1", function() { return __webpack_require__.e("vendors-node_modules_react-redux_node_modules_prop-types_index_js").then(function() { return function() { return __webpack_require__(/*! ./node_modules/react-redux/node_modules/prop-types/index.js */ "./node_modules/react-redux/node_modules/prop-types/index.js"); }; }); });
/******/ 					register("react-autosuggest", "9.4.3", function() { return Promise.all([__webpack_require__.e("vendors-node_modules_react-autosuggest_dist_index_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_prop-types_prop-types-webpack_sharing_consume_default_prop-ty-9754ad")]).then(function() { return function() { return __webpack_require__(/*! ./node_modules/react-autosuggest/dist/index.js */ "./node_modules/react-autosuggest/dist/index.js"); }; }); });
/******/ 					register("react-data-grid", "7.0.0-beta.7", function() { return Promise.all([__webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("react-data-grid_lib_bundle_js")]).then(function() { return function() { return __webpack_require__(/*! ../react-data-grid/lib/bundle.js */ "../react-data-grid/lib/bundle.js"); }; }); });
/******/ 					register("react-dnd-html5-backend", "10.0.2", function() { return __webpack_require__.e("vendors-node_modules_react-dnd-html5-backend_dist_esm_index_js").then(function() { return function() { return __webpack_require__(/*! ./node_modules/react-dnd-html5-backend/dist/esm/index.js */ "./node_modules/react-dnd-html5-backend/dist/esm/index.js"); }; }); });
/******/ 					register("react-dnd", "10.0.2", function() { return Promise.all([__webpack_require__.e("vendors-node_modules_react-dnd_dist_esm_index_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_redux_redux")]).then(function() { return function() { return __webpack_require__(/*! ./node_modules/react-dnd/dist/esm/index.js */ "./node_modules/react-dnd/dist/esm/index.js"); }; }); });
/******/ 					register("react-fast-compare", "3.2.0", function() { return __webpack_require__.e("node_modules_react-fast-compare_index_js").then(function() { return function() { return __webpack_require__(/*! ./node_modules/react-fast-compare/index.js */ "./node_modules/react-fast-compare/index.js"); }; }); });
/******/ 					register("react-redux", "7.2.6", function() { return Promise.all([__webpack_require__.e("vendors-node_modules_react-redux_es_index_js"), __webpack_require__.e("webpack_sharing_consume_default_react"), __webpack_require__.e("webpack_sharing_consume_default_react-dom"), __webpack_require__.e("webpack_sharing_consume_default_prop-types_prop-types-_0f41")]).then(function() { return function() { return __webpack_require__(/*! ./node_modules/react-redux/es/index.js */ "./node_modules/react-redux/es/index.js"); }; }); });
/******/ 					register("redux", "4.1.2", function() { return __webpack_require__.e("vendors-node_modules_redux_es_redux_js").then(function() { return function() { return __webpack_require__(/*! ./node_modules/redux/es/redux.js */ "./node_modules/redux/es/redux.js"); }; }); });
/******/ 					register("redux", "4.2.0", function() { return __webpack_require__.e("vendors-node_modules_dnd-core_node_modules_redux_es_redux_js").then(function() { return function() { return __webpack_require__(/*! ./node_modules/dnd-core/node_modules/redux/es/redux.js */ "./node_modules/dnd-core/node_modules/redux/es/redux.js"); }; }); });
/******/ 					register("sourcemap-codec", "1.4.8", function() { return __webpack_require__.e("node_modules_sourcemap-codec_dist_sourcemap-codec_es_js").then(function() { return function() { return __webpack_require__(/*! ./node_modules/sourcemap-codec/dist/sourcemap-codec.es.js */ "./node_modules/sourcemap-codec/dist/sourcemap-codec.es.js"); }; }); });
/******/ 				}
/******/ 				break;
/******/ 			}
/******/ 			if(!promises.length) return initPromises[name] = 1;
/******/ 			return initPromises[name] = Promise.all(promises).then(function() { return initPromises[name] = 1; });
/******/ 		};
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/publicPath */
/******/ 	!function() {
/******/ 		var scriptUrl;
/******/ 		if (__webpack_require__.g.importScripts) scriptUrl = __webpack_require__.g.location + "";
/******/ 		var document = __webpack_require__.g.document;
/******/ 		if (!scriptUrl && document) {
/******/ 			if (document.currentScript)
/******/ 				scriptUrl = document.currentScript.src
/******/ 			if (!scriptUrl) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				if(scripts.length) scriptUrl = scripts[scripts.length - 1].src
/******/ 			}
/******/ 		}
/******/ 		// When supporting browsers where an automatic publicPath is not supported you must specify an output.publicPath manually via configuration
/******/ 		// or pass an empty string ("") and set the __webpack_public_path__ variable from your code to use your own logic.
/******/ 		if (!scriptUrl) throw new Error("Automatic publicPath is not supported in this browser");
/******/ 		scriptUrl = scriptUrl.replace(/#.*$/, "").replace(/\?.*$/, "").replace(/\/[^\/]+$/, "/");
/******/ 		__webpack_require__.p = scriptUrl;
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/consumes */
/******/ 	!function() {
/******/ 		var parseVersion = function(str) {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			var p=function(p){return p.split(".").map((function(p){return+p==p?+p:p}))},n=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(str),r=n[1]?p(n[1]):[];return n[2]&&(r.length++,r.push.apply(r,p(n[2]))),n[3]&&(r.push([]),r.push.apply(r,p(n[3]))),r;
/******/ 		}
/******/ 		var versionLt = function(a, b) {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			a=parseVersion(a),b=parseVersion(b);for(var r=0;;){if(r>=a.length)return r<b.length&&"u"!=(typeof b[r])[0];var e=a[r],n=(typeof e)[0];if(r>=b.length)return"u"==n;var t=b[r],f=(typeof t)[0];if(n!=f)return"o"==n&&"n"==f||("s"==f||"u"==n);if("o"!=n&&"u"!=n&&e!=t)return e<t;r++}
/******/ 		}
/******/ 		var rangeToString = function(range) {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			var r=range[0],n="";if(1===range.length)return"*";if(r+.5){n+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var e=1,a=1;a<range.length;a++){e--,n+="u"==(typeof(t=range[a]))[0]?"-":(e>0?".":"")+(e=2,t)}return n}var g=[];for(a=1;a<range.length;a++){var t=range[a];g.push(0===t?"not("+o()+")":1===t?"("+o()+" || "+o()+")":2===t?g.pop()+" "+g.pop():rangeToString(t))}return o();function o(){return g.pop().replace(/^\((.+)\)$/,"$1")}
/******/ 		}
/******/ 		var satisfy = function(range, version) {
/******/ 			// see webpack/lib/util/semver.js for original code
/******/ 			if(0 in range){version=parseVersion(version);var e=range[0],r=e<0;r&&(e=-e-1);for(var n=0,i=1,a=!0;;i++,n++){var f,s,g=i<range.length?(typeof range[i])[0]:"";if(n>=version.length||"o"==(s=(typeof(f=version[n]))[0]))return!a||("u"==g?i>e&&!r:""==g!=r);if("u"==s){if(!a||"u"!=g)return!1}else if(a)if(g==s)if(i<=e){if(f!=range[i])return!1}else{if(r?f>range[i]:f<range[i])return!1;f!=range[i]&&(a=!1)}else if("s"!=g&&"n"!=g){if(r||i<=e)return!1;a=!1,i--}else{if(i<=e||s<g!=r)return!1;a=!1}else"s"!=g&&"n"!=g&&(a=!1,i--)}}var t=[],o=t.pop.bind(t);for(n=1;n<range.length;n++){var u=range[n];t.push(1==u?o()|o():2==u?o()&o():u?satisfy(u,version):!o())}return!!o();
/******/ 		}
/******/ 		var ensureExistence = function(scopeName, key) {
/******/ 			var scope = __webpack_require__.S[scopeName];
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) throw new Error("Shared module " + key + " doesn't exist in shared scope " + scopeName);
/******/ 			return scope;
/******/ 		};
/******/ 		var findVersion = function(scope, key) {
/******/ 			var versions = scope[key];
/******/ 			var key = Object.keys(versions).reduce(function(a, b) {
/******/ 				return !a || versionLt(a, b) ? b : a;
/******/ 			}, 0);
/******/ 			return key && versions[key]
/******/ 		};
/******/ 		var findSingletonVersionKey = function(scope, key) {
/******/ 			var versions = scope[key];
/******/ 			return Object.keys(versions).reduce(function(a, b) {
/******/ 				return !a || (!versions[a].loaded && versionLt(a, b)) ? b : a;
/******/ 			}, 0);
/******/ 		};
/******/ 		var getInvalidSingletonVersionMessage = function(scope, key, version, requiredVersion) {
/******/ 			return "Unsatisfied version " + version + " from " + (version && scope[key][version].from) + " of shared singleton module " + key + " (required " + rangeToString(requiredVersion) + ")"
/******/ 		};
/******/ 		var getSingleton = function(scope, scopeName, key, requiredVersion) {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var getSingletonVersion = function(scope, scopeName, key, requiredVersion) {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			if (!satisfy(requiredVersion, version)) typeof console !== "undefined" && console.warn && console.warn(getInvalidSingletonVersionMessage(scope, key, version, requiredVersion));
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var getStrictSingletonVersion = function(scope, scopeName, key, requiredVersion) {
/******/ 			var version = findSingletonVersionKey(scope, key);
/******/ 			if (!satisfy(requiredVersion, version)) throw new Error(getInvalidSingletonVersionMessage(scope, key, version, requiredVersion));
/******/ 			return get(scope[key][version]);
/******/ 		};
/******/ 		var findValidVersion = function(scope, key, requiredVersion) {
/******/ 			var versions = scope[key];
/******/ 			var key = Object.keys(versions).reduce(function(a, b) {
/******/ 				if (!satisfy(requiredVersion, b)) return a;
/******/ 				return !a || versionLt(a, b) ? b : a;
/******/ 			}, 0);
/******/ 			return key && versions[key]
/******/ 		};
/******/ 		var getInvalidVersionMessage = function(scope, scopeName, key, requiredVersion) {
/******/ 			var versions = scope[key];
/******/ 			return "No satisfying version (" + rangeToString(requiredVersion) + ") of shared module " + key + " found in shared scope " + scopeName + ".\n" +
/******/ 				"Available versions: " + Object.keys(versions).map(function(key) {
/******/ 				return key + " from " + versions[key].from;
/******/ 			}).join(", ");
/******/ 		};
/******/ 		var getValidVersion = function(scope, scopeName, key, requiredVersion) {
/******/ 			var entry = findValidVersion(scope, key, requiredVersion);
/******/ 			if(entry) return get(entry);
/******/ 			throw new Error(getInvalidVersionMessage(scope, scopeName, key, requiredVersion));
/******/ 		};
/******/ 		var warnInvalidVersion = function(scope, scopeName, key, requiredVersion) {
/******/ 			typeof console !== "undefined" && console.warn && console.warn(getInvalidVersionMessage(scope, scopeName, key, requiredVersion));
/******/ 		};
/******/ 		var get = function(entry) {
/******/ 			entry.loaded = 1;
/******/ 			return entry.get()
/******/ 		};
/******/ 		var init = function(fn) { return function(scopeName, a, b, c) {
/******/ 			var promise = __webpack_require__.I(scopeName);
/******/ 			if (promise && promise.then) return promise.then(fn.bind(fn, scopeName, __webpack_require__.S[scopeName], a, b, c));
/******/ 			return fn(scopeName, __webpack_require__.S[scopeName], a, b, c);
/******/ 		}; };
/******/ 		
/******/ 		var load = /*#__PURE__*/ init(function(scopeName, scope, key) {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return get(findVersion(scope, key));
/******/ 		});
/******/ 		var loadFallback = /*#__PURE__*/ init(function(scopeName, scope, key, fallback) {
/******/ 			return scope && __webpack_require__.o(scope, key) ? get(findVersion(scope, key)) : fallback();
/******/ 		});
/******/ 		var loadVersionCheck = /*#__PURE__*/ init(function(scopeName, scope, key, version) {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return get(findValidVersion(scope, key, version) || warnInvalidVersion(scope, scopeName, key, version) || findVersion(scope, key));
/******/ 		});
/******/ 		var loadSingleton = /*#__PURE__*/ init(function(scopeName, scope, key) {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getSingleton(scope, scopeName, key);
/******/ 		});
/******/ 		var loadSingletonVersionCheck = /*#__PURE__*/ init(function(scopeName, scope, key, version) {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictVersionCheck = /*#__PURE__*/ init(function(scopeName, scope, key, version) {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getValidVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictSingletonVersionCheck = /*#__PURE__*/ init(function(scopeName, scope, key, version) {
/******/ 			ensureExistence(scopeName, key);
/******/ 			return getStrictSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadVersionCheckFallback = /*#__PURE__*/ init(function(scopeName, scope, key, version, fallback) {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return get(findValidVersion(scope, key, version) || warnInvalidVersion(scope, scopeName, key, version) || findVersion(scope, key));
/******/ 		});
/******/ 		var loadSingletonFallback = /*#__PURE__*/ init(function(scopeName, scope, key, fallback) {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getSingleton(scope, scopeName, key);
/******/ 		});
/******/ 		var loadSingletonVersionCheckFallback = /*#__PURE__*/ init(function(scopeName, scope, key, version, fallback) {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var loadStrictVersionCheckFallback = /*#__PURE__*/ init(function(scopeName, scope, key, version, fallback) {
/******/ 			var entry = scope && __webpack_require__.o(scope, key) && findValidVersion(scope, key, version);
/******/ 			return entry ? get(entry) : fallback();
/******/ 		});
/******/ 		var loadStrictSingletonVersionCheckFallback = /*#__PURE__*/ init(function(scopeName, scope, key, version, fallback) {
/******/ 			if(!scope || !__webpack_require__.o(scope, key)) return fallback();
/******/ 			return getStrictSingletonVersion(scope, scopeName, key, version);
/******/ 		});
/******/ 		var installedModules = {};
/******/ 		var moduleToHandlerMapping = {
/******/ 			"webpack/sharing/consume/default/react": function() { return loadSingletonVersionCheck("default", "react", [1,17,0,1]); },
/******/ 			"webpack/sharing/consume/default/react-dom": function() { return loadSingletonVersionCheck("default", "react-dom", [1,17,0,1]); },
/******/ 			"webpack/sharing/consume/default/react-redux/react-redux": function() { return loadStrictVersionCheckFallback("default", "react-redux", [4,7,2,6], function() { return Promise.all([__webpack_require__.e("vendors-node_modules_react-redux_es_index_js"), __webpack_require__.e("webpack_sharing_consume_default_prop-types_prop-types-_0f41")]).then(function() { return function() { return __webpack_require__(/*! react-redux */ "./node_modules/react-redux/es/index.js"); }; }); }); },
/******/ 			"webpack/sharing/consume/default/redux/redux?375d": function() { return loadStrictVersionCheckFallback("default", "redux", [4,4,1,2], function() { return __webpack_require__.e("vendors-node_modules_redux_es_redux_js").then(function() { return function() { return __webpack_require__(/*! redux */ "./node_modules/redux/es/redux.js"); }; }); }); },
/******/ 			"webpack/sharing/consume/default/immer/immer": function() { return loadStrictVersionCheckFallback("default", "immer", [4,9,0,6], function() { return __webpack_require__.e("vendors-node_modules_immer_dist_immer_esm_js").then(function() { return function() { return __webpack_require__(/*! immer */ "./node_modules/immer/dist/immer.esm.js"); }; }); }); },
/******/ 			"webpack/sharing/consume/default/react-fast-compare/react-fast-compare": function() { return loadStrictVersionCheckFallback("default", "react-fast-compare", [4,3,2,0], function() { return __webpack_require__.e("node_modules_react-fast-compare_index_js").then(function() { return function() { return __webpack_require__(/*! react-fast-compare */ "./node_modules/react-fast-compare/index.js"); }; }); }); },
/******/ 			"webpack/sharing/consume/default/color/color": function() { return loadStrictVersionCheckFallback("default", "color", [4,3,2,1], function() { return __webpack_require__.e("vendors-node_modules_color_index_js").then(function() { return function() { return __webpack_require__(/*! color */ "./node_modules/color/index.js"); }; }); }); },
/******/ 			"webpack/sharing/consume/default/react-dnd/react-dnd": function() { return loadStrictVersionCheckFallback("default", "react-dnd", [4,10,0,2], function() { return Promise.all([__webpack_require__.e("vendors-node_modules_react-dnd_dist_esm_index_js"), __webpack_require__.e("webpack_sharing_consume_default_redux_redux")]).then(function() { return function() { return __webpack_require__(/*! react-dnd */ "./node_modules/react-dnd/dist/esm/index.js"); }; }); }); },
/******/ 			"webpack/sharing/consume/default/react-dnd-html5-backend/react-dnd-html5-backend": function() { return loadStrictVersionCheckFallback("default", "react-dnd-html5-backend", [4,10,0,2], function() { return __webpack_require__.e("vendors-node_modules_react-dnd-html5-backend_dist_esm_index_js").then(function() { return function() { return __webpack_require__(/*! react-dnd-html5-backend */ "./node_modules/react-dnd-html5-backend/dist/esm/index.js"); }; }); }); },
/******/ 			"webpack/sharing/consume/default/react-data-grid/react-data-grid": function() { return loadStrictVersionCheckFallback("default", "react-data-grid", [7,7,0,0,,"beta",7], function() { return __webpack_require__.e("react-data-grid_lib_bundle_js").then(function() { return function() { return __webpack_require__(/*! react-data-grid */ "../react-data-grid/lib/bundle.js"); }; }); }); },
/******/ 			"webpack/sharing/consume/default/react-autosuggest/react-autosuggest": function() { return loadStrictVersionCheckFallback("default", "react-autosuggest", [4,9,4,3], function() { return Promise.all([__webpack_require__.e("vendors-node_modules_react-autosuggest_dist_index_js"), __webpack_require__.e("webpack_sharing_consume_default_prop-types_prop-types-webpack_sharing_consume_default_prop-ty-9754ad")]).then(function() { return function() { return __webpack_require__(/*! react-autosuggest */ "./node_modules/react-autosuggest/dist/index.js"); }; }); }); },
/******/ 			"webpack/sharing/consume/default/@lumino/algorithm": function() { return loadSingletonVersionCheck("default", "@lumino/algorithm", [1,1,3,3]); },
/******/ 			"webpack/sharing/consume/default/@lumino/properties": function() { return loadSingletonVersionCheck("default", "@lumino/properties", [1,1,2,3]); },
/******/ 			"webpack/sharing/consume/default/@lumino/disposable": function() { return loadSingletonVersionCheck("default", "@lumino/disposable", [1,1,4,3]); },
/******/ 			"webpack/sharing/consume/default/@jupyterlab/services": function() { return loadSingletonVersionCheck("default", "@jupyterlab/services", [1,6,2,4]); },
/******/ 			"webpack/sharing/consume/default/@jupyterlab/docmanager": function() { return loadSingletonVersionCheck("default", "@jupyterlab/docmanager", [1,3,2,4]); },
/******/ 			"webpack/sharing/consume/default/@jupyterlab/mainmenu": function() { return loadSingletonVersionCheck("default", "@jupyterlab/mainmenu", [1,3,2,4]); },
/******/ 			"webpack/sharing/consume/default/@jupyterlab/logconsole": function() { return loadSingletonVersionCheck("default", "@jupyterlab/logconsole", [1,3,2,4]); },
/******/ 			"webpack/sharing/consume/default/@jupyterlab/rendermime": function() { return loadSingletonVersionCheck("default", "@jupyterlab/rendermime", [1,3,2,4]); },
/******/ 			"webpack/sharing/consume/default/@jupyterlab/apputils": function() { return loadSingletonVersionCheck("default", "@jupyterlab/apputils", [1,3,2,4]); },
/******/ 			"webpack/sharing/consume/default/@jupyterlab/notebook": function() { return loadSingletonVersionCheck("default", "@jupyterlab/notebook", [1,3,2,4]); },
/******/ 			"webpack/sharing/consume/default/@jupyterlab/settingregistry": function() { return loadSingletonVersionCheck("default", "@jupyterlab/settingregistry", [1,3,2,4]); },
/******/ 			"webpack/sharing/consume/default/@jupyterlab/application": function() { return loadSingletonVersionCheck("default", "@jupyterlab/application", [1,3,2,4]); },
/******/ 			"webpack/sharing/consume/default/@jupyterlab/ui-components": function() { return loadSingletonVersionCheck("default", "@jupyterlab/ui-components", [1,3,2,4]); },
/******/ 			"webpack/sharing/consume/default/@lumino/widgets": function() { return loadSingletonVersionCheck("default", "@lumino/widgets", [1,1,19,0]); },
/******/ 			"webpack/sharing/consume/default/@lumino/coreutils": function() { return loadSingletonVersionCheck("default", "@lumino/coreutils", [1,1,5,3]); },
/******/ 			"webpack/sharing/consume/default/jupyterlab_toastify/jupyterlab_toastify": function() { return loadStrictVersionCheckFallback("default", "jupyterlab_toastify", [1,4,2,1], function() { return Promise.all([__webpack_require__.e("vendors-node_modules_jupyterlab_toastify_lib_index_js"), __webpack_require__.e("webpack_sharing_consume_default_prop-types_prop-types-_7bc8")]).then(function() { return function() { return __webpack_require__(/*! jupyterlab_toastify */ "./node_modules/jupyterlab_toastify/lib/index.js"); }; }); }); },
/******/ 			"webpack/sharing/consume/default/sourcemap-codec/sourcemap-codec": function() { return loadStrictVersionCheckFallback("default", "sourcemap-codec", [1,1,4,8], function() { return __webpack_require__.e("node_modules_sourcemap-codec_dist_sourcemap-codec_es_js").then(function() { return function() { return __webpack_require__(/*! sourcemap-codec */ "./node_modules/sourcemap-codec/dist/sourcemap-codec.es.js"); }; }); }); },
/******/ 			"webpack/sharing/consume/default/@jupyterlab/outputarea": function() { return loadVersionCheck("default", "@jupyterlab/outputarea", [1,3,2,4]); },
/******/ 			"webpack/sharing/consume/default/@jupyterlab/cells": function() { return loadVersionCheck("default", "@jupyterlab/cells", [1,3,2,4]); },
/******/ 			"webpack/sharing/consume/default/prop-types/prop-types?7bc8": function() { return loadStrictVersionCheckFallback("default", "prop-types", [1,15,8,1], function() { return __webpack_require__.e("vendors-node_modules_fortawesome_react-fontawesome_node_modules_prop-types_index_js").then(function() { return function() { return __webpack_require__(/*! prop-types */ "./node_modules/@fortawesome/react-fontawesome/node_modules/prop-types/index.js"); }; }); }); },
/******/ 			"webpack/sharing/consume/default/prop-types/prop-types?8efc": function() { return loadStrictVersionCheckFallback("default", "prop-types", [1,15,5,10], function() { return __webpack_require__.e("vendors-node_modules_react-autosuggest_node_modules_prop-types_index_js").then(function() { return function() { return __webpack_require__(/*! prop-types */ "./node_modules/react-autosuggest/node_modules/prop-types/index.js"); }; }); }); },
/******/ 			"webpack/sharing/consume/default/prop-types/prop-types?3d74": function() { return loadStrictVersionCheckFallback("default", "prop-types", [1,15,5,8], function() { return __webpack_require__.e("vendors-node_modules_react-autowhatever_node_modules_prop-types_index_js").then(function() { return function() { return __webpack_require__(/*! prop-types */ "./node_modules/react-autowhatever/node_modules/prop-types/index.js"); }; }); }); },
/******/ 			"webpack/sharing/consume/default/clsx/clsx?d593": function() { return loadStrictVersionCheckFallback("default", "clsx", [1,1,1,1], function() { return __webpack_require__.e("react-data-grid_node_modules_clsx_dist_clsx_m_js").then(function() { return function() { return __webpack_require__(/*! clsx */ "../react-data-grid/node_modules/clsx/dist/clsx.m.js"); }; }); }); },
/******/ 			"webpack/sharing/consume/default/redux/redux?6bc0": function() { return loadStrictVersionCheckFallback("default", "redux", [1,4,0,4], function() { return __webpack_require__.e("vendors-node_modules_dnd-core_node_modules_redux_es_redux_js").then(function() { return function() { return __webpack_require__(/*! redux */ "./node_modules/dnd-core/node_modules/redux/es/redux.js"); }; }); }); },
/******/ 			"webpack/sharing/consume/default/prop-types/prop-types?0f41": function() { return loadStrictVersionCheckFallback("default", "prop-types", [1,15,7,2], function() { return __webpack_require__.e("vendors-node_modules_react-redux_node_modules_prop-types_index_js").then(function() { return function() { return __webpack_require__(/*! prop-types */ "./node_modules/react-redux/node_modules/prop-types/index.js"); }; }); }); },
/******/ 			"webpack/sharing/consume/default/clsx/clsx?d96a": function() { return loadStrictVersionCheckFallback("default", "clsx", [1,1,1,1], function() { return __webpack_require__.e("node_modules_clsx_dist_clsx_m_js").then(function() { return function() { return __webpack_require__(/*! clsx */ "./node_modules/clsx/dist/clsx.m.js"); }; }); }); }
/******/ 		};
/******/ 		// no consumes in initial chunks
/******/ 		var chunkMapping = {
/******/ 			"webpack_sharing_consume_default_react": [
/******/ 				"webpack/sharing/consume/default/react"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_react-dom": [
/******/ 				"webpack/sharing/consume/default/react-dom"
/******/ 			],
/******/ 			"lib_containers_TableView_index_js-lib_containers_TextView_index_js-webpack_sharing_consume_de-5d1d96": [
/******/ 				"webpack/sharing/consume/default/react-redux/react-redux",
/******/ 				"webpack/sharing/consume/default/redux/redux?375d",
/******/ 				"webpack/sharing/consume/default/immer/immer",
/******/ 				"webpack/sharing/consume/default/react-fast-compare/react-fast-compare",
/******/ 				"webpack/sharing/consume/default/color/color",
/******/ 				"webpack/sharing/consume/default/react-dnd/react-dnd",
/******/ 				"webpack/sharing/consume/default/react-dnd-html5-backend/react-dnd-html5-backend",
/******/ 				"webpack/sharing/consume/default/react-data-grid/react-data-grid",
/******/ 				"webpack/sharing/consume/default/react-autosuggest/react-autosuggest"
/******/ 			],
/******/ 			"lib_jupyter_plugin_js": [
/******/ 				"webpack/sharing/consume/default/@lumino/algorithm",
/******/ 				"webpack/sharing/consume/default/@lumino/properties",
/******/ 				"webpack/sharing/consume/default/@lumino/disposable",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/services",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/docmanager",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/mainmenu",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/logconsole",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/rendermime",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/apputils",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/notebook",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/settingregistry",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/application",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/ui-components",
/******/ 				"webpack/sharing/consume/default/@lumino/widgets",
/******/ 				"webpack/sharing/consume/default/@lumino/coreutils",
/******/ 				"webpack/sharing/consume/default/jupyterlab_toastify/jupyterlab_toastify",
/******/ 				"webpack/sharing/consume/default/sourcemap-codec/sourcemap-codec",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/outputarea",
/******/ 				"webpack/sharing/consume/default/@jupyterlab/cells"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_prop-types_prop-types-_7bc8": [
/******/ 				"webpack/sharing/consume/default/prop-types/prop-types?7bc8"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_prop-types_prop-types-webpack_sharing_consume_default_prop-ty-9754ad": [
/******/ 				"webpack/sharing/consume/default/prop-types/prop-types?8efc",
/******/ 				"webpack/sharing/consume/default/prop-types/prop-types?3d74"
/******/ 			],
/******/ 			"react-data-grid_lib_bundle_js": [
/******/ 				"webpack/sharing/consume/default/clsx/clsx?d593"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_redux_redux": [
/******/ 				"webpack/sharing/consume/default/redux/redux?6bc0"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_prop-types_prop-types-_0f41": [
/******/ 				"webpack/sharing/consume/default/prop-types/prop-types?0f41"
/******/ 			],
/******/ 			"webpack_sharing_consume_default_clsx_clsx": [
/******/ 				"webpack/sharing/consume/default/clsx/clsx?d96a"
/******/ 			]
/******/ 		};
/******/ 		__webpack_require__.f.consumes = function(chunkId, promises) {
/******/ 			if(__webpack_require__.o(chunkMapping, chunkId)) {
/******/ 				chunkMapping[chunkId].forEach(function(id) {
/******/ 					if(__webpack_require__.o(installedModules, id)) return promises.push(installedModules[id]);
/******/ 					var onFactory = function(factory) {
/******/ 						installedModules[id] = 0;
/******/ 						__webpack_require__.m[id] = function(module) {
/******/ 							delete __webpack_require__.c[id];
/******/ 							module.exports = factory();
/******/ 						}
/******/ 					};
/******/ 					var onError = function(error) {
/******/ 						delete installedModules[id];
/******/ 						__webpack_require__.m[id] = function(module) {
/******/ 							delete __webpack_require__.c[id];
/******/ 							throw error;
/******/ 						}
/******/ 					};
/******/ 					try {
/******/ 						var promise = moduleToHandlerMapping[id]();
/******/ 						if(promise.then) {
/******/ 							promises.push(installedModules[id] = promise.then(onFactory)['catch'](onError));
/******/ 						} else onFactory(promise);
/******/ 					} catch(e) { onError(e); }
/******/ 				});
/******/ 			}
/******/ 		}
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/jsonp chunk loading */
/******/ 	!function() {
/******/ 		// no baseURI
/******/ 		
/******/ 		// object to store loaded and loading chunks
/******/ 		// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 		// [resolve, reject, Promise] = chunk loading, 0 = chunk loaded
/******/ 		var installedChunks = {
/******/ 			"metanno": 0
/******/ 		};
/******/ 		
/******/ 		__webpack_require__.f.j = function(chunkId, promises) {
/******/ 				// JSONP chunk loading for javascript
/******/ 				var installedChunkData = __webpack_require__.o(installedChunks, chunkId) ? installedChunks[chunkId] : undefined;
/******/ 				if(installedChunkData !== 0) { // 0 means "already installed".
/******/ 		
/******/ 					// a Promise means "currently loading".
/******/ 					if(installedChunkData) {
/******/ 						promises.push(installedChunkData[2]);
/******/ 					} else {
/******/ 						if(!/^webpack_sharing_consume_default_(prop\-types_prop\-types\-(_0f41|_7bc8|webpack_sharing_consume_default_prop\-ty\-9754ad)|re(act(|\-dom)|dux_redux)|clsx_clsx)$/.test(chunkId)) {
/******/ 							// setup Promise in chunk cache
/******/ 							var promise = new Promise(function(resolve, reject) { installedChunkData = installedChunks[chunkId] = [resolve, reject]; });
/******/ 							promises.push(installedChunkData[2] = promise);
/******/ 		
/******/ 							// start chunk loading
/******/ 							var url = __webpack_require__.p + __webpack_require__.u(chunkId);
/******/ 							// create error before stack unwound to get useful stacktrace later
/******/ 							var error = new Error();
/******/ 							var loadingEnded = function(event) {
/******/ 								if(__webpack_require__.o(installedChunks, chunkId)) {
/******/ 									installedChunkData = installedChunks[chunkId];
/******/ 									if(installedChunkData !== 0) installedChunks[chunkId] = undefined;
/******/ 									if(installedChunkData) {
/******/ 										var errorType = event && (event.type === 'load' ? 'missing' : event.type);
/******/ 										var realSrc = event && event.target && event.target.src;
/******/ 										error.message = 'Loading chunk ' + chunkId + ' failed.\n(' + errorType + ': ' + realSrc + ')';
/******/ 										error.name = 'ChunkLoadError';
/******/ 										error.type = errorType;
/******/ 										error.request = realSrc;
/******/ 										installedChunkData[1](error);
/******/ 									}
/******/ 								}
/******/ 							};
/******/ 							__webpack_require__.l(url, loadingEnded, "chunk-" + chunkId, chunkId);
/******/ 						} else installedChunks[chunkId] = 0;
/******/ 					}
/******/ 				}
/******/ 		};
/******/ 		
/******/ 		// no prefetching
/******/ 		
/******/ 		// no preloaded
/******/ 		
/******/ 		// no HMR
/******/ 		
/******/ 		// no HMR manifest
/******/ 		
/******/ 		// no on chunks loaded
/******/ 		
/******/ 		// install a JSONP callback for chunk loading
/******/ 		var webpackJsonpCallback = function(parentChunkLoadingFunction, data) {
/******/ 			var chunkIds = data[0];
/******/ 			var moreModules = data[1];
/******/ 			var runtime = data[2];
/******/ 			// add "moreModules" to the modules object,
/******/ 			// then flag all "chunkIds" as loaded and fire callback
/******/ 			var moduleId, chunkId, i = 0;
/******/ 			if(chunkIds.some(function(id) { return installedChunks[id] !== 0; })) {
/******/ 				for(moduleId in moreModules) {
/******/ 					if(__webpack_require__.o(moreModules, moduleId)) {
/******/ 						__webpack_require__.m[moduleId] = moreModules[moduleId];
/******/ 					}
/******/ 				}
/******/ 				if(runtime) var result = runtime(__webpack_require__);
/******/ 			}
/******/ 			if(parentChunkLoadingFunction) parentChunkLoadingFunction(data);
/******/ 			for(;i < chunkIds.length; i++) {
/******/ 				chunkId = chunkIds[i];
/******/ 				if(__webpack_require__.o(installedChunks, chunkId) && installedChunks[chunkId]) {
/******/ 					installedChunks[chunkId][0]();
/******/ 				}
/******/ 				installedChunks[chunkId] = 0;
/******/ 			}
/******/ 		
/******/ 		}
/******/ 		
/******/ 		var chunkLoadingGlobal = self["webpackChunkmetanno"] = self["webpackChunkmetanno"] || [];
/******/ 		chunkLoadingGlobal.forEach(webpackJsonpCallback.bind(null, 0));
/******/ 		chunkLoadingGlobal.push = webpackJsonpCallback.bind(null, chunkLoadingGlobal.push.bind(chunkLoadingGlobal));
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/nonce */
/******/ 	!function() {
/******/ 		__webpack_require__.nc = undefined;
/******/ 	}();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// module cache are used so entry inlining is disabled
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	var __webpack_exports__ = __webpack_require__("webpack/container/entry/metanno");
/******/ 	(_JUPYTERLAB = typeof _JUPYTERLAB === "undefined" ? {} : _JUPYTERLAB).metanno = __webpack_exports__;
/******/ 	
/******/ })()
;
//# sourceMappingURL=remoteEntry.f3d25e929c7a1745b41a.js.map