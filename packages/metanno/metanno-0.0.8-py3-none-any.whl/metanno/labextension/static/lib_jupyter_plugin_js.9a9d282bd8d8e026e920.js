(self["webpackChunkmetanno"] = self["webpackChunkmetanno"] || []).push([["lib_jupyter_plugin_js"],{

/***/ "./lib/jupyter/dontDisplayHiddenOutput.js":
/*!************************************************!*\
  !*** ./lib/jupyter/dontDisplayHiddenOutput.js ***!
  \************************************************/
/***/ (function(__unused_webpack_module, __unused_webpack_exports, __webpack_require__) {

"use strict";


var _outputarea = __webpack_require__(/*! @jupyterlab/outputarea */ "webpack/sharing/consume/default/@jupyterlab/outputarea");

var _cells = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); enumerableOnly && (symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; })), keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = null != arguments[i] ? arguments[i] : {}; i % 2 ? ownKeys(Object(source), !0).forEach(function (key) { _defineProperty(target, key, source[key]); }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)) : ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { Promise.resolve(value).then(_next, _throw); } }

function _asyncToGenerator(fn) { return function () { var self = this, args = arguments; return new Promise(function (resolve, reject) { var gen = fn.apply(self, args); function _next(value) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value); } function _throw(err) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err); } _next(undefined); }); }; }

/**
 * The namespace for the `CodeCell` class statics.
 */

/**
 * Execute a cell given a client session.
 */
(function (CodeCell) {
  function execute(_x, _x2, _x3) {
    return _execute.apply(this, arguments);
  }

  function _execute() {
    _execute = _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee(cell, sessionContext, metadata) {
      var _cell$outputArea, _cell$outputArea$widg, _cell$outputArea$widg2, _cell$outputArea$widg3, _sessionContext$sessi;

      var model, code, canChangeHiddenState, cellId, _metadata, recordTiming, future, msgPromise, recordTimingHook, msg, timingInfo, started, finished;

      return regeneratorRuntime.wrap(function _callee$(_context) {
        while (1) {
          switch (_context.prev = _context.next) {
            case 0:
              model = cell.model;
              code = model.value.text;
              canChangeHiddenState = !(cell !== null && cell !== void 0 && (_cell$outputArea = cell.outputArea) !== null && _cell$outputArea !== void 0 && (_cell$outputArea$widg = _cell$outputArea.widgets) !== null && _cell$outputArea$widg !== void 0 && (_cell$outputArea$widg2 = _cell$outputArea$widg[0]) !== null && _cell$outputArea$widg2 !== void 0 && (_cell$outputArea$widg3 = _cell$outputArea$widg2.widgets) !== null && _cell$outputArea$widg3 !== void 0 && _cell$outputArea$widg3[1].editor_type); // <--- modified here

              if (!(!code.trim() || !((_sessionContext$sessi = sessionContext.session) !== null && _sessionContext$sessi !== void 0 && _sessionContext$sessi.kernel))) {
                _context.next = 6;
                break;
              }

              model.clearExecution();
              return _context.abrupt("return");

            case 6:
              cellId = {
                cellId: model.id
              };
              metadata = _objectSpread(_objectSpread(_objectSpread({}, model.metadata.toJSON()), metadata), cellId);
              _metadata = metadata, recordTiming = _metadata.recordTiming;
              model.clearExecution();

              if (canChangeHiddenState) {
                // <--- modified here
                cell.outputHidden = false;
              } // <--- modified here


              cell.setPrompt('*');
              model.trusted = true;
              _context.prev = 13;
              msgPromise = _outputarea.OutputArea.execute(code, cell.outputArea, sessionContext, metadata); // cell.outputArea.future assigned synchronously in `execute`

              if (recordTiming) {
                recordTimingHook = function recordTimingHook(msg) {
                  var label;

                  switch (msg.header.msg_type) {
                    case 'status':
                      label = "status.".concat(msg.content.execution_state);
                      break;

                    case 'execute_input':
                      label = 'execute_input';
                      break;

                    default:
                      return true;
                  } // If the data is missing, estimate it to now
                  // Date was added in 5.1: https://jupyter-client.readthedocs.io/en/stable/messaging.html#message-header


                  var value = msg.header.date || new Date().toISOString();
                  var timingInfo = Object.assign({}, model.metadata.get('execution'));
                  timingInfo["iopub.".concat(label)] = value;
                  model.metadata.set('execution', timingInfo);
                  return true;
                };

                cell.outputArea.future.registerMessageHook(recordTimingHook);
              } else {
                model.metadata.delete('execution');
              } // Save this execution's future so we can compare in the catch below.


              future = cell.outputArea.future;
              _context.next = 19;
              return msgPromise;

            case 19:
              msg = _context.sent;
              model.executionCount = msg.content.execution_count;

              if (recordTiming) {
                timingInfo = Object.assign({}, model.metadata.get('execution'));
                started = msg.metadata.started; // Started is not in the API, but metadata IPyKernel sends

                if (started) {
                  timingInfo['shell.execute_reply.started'] = started;
                } // Per above, the 5.0 spec does not assume date, so we estimate is required


                finished = msg.header.date;
                timingInfo['shell.execute_reply'] = finished || new Date().toISOString();
                model.metadata.set('execution', timingInfo);
              }

              return _context.abrupt("return", msg);

            case 25:
              _context.prev = 25;
              _context.t0 = _context["catch"](13);

              // If we started executing, and the cell is still indicating this
              // execution, clear the prompt.
              if (future && !cell.isDisposed && cell.outputArea.future === future) {
                cell.setPrompt('');
              }

              throw _context.t0;

            case 29:
            case "end":
              return _context.stop();
          }
        }
      }, _callee, null, [[13, 25]]);
    }));
    return _execute.apply(this, arguments);
  }

  CodeCell.old_execute = CodeCell.execute;
  CodeCell.execute = execute;
})(_cells.CodeCell);

/***/ }),

/***/ "./lib/jupyter/loadTranscypt.js":
/*!**************************************!*\
  !*** ./lib/jupyter/loadTranscypt.js ***!
  \**************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.eval_code = eval_code;

var _immer = __webpack_require__(/*! immer */ "webpack/sharing/consume/default/immer/immer");

function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { Promise.resolve(value).then(_next, _throw); } }

function _asyncToGenerator(fn) { return function () { var self = this, args = arguments; return new Promise(function (resolve, reject) { var gen = fn.apply(self, args); function _next(value) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value); } function _throw(err) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err); } _next(undefined); }); }; }

var _require = __webpack_require__(/*! ./org.transcrypt.__runtime__.js */ "./lib/jupyter/org.transcrypt.__runtime__.js"),
    AssertionError = _require.AssertionError,
    AttributeError = _require.AttributeError,
    BaseException = _require.BaseException,
    DeprecationWarning = _require.DeprecationWarning,
    Exception = _require.Exception,
    IndexError = _require.IndexError,
    IterableError = _require.IterableError,
    KeyError = _require.KeyError,
    NotImplementedError = _require.NotImplementedError,
    RuntimeWarning = _require.RuntimeWarning,
    StopIteration = _require.StopIteration,
    UserWarning = _require.UserWarning,
    ValueError = _require.ValueError,
    Warning = _require.Warning,
    __JsIterator__ = _require.__JsIterator__,
    __PyIterator__ = _require.__PyIterator__,
    __Terminal__ = _require.__Terminal__,
    __add__ = _require.__add__,
    __and__ = _require.__and__,
    __call__ = _require.__call__,
    __class__ = _require.__class__,
    __envir__ = _require.__envir__,
    __eq__ = _require.__eq__,
    __floordiv__ = _require.__floordiv__,
    __ge__ = _require.__ge__,
    __get__ = _require.__get__,
    __getcm__ = _require.__getcm__,
    __getitem__ = _require.__getitem__,
    __getslice__ = _require.__getslice__,
    __getsm__ = _require.__getsm__,
    __gt__ = _require.__gt__,
    __i__ = _require.__i__,
    __iadd__ = _require.__iadd__,
    __iand__ = _require.__iand__,
    __idiv__ = _require.__idiv__,
    __ijsmod__ = _require.__ijsmod__,
    __ilshift__ = _require.__ilshift__,
    __imatmul__ = _require.__imatmul__,
    __imod__ = _require.__imod__,
    __imul__ = _require.__imul__,
    __in__ = _require.__in__,
    __init__ = _require.__init__,
    __ior__ = _require.__ior__,
    __ipow__ = _require.__ipow__,
    __irshift__ = _require.__irshift__,
    __isub__ = _require.__isub__,
    __ixor__ = _require.__ixor__,
    __jsUsePyNext__ = _require.__jsUsePyNext__,
    __jsmod__ = _require.__jsmod__,
    __k__ = _require.__k__,
    __kwargtrans__ = _require.__kwargtrans__,
    __le__ = _require.__le__,
    __lshift__ = _require.__lshift__,
    __lt__ = _require.__lt__,
    __matmul__ = _require.__matmul__,
    __mergefields__ = _require.__mergefields__,
    __mergekwargtrans__ = _require.__mergekwargtrans__,
    __mod__ = _require.__mod__,
    __mul__ = _require.__mul__,
    __ne__ = _require.__ne__,
    __neg__ = _require.__neg__,
    __nest__ = _require.__nest__,
    __or__ = _require.__or__,
    __pow__ = _require.__pow__,
    __pragma__ = _require.__pragma__,
    __proxy__ = _require.__proxy__,
    __pyUseJsNext__ = _require.__pyUseJsNext__,
    __rshift__ = _require.__rshift__,
    __setitem__ = _require.__setitem__,
    __setproperty__ = _require.__setproperty__,
    __setslice__ = _require.__setslice__,
    __sort__ = _require.__sort__,
    __specialattrib__ = _require.__specialattrib__,
    __sub__ = _require.__sub__,
    __super__ = _require.__super__,
    __t__ = _require.__t__,
    __terminal__ = _require.__terminal__,
    __truediv__ = _require.__truediv__,
    __withblock__ = _require.__withblock__,
    __xor__ = _require.__xor__,
    abs = _require.abs,
    all = _require.all,
    any = _require.any,
    assert = _require.assert,
    bool = _require.bool,
    bytearray = _require.bytearray,
    bytes = _require.bytes,
    callable = _require.callable,
    chr = _require.chr,
    copy = _require.copy,
    deepcopy = _require.deepcopy,
    delattr = _require.delattr,
    dict = _require.dict,
    dir = _require.dir,
    divmod = _require.divmod,
    enumerate = _require.enumerate,
    filter = _require.filter,
    float = _require.float,
    getattr = _require.getattr,
    hasattr = _require.hasattr,
    input = _require.input,
    int = _require.int,
    isinstance = _require.isinstance,
    issubclass = _require.issubclass,
    len = _require.len,
    list = _require.list,
    map = _require.map,
    max = _require.max,
    min = _require.min,
    object = _require.object,
    ord = _require.ord,
    pow = _require.pow,
    print = _require.print,
    property = _require.property,
    py_TypeError = _require.py_TypeError,
    py_iter = _require.py_iter,
    py_metatype = _require.py_metatype,
    py_next = _require.py_next,
    py_reversed = _require.py_reversed,
    py_typeof = _require.py_typeof,
    range = _require.range,
    repr = _require.repr,
    round = _require.round,
    set = _require.set,
    setattr = _require.setattr,
    sorted = _require.sorted,
    str = _require.str,
    sum = _require.sum,
    tuple = _require.tuple,
    zip = _require.zip;

var chain_map = function chain_map() {
  for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
    args[_key] = arguments[_key];
  }

  return Object.assign.apply(Object, [{}].concat(args));
};

var chain_list = function chain_list() {
  for (var _len2 = arguments.length, args = new Array(_len2), _key2 = 0; _key2 < _len2; _key2++) {
    args[_key2] = arguments[_key2];
  }

  return [].concat.apply([], args);
};

var kernel_only = function kernel_only(fn) {
  var func_name = fn();
  return function (self) {
    for (var _len3 = arguments.length, args = new Array(_len3 > 1 ? _len3 - 1 : 0), _key3 = 1; _key3 < _len3; _key3++) {
      args[_key3 - 1] = arguments[_key3];
    }

    return self.manager.remoteCall(func_name, args);
  };
};

var frontend_only = function frontend_only(fn) {
  fn.frontend_only = true;
  return fn;
};

var produce = function produce(fn) {
  var new_fn = /*#__PURE__*/function () {
    var _ref = _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee(self) {
      var recordedPatches,
          _len4,
          args,
          _key4,
          newState,
          _args = arguments;

      return regeneratorRuntime.wrap(function _callee$(_context) {
        while (1) {
          switch (_context.prev = _context.next) {
            case 0:
              recordedPatches = []; // Create a new immer draft for the state and make it available to the app instance

              self.state = (0, _immer.createDraft)(self.manager.store.getState()); // Await the function result (in case it is async, when it queries the backend)

              for (_len4 = _args.length, args = new Array(_len4 > 1 ? _len4 - 1 : 0), _key4 = 1; _key4 < _len4; _key4++) {
                args[_key4 - 1] = _args[_key4];
              }

              _context.next = 5;
              return fn.apply(void 0, [self].concat(args));

            case 5:
              // Finish the draft and if the state has changed, update the redux state and send the patches to the backend
              (0, _immer.finishDraft)(self.state, function (patches, inversePatches) {
                return recordedPatches = patches;
              });

              if (!recordedPatches.length) {
                _context.next = 12;
                break;
              }

              newState = (0, _immer.applyPatches)(self.manager.store.getState(), recordedPatches);
              self.manager.store.dispatch({
                type: 'SET_STATE',
                payload: newState
              }); // @ts-ignore

              if (!(new_fn.frontend_only || fn.frontend_only)) {
                _context.next = 11;
                break;
              }

              return _context.abrupt("return");

            case 11:
              self.manager.comm.send({
                'method': 'patch',
                'data': {
                  'patches': recordedPatches
                }
              }, {
                id: self.manager.id
              });

            case 12:
              delete self.state;

            case 13:
            case "end":
              return _context.stop();
          }
        }
      }, _callee);
    }));

    return function new_fn(_x) {
      return _ref.apply(this, arguments);
    };
  }();

  return new_fn;
};

var get_idx = function get_idx(items, value) {
  var key = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : "id";

  for (var i = 0; i < items.length; i++) {
    if (items[i][key] === value) {
      return i;
    }
  }
};

function __keys__(obj) {
  if (!(obj instanceof Object)) return obj.keys();
  var keys = [];

  for (var attrib in obj) {
    if (!__specialattrib__(attrib)) {
      keys.push(attrib);
    }
  }

  return keys;
}

function __items__(obj) {
  if (!(obj instanceof Object)) return obj.items();
  var items = [];

  for (var attrib in obj) {
    if (!__specialattrib__(attrib)) {
      items.push([attrib, obj[attrib]]);
    }
  }

  return items;
}

function __clear__(obj) {
  if (!(obj instanceof Object)) return obj.clear();

  for (var attrib in obj) {
    delete obj[attrib];
  }
}

function __getdefault__(obj, aKey, aDefault) {
  if (!(obj instanceof Object)) return obj.get(aKey, aDefault);
  var result = obj[aKey];

  if (result == undefined) {
    result = obj['py_' + aKey];
  }

  return result == undefined ? aDefault == undefined ? null : aDefault : result;
}

function __setdefault__(obj, aKey, aDefault) {
  if (!(obj instanceof Object)) return obj.setdefault(aKey, aDefault);
  var result = obj[aKey];

  if (result != undefined) {
    return result;
  }

  var val = aDefault == undefined ? null : aDefault;
  obj[aKey] = val;
  return val;
}

function __pop__(obj, aKey, aDefault) {
  if (!(obj instanceof Object)) return obj.pop(aKey, aDefault);
  var result = obj[aKey];

  if (result != undefined) {
    delete obj[aKey];
    return result;
  } else {
    if (aDefault === undefined) {
      throw KeyError(aKey, new Error());
    }
  }

  return aDefault;
}

function __popitem__(obj) {
  if (!(obj instanceof Object)) return obj.popitem();
  var aKey = Object.keys(obj)[0];

  if (aKey == null) {
    throw KeyError("popitem(): dictionary is empty", new Error());
  }

  var result = tuple([aKey, obj[aKey]]);
  delete obj[aKey];
  return result;
}

function __update__(obj, aDict) {
  if (!(obj instanceof Object)) return obj.update(aDict);

  for (var aKey in aDict) {
    obj[aKey] = aDict[aKey];
  }
}

function __values__(obj) {
  if (!(obj instanceof Object)) return obj.values();
  var values = [];

  for (var attrib in obj) {
    if (!__specialattrib__(attrib)) {
      values.push(obj[attrib]);
    }
  }

  return values;
}

function eval_code(code) {
  return eval(code);
}

/***/ }),

/***/ "./lib/jupyter/manager.js":
/*!********************************!*\
  !*** ./lib/jupyter/manager.js ***!
  \********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

__webpack_require__(/*! regenerator-runtime/runtime */ "./node_modules/regenerator-runtime/runtime.js");

var _react = _interopRequireDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));

var _redux = __webpack_require__(/*! redux */ "webpack/sharing/consume/default/redux/redux?375d");

var _loadTranscypt = __webpack_require__(/*! ./loadTranscypt */ "./lib/jupyter/loadTranscypt.js");

var _immer = __webpack_require__(/*! immer */ "webpack/sharing/consume/default/immer/immer");

var _jupyterlab_toastify = __webpack_require__(/*! jupyterlab_toastify */ "webpack/sharing/consume/default/jupyterlab_toastify/jupyterlab_toastify");

var _coreutils = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");

var _sourcemapCodec = __webpack_require__(/*! sourcemap-codec */ "webpack/sharing/consume/default/sourcemap-codec/sourcemap-codec");

__webpack_require__(/*! ./metanno.css */ "./lib/jupyter/metanno.css");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }

function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _iterableToArrayLimit(arr, i) { var _i = arr == null ? null : typeof Symbol !== "undefined" && arr[Symbol.iterator] || arr["@@iterator"]; if (_i == null) return; var _arr = []; var _n = true; var _d = false; var _s, _e; try { for (_i = _i.call(arr); !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }

function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _iterableToArray(iter) { if (typeof Symbol !== "undefined" && iter[Symbol.iterator] != null || iter["@@iterator"] != null) return Array.from(iter); }

function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { Promise.resolve(value).then(_next, _throw); } }

function _asyncToGenerator(fn) { return function () { var self = this, args = arguments; return new Promise(function (resolve, reject) { var gen = fn.apply(self, args); function _next(value) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value); } function _throw(err) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err); } _next(undefined); }); }; }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); Object.defineProperty(Constructor, "prototype", { writable: false }); return Constructor; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

(0, _immer.enablePatches)();

var metannoManager = /*#__PURE__*/_createClass( //modelsSync: Map<any>;
// Lock promise to chain events, and avoid concurrent state access
// Each event calls .then on this promise and replaces it to queue itself
function metannoManager(context, settings) {
  var _this = this,
      _context$sessionConte;

  _classCallCheck(this, metannoManager);

  _defineProperty(this, "actions", void 0);

  _defineProperty(this, "app", void 0);

  _defineProperty(this, "store", void 0);

  _defineProperty(this, "views", void 0);

  _defineProperty(this, "id", void 0);

  _defineProperty(this, "context", void 0);

  _defineProperty(this, "isDisposed", void 0);

  _defineProperty(this, "comm_target_name", void 0);

  _defineProperty(this, "settings", void 0);

  _defineProperty(this, "comm", void 0);

  _defineProperty(this, "source_code_py", void 0);

  _defineProperty(this, "sourcemap", void 0);

  _defineProperty(this, "callbacks", void 0);

  _defineProperty(this, "lock", void 0);

  _defineProperty(this, "_handleCommOpen", function (comm, msg) {
    // const data = (msg.content.data);
    // hydrate state ?
    _this.comm = comm;
    _this.comm.onMsg = _this.onMsg;

    _this.comm.send({
      "method": "sync_request",
      "data": {}
    });
  });

  _defineProperty(this, "_create_comm", /*#__PURE__*/function () {
    var _ref = _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee(target_name, model_id, data, metadata, buffers) {
      var _this$context$session;

      var kernel, comm;
      return regeneratorRuntime.wrap(function _callee$(_context) {
        while (1) {
          switch (_context.prev = _context.next) {
            case 0:
              kernel = (_this$context$session = _this.context.sessionContext.session) === null || _this$context$session === void 0 ? void 0 : _this$context$session.kernel;

              if (kernel) {
                _context.next = 3;
                break;
              }

              throw new Error('No current kernel');

            case 3:
              comm = kernel.createComm(target_name, model_id);

              if (data || metadata) {
                comm.open(data, metadata, buffers);
              }

              return _context.abrupt("return", comm);

            case 6:
            case "end":
              return _context.stop();
          }
        }
      }, _callee);
    }));

    return function (_x, _x2, _x3, _x4, _x5) {
      return _ref.apply(this, arguments);
    };
  }());

  _defineProperty(this, "_get_comm_info", /*#__PURE__*/_asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee2() {
    var _this$context$session2;

    var kernel, reply;
    return regeneratorRuntime.wrap(function _callee2$(_context2) {
      while (1) {
        switch (_context2.prev = _context2.next) {
          case 0:
            kernel = (_this$context$session2 = _this.context.sessionContext.session) === null || _this$context$session2 === void 0 ? void 0 : _this$context$session2.kernel;

            if (kernel) {
              _context2.next = 3;
              break;
            }

            throw new Error('No current kernel');

          case 3:
            _context2.next = 5;
            return kernel.requestCommInfo({
              target_name: _this.comm_target_name
            });

          case 5:
            reply = _context2.sent;

            if (!(reply.content.status === 'ok')) {
              _context2.next = 10;
              break;
            }

            return _context2.abrupt("return", reply.content.comms);

          case 10:
            return _context2.abrupt("return", {});

          case 11:
          case "end":
            return _context2.stop();
        }
      }
    }, _callee2);
  })));

  _defineProperty(this, "connectToAnyKernel", /*#__PURE__*/_asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee3() {
    var all_comm_ids, relevant_comm_ids, comm;
    return regeneratorRuntime.wrap(function _callee3$(_context3) {
      while (1) {
        switch (_context3.prev = _context3.next) {
          case 0:
            if (_this.context.sessionContext) {
              _context3.next = 2;
              break;
            }

            return _context3.abrupt("return");

          case 2:
            _context3.next = 4;
            return _this.context.sessionContext.ready;

          case 4:
            if (!(_this.context.sessionContext.session.kernel.handleComms === false)) {
              _context3.next = 6;
              break;
            }

            return _context3.abrupt("return");

          case 6:
            _context3.next = 8;
            return _this._get_comm_info();

          case 8:
            all_comm_ids = _context3.sent;
            relevant_comm_ids = Object.keys(all_comm_ids).filter(function (key) {
              return all_comm_ids[key]['target_name'] === _this.comm_target_name;
            });
            console.log("Jupyter annotator comm ids", relevant_comm_ids, "(there should be at most one)");

            if (!(relevant_comm_ids.length > 0)) {
              _context3.next = 16;
              break;
            }

            _context3.next = 14;
            return _this._create_comm(_this.comm_target_name, relevant_comm_ids[0]);

          case 14:
            comm = _context3.sent;

            _this._handleCommOpen(comm);

          case 16:
          case "end":
            return _context3.stop();
        }
      }
    }, _callee3);
  })));

  _defineProperty(this, "registerRemoteCallback", function (callbackId, callback) {
    _this.callbacks[callbackId] = callback;
  });

  _defineProperty(this, "remoteCall", function (func_name, args) {
    var callbackId = _coreutils.UUID.uuid4();

    _this.comm.send({
      'method': 'method_call',
      'data': {
        'method_name': func_name,
        'args': args,
        'callback_id': callbackId
      }
    });

    return new Promise(function (resolve, reject) {
      _this.registerRemoteCallback(callbackId, resolve);
    });
  });

  _defineProperty(this, "onMsg", function (msg) {
    try {
      var _msg$metadata;

      var _ref4 = msg.content.data,
          method = _ref4.method,
          data = _ref4.data;
      var exceptId = msg === null || msg === void 0 ? void 0 : (_msg$metadata = msg.metadata) === null || _msg$metadata === void 0 ? void 0 : _msg$metadata.exceptId;

      if (_this.id === exceptId) {
        return;
      }

      if (method === "action") {
        _this.store.dispatch(data);
      } else if (method === "method_call") {
        var _this$app;

        (_this$app = _this.app)[data.method_name].apply(_this$app, _toConsumableArray(data.args));
      } else if (method === "method_return") {
        _this.callbacks[data.callback_id](data.value);

        delete _this.callbacks[data.callback_id];
      } else if (method === "patch") {
        try {
          var newState = (0, _immer.applyPatches)(_this.store.getState(), data.patches);

          _this.store.dispatch({
            'type': 'SET_STATE',
            'payload': newState
          });
        } catch (error) {
          console.error("ERROR DURING PATCHING");
          console.error(error);
        }
      } else if (method === "set_app_code") {
        _this.app = (0, _loadTranscypt.eval_code)(data.code)();
        _this.sourcemap = (0, _sourcemapCodec.decode)(data.sourcemap);
        _this.source_code_py = data.py_code;
        _this.app.manager = _this;

        _this.views.forEach(function (view) {
          return view.showContent();
        });
      } else if (method === "sync") {
        _this.store.dispatch({
          'type': 'SET_STATE',
          'payload': data.state
        });
      }
    } catch (e) {
      console.error("Error during comm message reception", e);
    }
  });

  _defineProperty(this, "handle_exception", function (e) {
    console.log("Got an error !");
    console.log(e);

    var py_lines = _toConsumableArray(e.stack.matchAll(/<anonymous>:(\d+):(\d+)/gm));

    if (py_lines.length > 0 && _this.sourcemap !== null) {
      var _py_lines$ = _slicedToArray(py_lines[0], 3),
          _ = _py_lines$[0],
          lineStr = _py_lines$[1],
          columnStr = _py_lines$[2];

      var source_line_str = _this.source_code_py.split("\n")[_this.sourcemap[parseInt(lineStr) - 1][0][2]].trim();

      _this.toastError("Error: ".concat(e.message, " at \n").concat(source_line_str));
    } else {
      // @ts-ignore
      if (e.__args__) {
        // @ts-ignore
        _this.toastError("Error: ".concat(e.__args__[0]));
      } else {
        _this.toastError("Error: ".concat(e.message));
      }
    }
  });

  _defineProperty(this, "queue_try_catch_exec", function (fn) {
    for (var _len = arguments.length, args = new Array(_len > 1 ? _len - 1 : 0), _key = 1; _key < _len; _key++) {
      args[_key - 1] = arguments[_key];
    }

    _this.lock = _this.lock.then(function () {
      return _this.try_catch_exec.apply(_this, [fn].concat(args));
    }).catch(_this.handle_exception);
  });

  _defineProperty(this, "try_catch_exec", function (fn) {
    try {
      if (fn) {
        for (var _len2 = arguments.length, args = new Array(_len2 > 1 ? _len2 - 1 : 0), _key2 = 1; _key2 < _len2; _key2++) {
          args[_key2 - 1] = arguments[_key2];
        }

        return fn.apply(void 0, args);
      }
    } catch (e) {
      _this.handle_exception(e);
    }
  });

  _defineProperty(this, "toastError", function (message) {
    var autoClose = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 10000;

    //INotification.error(`Message: ${e.message} at ${parseInt(lineStr)-1}:${parseInt(columnStr)-1}`);
    _jupyterlab_toastify.INotification.error( /*#__PURE__*/_react.default.createElement("div", null, message.split("\n").map(function (line) {
      return /*#__PURE__*/_react.default.createElement("p", null, line);
    })), {
      autoClose: autoClose
    });
  });

  _defineProperty(this, "toastInfo", function (message) {
    var autoClose = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 10000;

    //INotification.error(`Message: ${e.message} at ${parseInt(lineStr)-1}:${parseInt(columnStr)-1}`);
    _jupyterlab_toastify.INotification.info( /*#__PURE__*/_react.default.createElement("div", null, message.split("\n").map(function (line) {
      return /*#__PURE__*/_react.default.createElement("p", null, line);
    })), {
      autoClose: autoClose
    });
  });

  _defineProperty(this, "_handleKernelChanged", function (_ref5) {
    var name = _ref5.name,
        oldValue = _ref5.oldValue,
        newValue = _ref5.newValue;

    if (oldValue) {
      _this.comm = null;
      oldValue.removeCommTarget(_this.comm_target_name, _this._handleCommOpen);
    }

    if (newValue) {
      newValue.registerCommTarget(_this.comm_target_name, _this._handleCommOpen);
    }
  });

  _defineProperty(this, "_handleKernelStatusChange", function (status) {
    switch (status) {
      case 'autorestarting':
      case 'restarting':
      case 'dead':
        //this.disconnect();
        break;

      default:
    }
  });

  _defineProperty(this, "dispose", function () {
    if (_this.isDisposed) {
      return;
    }

    _this.isDisposed = true; // TODO do something with the comm ?
  });

  _defineProperty(this, "reduce", function () {
    var _this$app2;

    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : null;
    var action = arguments.length > 1 ? arguments[1] : undefined;

    if (action.type === 'SET_STATE') {
      return action.payload;
    }

    if ((_this$app2 = _this.app) !== null && _this$app2 !== void 0 && _this$app2.reduce) {
      return _this.app.reduce(state, action);
    }

    return state;
  });

  _defineProperty(this, "getState", function () {
    return _this.store.getState();
  });

  _defineProperty(this, "dispatch", function (action) {
    return _this.store.dispatch(action);
  });

  _defineProperty(this, "createStore", function () {
    var composeEnhancers = (typeof window === "undefined" ? "undefined" : _typeof(window)) === 'object' && // @ts-ignore
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ ? // @ts-ignore
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__({// Specify extension’s options like name, actionsBlacklist, actionsCreators, serialize...
    }) : _redux.compose;
    return (0, _redux.createStore)(_this.reduce, composeEnhancers((0, _redux.applyMiddleware)()));
  });

  this.store = this.createStore();
  this.actions = {};
  this.app = null;
  this.id = _coreutils.UUID.uuid4();
  this.callbacks = {};
  this.comm_target_name = 'metanno';
  this.context = context;
  this.comm = null;
  this.views = new Set();
  this.lock = Promise.resolve();
  this.source_code_py = '';
  this.sourcemap = null; // this.modelsSync = new Map();
  // this.onUnhandledIOPubMessage = new Signal(this);
  // https://github.com/jupyter-widgets/ipywidgets/commit/5b922f23e54f3906ed9578747474176396203238

  context.sessionContext.kernelChanged.connect(function (sender, args) {
    _this._handleKernelChanged(args);
  });
  context.sessionContext.statusChanged.connect(function (sender, status) {
    _this._handleKernelStatusChange(status);
  });

  if ((_context$sessionConte = context.sessionContext.session) !== null && _context$sessionConte !== void 0 && _context$sessionConte.kernel) {
    var _context$sessionConte2;

    this._handleKernelChanged({
      name: 'kernel',
      oldValue: null,
      newValue: (_context$sessionConte2 = context.sessionContext.session) === null || _context$sessionConte2 === void 0 ? void 0 : _context$sessionConte2.kernel
    });
  }

  this.connectToAnyKernel().then(); //() => {});

  this.settings = settings;
  /*context.saveState.connect((sender, saveState) => {
      if (saveState === 'started' && settings.saveState) {
          this.saveState();
      }
  });*/
});

exports["default"] = metannoManager;

/***/ }),

/***/ "./lib/jupyter/org.transcrypt.__runtime__.js":
/*!***************************************************!*\
  !*** ./lib/jupyter/org.transcrypt.__runtime__.js ***!
  \***************************************************/
/***/ (function(__unused_webpack_module, exports) {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.Warning = exports.ValueError = exports.UserWarning = exports.StopIteration = exports.RuntimeWarning = exports.NotImplementedError = exports.KeyError = exports.IterableError = exports.IndexError = exports.Exception = exports.DeprecationWarning = exports.BaseException = exports.AttributeError = exports.AssertionError = void 0;
exports.__JsIterator__ = __JsIterator__;
exports.__PyIterator__ = __PyIterator__;
exports.__Terminal__ = void 0;
exports.__add__ = __add__;
exports.__and__ = __and__;
exports.__call__ = __call__;
exports.__class__ = __class__;
exports.__envir__ = void 0;
exports.__eq__ = __eq__;
exports.__floordiv__ = __floordiv__;
exports.__ge__ = __ge__;
exports.__get__ = __get__;
exports.__getcm__ = __getcm__;
exports.__getitem__ = __getitem__;
exports.__getslice__ = __getslice__;
exports.__getsm__ = __getsm__;
exports.__gt__ = __gt__;
exports.__i__ = __i__;
exports.__iadd__ = __iadd__;
exports.__iand__ = __iand__;
exports.__idiv__ = __idiv__;
exports.__ijsmod__ = __ijsmod__;
exports.__ilshift__ = __ilshift__;
exports.__imatmul__ = __imatmul__;
exports.__imod__ = __imod__;
exports.__imul__ = __imul__;
exports.__in__ = __in__;
exports.__init__ = __init__;
exports.__ior__ = __ior__;
exports.__ipow__ = __ipow__;
exports.__irshift__ = __irshift__;
exports.__isub__ = __isub__;
exports.__ixor__ = __ixor__;
exports.__jsUsePyNext__ = __jsUsePyNext__;
exports.__jsmod__ = __jsmod__;
exports.__k__ = __k__;
exports.__kwargtrans__ = __kwargtrans__;
exports.__le__ = __le__;
exports.__lshift__ = __lshift__;
exports.__lt__ = __lt__;
exports.__matmul__ = __matmul__;
exports.__mergefields__ = __mergefields__;
exports.__mergekwargtrans__ = __mergekwargtrans__;
exports.__mod__ = __mod__;
exports.__mul__ = __mul__;
exports.__ne__ = __ne__;
exports.__neg__ = __neg__;
exports.__nest__ = __nest__;
exports.__or__ = __or__;
exports.__pow__ = __pow__;
exports.__pragma__ = __pragma__;
exports.__proxy__ = void 0;
exports.__pyUseJsNext__ = __pyUseJsNext__;
exports.__rshift__ = __rshift__;
exports.__setitem__ = __setitem__;
exports.__setproperty__ = __setproperty__;
exports.__setslice__ = __setslice__;
exports.__sort__ = void 0;
exports.__specialattrib__ = __specialattrib__;
exports.__sub__ = __sub__;
exports.__super__ = __super__;
exports.__t__ = __t__;
exports.__terminal__ = void 0;
exports.__truediv__ = __truediv__;
exports.__withblock__ = __withblock__;
exports.__xor__ = __xor__;
exports.abs = void 0;
exports.all = all;
exports.any = any;
exports.assert = assert;
exports.bool = bool;
exports.bytearray = bytearray;
exports.bytes = void 0;
exports.callable = callable;
exports.chr = chr;
exports.copy = copy;
exports.deepcopy = deepcopy;
exports.delattr = delattr;
exports.dict = dict;
exports.dir = dir;
exports.divmod = void 0;
exports.enumerate = enumerate;
exports.filter = void 0;
exports.float = float;
exports.getattr = getattr;
exports.hasattr = hasattr;
exports.input = void 0;
exports.int = int;
exports.isinstance = isinstance;
exports.issubclass = issubclass;
exports.len = len;
exports.list = list;
exports.map = void 0;
exports.max = max;
exports.min = min;
exports.object = void 0;
exports.ord = ord;
exports.print = exports.pow = void 0;
exports.property = property;
exports.py_TypeError = void 0;
exports.py_iter = py_iter;
exports.py_metatype = void 0;
exports.py_next = py_next;
exports.py_reversed = py_reversed;
exports.py_typeof = py_typeof;
exports.range = range;
exports.repr = repr;
exports.round = round;
exports.set = set;
exports.setattr = setattr;
exports.sorted = void 0;
exports.str = str;
exports.sum = sum;
exports.tuple = tuple;
exports.zip = zip;

function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }

function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _iterableToArray(iter) { if (typeof Symbol !== "undefined" && iter[Symbol.iterator] != null || iter["@@iterator"] != null) return Array.from(iter); }

function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }

function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }

function _createForOfIteratorHelper(o, allowArrayLike) { var it = typeof Symbol !== "undefined" && o[Symbol.iterator] || o["@@iterator"]; if (!it) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = it.call(o); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

// Transcrypt'ed from Python, 2020-02-26 02:20:31
var __name__ = 'org.transcrypt.__runtime__';
var __envir__ = {};
exports.__envir__ = __envir__;
__envir__.interpreter_name = 'python';
__envir__.transpiler_name = 'transcrypt';
__envir__.executor_name = __envir__.transpiler_name;
__envir__.transpiler_version = '3.7.16';

function __nest__(headObject, tailNames, value) {
  var current = headObject;

  if (tailNames != '') {
    var tailChain = tailNames.split('.');
    var firstNewIndex = tailChain.length;

    for (var index = 0; index < tailChain.length; index++) {
      if (!current.hasOwnProperty(tailChain[index])) {
        firstNewIndex = index;
        break;
      }

      current = current[tailChain[index]];
    }

    for (var index = firstNewIndex; index < tailChain.length; index++) {
      current[tailChain[index]] = {};
      current = current[tailChain[index]];
    }
  }

  var _iterator = _createForOfIteratorHelper(Object.getOwnPropertyNames(value)),
      _step;

  try {
    var _loop = function _loop() {
      var attrib = _step.value;
      Object.defineProperty(current, attrib, {
        get: function get() {
          return value[attrib];
        },
        enumerable: true,
        configurable: true
      });
    };

    for (_iterator.s(); !(_step = _iterator.n()).done;) {
      _loop();
    }
  } catch (err) {
    _iterator.e(err);
  } finally {
    _iterator.f();
  }
}

;

function __init__(module) {
  if (!module.__inited__) {
    module.__all__.__init__(module.__all__);

    module.__inited__ = true;
  }

  return module.__all__;
}

;
var __proxy__ = false;
exports.__proxy__ = __proxy__;

function __get__(self, func, quotedFuncName) {
  if (self) {
    if (self.hasOwnProperty('__class__') || typeof self == 'string' || self instanceof String) {
      if (quotedFuncName) {
        Object.defineProperty(self, quotedFuncName, {
          value: function value() {
            var args = [].slice.apply(arguments);
            return func.apply(null, [self].concat(args));
          },
          writable: true,
          enumerable: true,
          configurable: true
        });
      }

      return function () {
        var args = [].slice.apply(arguments);
        return func.apply(null, [self].concat(args));
      };
    } else {
      return func;
    }
  } else {
    return func;
  }
}

;

function __getcm__(self, func, quotedFuncName) {
  if (self.hasOwnProperty('__class__')) {
    return function () {
      var args = [].slice.apply(arguments);
      return func.apply(null, [self.__class__].concat(args));
    };
  } else {
    return function () {
      var args = [].slice.apply(arguments);
      return func.apply(null, [self].concat(args));
    };
  }
}

;

function __getsm__(self, func, quotedFuncName) {
  return func;
}

;
var py_metatype = {
  __name__: 'type',
  __bases__: [],
  __new__: function __new__(meta, name, bases, attribs) {
    var cls = function cls() {
      var args = [].slice.apply(arguments);
      return cls.__new__(args);
    };

    for (var index = bases.length - 1; index >= 0; index--) {
      var base = bases[index];

      for (var attrib in base) {
        var descrip = Object.getOwnPropertyDescriptor(base, attrib);
        Object.defineProperty(cls, attrib, descrip);
      }

      var _iterator2 = _createForOfIteratorHelper(Object.getOwnPropertySymbols(base)),
          _step2;

      try {
        for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
          var symbol = _step2.value;

          var _descrip = Object.getOwnPropertyDescriptor(base, symbol);

          Object.defineProperty(cls, symbol, _descrip);
        }
      } catch (err) {
        _iterator2.e(err);
      } finally {
        _iterator2.f();
      }
    }

    cls.__metaclass__ = meta;
    cls.__name__ = name.startsWith('py_') ? name.slice(3) : name;
    cls.__bases__ = bases;

    for (var attrib in attribs) {
      var descrip = Object.getOwnPropertyDescriptor(attribs, attrib);
      Object.defineProperty(cls, attrib, descrip);
    }

    var _iterator3 = _createForOfIteratorHelper(Object.getOwnPropertySymbols(attribs)),
        _step3;

    try {
      for (_iterator3.s(); !(_step3 = _iterator3.n()).done;) {
        var _symbol = _step3.value;

        var _descrip2 = Object.getOwnPropertyDescriptor(attribs, _symbol);

        Object.defineProperty(cls, _symbol, _descrip2);
      }
    } catch (err) {
      _iterator3.e(err);
    } finally {
      _iterator3.f();
    }

    return cls;
  }
};
exports.py_metatype = py_metatype;
py_metatype.__metaclass__ = py_metatype;
var object = {
  __init__: function __init__(self) {},
  __metaclass__: py_metatype,
  __name__: 'object',
  __bases__: [],
  __new__: function __new__(args) {
    var instance = Object.create(this, {
      __class__: {
        value: this,
        enumerable: true
      }
    });

    if ('__getattr__' in this || '__setattr__' in this) {
      instance = new Proxy(instance, {
        get: function get(target, name) {
          var result = target[name];

          if (result == undefined) {
            return target.__getattr__(name);
          } else {
            return result;
          }
        },
        set: function set(target, name, value) {
          try {
            target.__setattr__(name, value);
          } catch (exception) {
            target[name] = value;
          }

          return true;
        }
      });
    }

    this.__init__.apply(null, [instance].concat(args));

    return instance;
  }
};
exports.object = object;

function __class__(name, bases, attribs, meta) {
  if (meta === undefined) {
    meta = bases[0].__metaclass__;
  }

  return meta.__new__(meta, name, bases, attribs);
}

;

function __pragma__() {}

;

function
  /* <callee>, <this>, <params>* */
__call__() {
  var args = [].slice.apply(arguments);

  if (_typeof(args[0]) == 'object' && '__call__' in args[0]) {
    return args[0].__call__.apply(args[1], args.slice(2));
  } else {
    return args[0].apply(args[1], args.slice(2));
  }
}

;
__envir__.executor_name = __envir__.transpiler_name;
var __main__ = {
  __file__: ''
};
var __except__ = null;

function __kwargtrans__(anObject) {
  anObject.__kwargtrans__ = null;
  anObject.constructor = Object;
  return anObject;
}

function __super__(aClass, methodName) {
  var _iterator4 = _createForOfIteratorHelper(aClass.__bases__),
      _step4;

  try {
    for (_iterator4.s(); !(_step4 = _iterator4.n()).done;) {
      var base = _step4.value;

      if (methodName in base) {
        return base[methodName];
      }
    }
  } catch (err) {
    _iterator4.e(err);
  } finally {
    _iterator4.f();
  }

  throw new Exception('Superclass method not found');
}

function property(getter, setter) {
  if (!setter) {
    setter = function setter() {};
  }

  return {
    get: function get() {
      return getter(this);
    },
    set: function set(value) {
      setter(this, value);
    },
    enumerable: true
  };
}

function __setproperty__(anObject, name, descriptor) {
  if (!anObject.hasOwnProperty(name)) {
    Object.defineProperty(anObject, name, descriptor);
  }
}

function assert(condition, message) {
  if (!condition) {
    throw AssertionError(message, new Error());
  }
}

function __mergekwargtrans__(object0, object1) {
  var result = {};

  for (var attrib in object0) {
    result[attrib] = object0[attrib];
  }

  for (var attrib in object1) {
    result[attrib] = object1[attrib];
  }

  return result;
}

;

function __mergefields__(targetClass, sourceClass) {
  var fieldNames = ['__reprfields__', '__comparefields__', '__initfields__'];

  if (sourceClass[fieldNames[0]]) {
    if (targetClass[fieldNames[0]]) {
      var _iterator5 = _createForOfIteratorHelper(fieldNames),
          _step5;

      try {
        for (_iterator5.s(); !(_step5 = _iterator5.n()).done;) {
          var fieldName = _step5.value;
          targetClass[fieldName] = new Set([].concat(_toConsumableArray(targetClass[fieldName]), _toConsumableArray(sourceClass[fieldName])));
        }
      } catch (err) {
        _iterator5.e(err);
      } finally {
        _iterator5.f();
      }
    } else {
      var _iterator6 = _createForOfIteratorHelper(fieldNames),
          _step6;

      try {
        for (_iterator6.s(); !(_step6 = _iterator6.n()).done;) {
          var _fieldName = _step6.value;
          targetClass[_fieldName] = new Set(sourceClass[_fieldName]);
        }
      } catch (err) {
        _iterator6.e(err);
      } finally {
        _iterator6.f();
      }
    }
  }
}

function __withblock__(manager, statements) {
  if (hasattr(manager, '__enter__')) {
    try {
      manager.__enter__();

      statements();

      manager.__exit__();
    } catch (exception) {
      if (!manager.__exit__(exception.name, exception, exception.stack)) {
        throw exception;
      }
    }
  } else {
    statements();
    manager.close();
  }
}

;

function dir(obj) {
  var aList = [];

  for (var aKey in obj) {
    aList.push(aKey.startsWith('py_') ? aKey.slice(3) : aKey);
  }

  aList.sort();
  return aList;
}

;

function setattr(obj, name, value) {
  obj[name] = value;
}

;

function getattr(obj, name) {
  return name in obj ? obj[name] : obj['py_' + name];
}

;

function hasattr(obj, name) {
  try {
    return name in obj || 'py_' + name in obj;
  } catch (exception) {
    return false;
  }
}

;

function delattr(obj, name) {
  if (name in obj) {
    delete obj[name];
  } else {
    delete obj['py_' + name];
  }
}

;

function __in__(element, container) {
  if (container === undefined || container === null) {
    return false;
  }

  if (container.__contains__ instanceof Function) {
    return container.__contains__(element);
  } else {
    return container.indexOf ? container.indexOf(element) > -1 : container.hasOwnProperty(element);
  }
}

;

function __specialattrib__(attrib) {
  return attrib.startswith('__') && attrib.endswith('__') || attrib == 'constructor' || attrib.startswith('py_');
}

;

function len(anObject) {
  if (anObject === undefined || anObject === null) {
    return 0;
  }

  if (anObject.__len__ instanceof Function) {
    return anObject.__len__();
  }

  if (anObject.length !== undefined) {
    return anObject.length;
  }

  var length = 0;

  for (var attr in anObject) {
    if (!__specialattrib__(attr)) {
      length++;
    }
  }

  return length;
}

;

function __i__(any) {
  return py_typeof(any) == dict ? any.py_keys() : any;
}

function __k__(keyed, key) {
  var result = keyed[key];

  if (typeof result == 'undefined') {
    if (keyed instanceof Array) {
      if (key == +key && key >= 0 && keyed.length > key) return result;else throw IndexError(key, new Error());
    } else throw KeyError(key, new Error());
  }

  return result;
}

function __t__(target) {
  return target === undefined || target === null ? false : ['boolean', 'number'].indexOf(_typeof(target)) >= 0 ? target : target.__bool__ instanceof Function ? target.__bool__() ? target : false : target.__len__ instanceof Function ? target.__len__() !== 0 ? target : false : target instanceof Function ? target : len(target) !== 0 ? target : false;
}

function float(any) {
  if (any == 'inf') {
    return Infinity;
  } else if (any == '-inf') {
    return -Infinity;
  } else if (any == 'nan') {
    return NaN;
  } else if (isNaN(parseFloat(any))) {
    if (any === false) {
      return 0;
    } else if (any === true) {
      return 1;
    } else {
      throw ValueError("could not convert string to float: '" + str(any) + "'", new Error());
    }
  } else {
    return +any;
  }
}

;
float.__name__ = 'float';
float.__bases__ = [object];

function int(any) {
  return float(any) | 0;
}

;
int.__name__ = 'int';
int.__bases__ = [object];

function bool(any) {
  return !!__t__(any);
}

;
bool.__name__ = 'bool';
bool.__bases__ = [int];

function py_typeof(anObject) {
  var aType = _typeof(anObject);

  if (aType == 'object') {
    try {
      return '__class__' in anObject ? anObject.__class__ : object;
    } catch (exception) {
      return aType;
    }
  } else {
    return aType == 'boolean' ? bool : aType == 'string' ? str : aType == 'number' ? anObject % 1 == 0 ? int : float : null;
  }
}

;

function issubclass(aClass, classinfo) {
  if (classinfo instanceof Array) {
    var _iterator7 = _createForOfIteratorHelper(classinfo),
        _step7;

    try {
      for (_iterator7.s(); !(_step7 = _iterator7.n()).done;) {
        var _aClass = _step7.value;

        if (issubclass(aClass, _aClass)) {
          return true;
        }
      }
    } catch (err) {
      _iterator7.e(err);
    } finally {
      _iterator7.f();
    }

    return false;
  }

  try {
    var aClass2 = aClass;

    if (aClass2 == classinfo) {
      return true;
    } else {
      var bases = [].slice.call(aClass2.__bases__);

      while (bases.length) {
        aClass2 = bases.shift();

        if (aClass2 == classinfo) {
          return true;
        }

        if (aClass2.__bases__.length) {
          bases = [].slice.call(aClass2.__bases__).concat(bases);
        }
      }

      return false;
    }
  } catch (exception) {
    return aClass == classinfo || classinfo == object;
  }
}

;

function isinstance(anObject, classinfo) {
  try {
    return '__class__' in anObject ? issubclass(anObject.__class__, classinfo) : issubclass(py_typeof(anObject), classinfo);
  } catch (exception) {
    return issubclass(py_typeof(anObject), classinfo);
  }
}

;

function callable(anObject) {
  return anObject && _typeof(anObject) == 'object' && '__call__' in anObject ? true : typeof anObject === 'function';
}

;

function repr(anObject) {
  try {
    return anObject.__repr__();
  } catch (exception) {
    try {
      return anObject.__str__();
    } catch (exception) {
      try {
        if (anObject == null) {
          return 'None';
        } else if (anObject.constructor == Object) {
          var result = '{';
          var comma = false;

          for (var attrib in anObject) {
            if (!__specialattrib__(attrib)) {
              if (attrib.isnumeric()) {
                var attribRepr = attrib;
              } else {
                var attribRepr = '\'' + attrib + '\'';
              }

              if (comma) {
                result += ', ';
              } else {
                comma = true;
              }

              result += attribRepr + ': ' + repr(anObject[attrib]);
            }
          }

          result += '}';
          return result;
        } else {
          return typeof anObject == 'boolean' ? anObject.toString().capitalize() : anObject.toString();
        }
      } catch (exception) {
        return '<object of type: ' + _typeof(anObject) + '>';
      }
    }
  }
}

;

function chr(charCode) {
  return String.fromCharCode(charCode);
}

;

function ord(aChar) {
  return aChar.charCodeAt(0);
}

;

function max(nrOrSeq) {
  return arguments.length == 1 ? Math.max.apply(Math, _toConsumableArray(nrOrSeq)) : Math.max.apply(Math, arguments);
}

;

function min(nrOrSeq) {
  return arguments.length == 1 ? Math.min.apply(Math, _toConsumableArray(nrOrSeq)) : Math.min.apply(Math, arguments);
}

;
var abs = Math.abs;
exports.abs = abs;

function round(number, ndigits) {
  if (ndigits) {
    var scale = Math.pow(10, ndigits);
    number *= scale;
  }

  var rounded = Math.round(number);

  if (rounded - number == 0.5 && rounded % 2) {
    rounded -= 1;
  }

  if (ndigits) {
    rounded /= scale;
  }

  return rounded;
}

;

function __jsUsePyNext__() {
  try {
    var result = this.__next__();

    return {
      value: result,
      done: false
    };
  } catch (exception) {
    return {
      value: undefined,
      done: true
    };
  }
}

function __pyUseJsNext__() {
  var result = this.next();

  if (result.done) {
    throw StopIteration(new Error());
  } else {
    return result.value;
  }
}

function py_iter(iterable) {
  if (typeof iterable == 'string' || '__iter__' in iterable) {
    var result = iterable.__iter__();

    result.next = __jsUsePyNext__;
  } else if ('selector' in iterable) {
    var result = list(iterable).__iter__();

    result.next = __jsUsePyNext__;
  } else if ('next' in iterable) {
    var result = iterable;

    if (!('__next__' in result)) {
      result.__next__ = __pyUseJsNext__;
    }
  } else if (Symbol.iterator in iterable) {
    var result = iterable[Symbol.iterator]();
    result.__next__ = __pyUseJsNext__;
  } else {
    throw IterableError(new Error());
  }

  result[Symbol.iterator] = function () {
    return result;
  };

  return result;
}

function py_next(iterator) {
  try {
    var result = iterator.__next__();
  } catch (exception) {
    var result = iterator.next();

    if (result.done) {
      throw StopIteration(new Error());
    } else {
      return result.value;
    }
  }

  if (result == undefined) {
    throw StopIteration(new Error());
  } else {
    return result;
  }
}

function __PyIterator__(iterable) {
  this.iterable = iterable;
  this.index = 0;
}

__PyIterator__.prototype.__next__ = function () {
  if (this.index < this.iterable.length) {
    return this.iterable[this.index++];
  } else {
    throw StopIteration(new Error());
  }
};

function __JsIterator__(iterable) {
  this.iterable = iterable;
  this.index = 0;
}

__JsIterator__.prototype.next = function () {
  if (this.index < this.iterable.py_keys.length) {
    return {
      value: this.index++,
      done: false
    };
  } else {
    return {
      value: undefined,
      done: true
    };
  }
};

function py_reversed(iterable) {
  iterable = iterable.slice();
  iterable.reverse();
  return iterable;
}

;

function zip() {
  var args = [].slice.call(arguments);

  for (var i = 0; i < args.length; i++) {
    if (typeof args[i] == 'string') {
      args[i] = args[i].split('');
    } else if (!Array.isArray(args[i])) {
      args[i] = Array.from(args[i]);
    }
  }

  var shortest = args.length == 0 ? [] : args.reduce(function (array0, array1) {
    return array0.length < array1.length ? array0 : array1;
  });
  return shortest.map(function (current, index) {
    return args.map(function (current) {
      return current[index];
    });
  });
}

;

function range(start, stop, step) {
  if (stop == undefined) {
    stop = start;
    start = 0;
  }

  if (step == undefined) {
    step = 1;
  }

  if (step > 0 && start >= stop || step < 0 && start <= stop) {
    return [];
  }

  var result = [];

  for (var i = start; step > 0 ? i < stop : i > stop; i += step) {
    result.push(i);
  }

  return result;
}

;

function any(iterable) {
  var _iterator8 = _createForOfIteratorHelper(iterable),
      _step8;

  try {
    for (_iterator8.s(); !(_step8 = _iterator8.n()).done;) {
      var item = _step8.value;

      if (bool(item)) {
        return true;
      }
    }
  } catch (err) {
    _iterator8.e(err);
  } finally {
    _iterator8.f();
  }

  return false;
}

function all(iterable) {
  var _iterator9 = _createForOfIteratorHelper(iterable),
      _step9;

  try {
    for (_iterator9.s(); !(_step9 = _iterator9.n()).done;) {
      var item = _step9.value;

      if (!bool(item)) {
        return false;
      }
    }
  } catch (err) {
    _iterator9.e(err);
  } finally {
    _iterator9.f();
  }

  return true;
}

function sum(iterable) {
  var result = 0;

  var _iterator10 = _createForOfIteratorHelper(iterable),
      _step10;

  try {
    for (_iterator10.s(); !(_step10 = _iterator10.n()).done;) {
      var item = _step10.value;
      result += item;
    }
  } catch (err) {
    _iterator10.e(err);
  } finally {
    _iterator10.f();
  }

  return result;
}

function enumerate(iterable) {
  return zip(range(len(iterable)), iterable);
}

function copy(anObject) {
  if (anObject == null || _typeof(anObject) == "object") {
    return anObject;
  } else {
    var result = {};

    for (var attrib in obj) {
      if (anObject.hasOwnProperty(attrib)) {
        result[attrib] = anObject[attrib];
      }
    }

    return result;
  }
}

function deepcopy(anObject) {
  if (anObject == null || _typeof(anObject) == "object") {
    return anObject;
  } else {
    var result = {};

    for (var attrib in obj) {
      if (anObject.hasOwnProperty(attrib)) {
        result[attrib] = deepcopy(anObject[attrib]);
      }
    }

    return result;
  }
}

function list(iterable) {
  var instance = iterable ? Array.from(iterable) : [];
  return instance;
}

Array.prototype.__class__ = list;
list.__name__ = 'list';
list.__bases__ = [object];

Array.prototype.__iter__ = function () {
  return new __PyIterator__(this);
};

Array.prototype.__getslice__ = function (start, stop, step) {
  if (start < 0) {
    start = this.length + start;
  }

  if (stop == null) {
    stop = this.length;
  } else if (stop < 0) {
    stop = this.length + stop;
  } else if (stop > this.length) {
    stop = this.length;
  }

  if (step == 1) {
    return Array.prototype.slice.call(this, start, stop);
  }

  var result = list([]);

  for (var index = start; index < stop; index += step) {
    result.push(this[index]);
  }

  return result;
};

Array.prototype.__setslice__ = function (start, stop, step, source) {
  if (start < 0) {
    start = this.length + start;
  }

  if (stop == null) {
    stop = this.length;
  } else if (stop < 0) {
    stop = this.length + stop;
  }

  if (step == null) {
    Array.prototype.splice.apply(this, [start, stop - start].concat(source));
  } else {
    var sourceIndex = 0;

    for (var targetIndex = start; targetIndex < stop; targetIndex += step) {
      this[targetIndex] = source[sourceIndex++];
    }
  }
};

Array.prototype.__repr__ = function () {
  if (this.__class__ == set && !this.length) {
    return 'set()';
  }

  var result = !this.__class__ || this.__class__ == list ? '[' : this.__class__ == tuple ? '(' : '{';

  for (var index = 0; index < this.length; index++) {
    if (index) {
      result += ', ';
    }

    result += repr(this[index]);
  }

  if (this.__class__ == tuple && this.length == 1) {
    result += ',';
  }

  result += !this.__class__ || this.__class__ == list ? ']' : this.__class__ == tuple ? ')' : '}';
  ;
  return result;
};

Array.prototype.__str__ = Array.prototype.__repr__;

Array.prototype.append = function (element) {
  this.push(element);
};

Array.prototype.py_clear = function () {
  this.length = 0;
};

Array.prototype.extend = function (aList) {
  this.push.apply(this, aList);
};

Array.prototype.insert = function (index, element) {
  this.splice(index, 0, element);
};

Array.prototype.remove = function (element) {
  var index = this.indexOf(element);

  if (index == -1) {
    throw ValueError("list.remove(x): x not in list", new Error());
  }

  this.splice(index, 1);
};

Array.prototype.index = function (element) {
  return this.indexOf(element);
};

Array.prototype.py_pop = function (index) {
  if (index == undefined) {
    return this.pop();
  } else {
    return this.splice(index, 1)[0];
  }
};

Array.prototype.py_sort = function () {
  __sort__.apply(null, [this].concat([].slice.apply(arguments)));
};

Array.prototype.__add__ = function (aList) {
  return list(this.concat(aList));
};

Array.prototype.__mul__ = function (scalar) {
  var result = this;

  for (var i = 1; i < scalar; i++) {
    result = result.concat(this);
  }

  return result;
};

Array.prototype.__rmul__ = Array.prototype.__mul__;

function tuple(iterable) {
  var instance = iterable ? [].slice.apply(iterable) : [];
  instance.__class__ = tuple;
  return instance;
}

tuple.__name__ = 'tuple';
tuple.__bases__ = [object];

function set(iterable) {
  var instance = [];

  if (iterable) {
    for (var index = 0; index < iterable.length; index++) {
      instance.add(iterable[index]);
    }
  }

  instance.__class__ = set;
  return instance;
}

set.__name__ = 'set';
set.__bases__ = [object];

Array.prototype.__bindexOf__ = function (element) {
  element += '';
  var mindex = 0;
  var maxdex = this.length - 1;

  while (mindex <= maxdex) {
    var index = (mindex + maxdex) / 2 | 0;
    var middle = this[index] + '';

    if (middle < element) {
      mindex = index + 1;
    } else if (middle > element) {
      maxdex = index - 1;
    } else {
      return index;
    }
  }

  return -1;
};

Array.prototype.add = function (element) {
  if (this.indexOf(element) == -1) {
    this.push(element);
  }
};

Array.prototype.discard = function (element) {
  var index = this.indexOf(element);

  if (index != -1) {
    this.splice(index, 1);
  }
};

Array.prototype.isdisjoint = function (other) {
  this.sort();

  for (var i = 0; i < other.length; i++) {
    if (this.__bindexOf__(other[i]) != -1) {
      return false;
    }
  }

  return true;
};

Array.prototype.issuperset = function (other) {
  this.sort();

  for (var i = 0; i < other.length; i++) {
    if (this.__bindexOf__(other[i]) == -1) {
      return false;
    }
  }

  return true;
};

Array.prototype.issubset = function (other) {
  return set(other.slice()).issuperset(this);
};

Array.prototype.union = function (other) {
  var result = set(this.slice().sort());

  for (var i = 0; i < other.length; i++) {
    if (result.__bindexOf__(other[i]) == -1) {
      result.push(other[i]);
    }
  }

  return result;
};

Array.prototype.intersection = function (other) {
  this.sort();
  var result = set();

  for (var i = 0; i < other.length; i++) {
    if (this.__bindexOf__(other[i]) != -1) {
      result.push(other[i]);
    }
  }

  return result;
};

Array.prototype.difference = function (other) {
  var sother = set(other.slice().sort());
  var result = set();

  for (var i = 0; i < this.length; i++) {
    if (sother.__bindexOf__(this[i]) == -1) {
      result.push(this[i]);
    }
  }

  return result;
};

Array.prototype.symmetric_difference = function (other) {
  return this.union(other).difference(this.intersection(other));
};

Array.prototype.py_update = function () {
  var updated = [].concat.apply(this.slice(), arguments).sort();
  this.py_clear();

  for (var i = 0; i < updated.length; i++) {
    if (updated[i] != updated[i - 1]) {
      this.push(updated[i]);
    }
  }
};

Array.prototype.__eq__ = function (other) {
  if (this.length != other.length) {
    return false;
  }

  if (this.__class__ == set) {
    this.sort();
    other.sort();
  }

  for (var i = 0; i < this.length; i++) {
    if (this[i] != other[i]) {
      return false;
    }
  }

  return true;
};

Array.prototype.__ne__ = function (other) {
  return !this.__eq__(other);
};

Array.prototype.__le__ = function (other) {
  if (this.__class__ == set) {
    return this.issubset(other);
  } else {
    for (var i = 0; i < this.length; i++) {
      if (this[i] > other[i]) {
        return false;
      } else if (this[i] < other[i]) {
        return true;
      }
    }

    return true;
  }
};

Array.prototype.__ge__ = function (other) {
  if (this.__class__ == set) {
    return this.issuperset(other);
  } else {
    for (var i = 0; i < this.length; i++) {
      if (this[i] < other[i]) {
        return false;
      } else if (this[i] > other[i]) {
        return true;
      }
    }

    return true;
  }
};

Array.prototype.__lt__ = function (other) {
  return this.__class__ == set ? this.issubset(other) && !this.issuperset(other) : !this.__ge__(other);
};

Array.prototype.__gt__ = function (other) {
  return this.__class__ == set ? this.issuperset(other) && !this.issubset(other) : !this.__le__(other);
};

function bytearray(bytable, encoding) {
  if (bytable == undefined) {
    return new Uint8Array(0);
  } else {
    var aType = py_typeof(bytable);

    if (aType == int) {
      return new Uint8Array(bytable);
    } else if (aType == str) {
      var aBytes = new Uint8Array(len(bytable));

      for (var i = 0; i < len(bytable); i++) {
        aBytes[i] = bytable.charCodeAt(i);
      }

      return aBytes;
    } else if (aType == list || aType == tuple) {
      return new Uint8Array(bytable);
    } else {
      throw py_TypeError;
    }
  }
}

var bytes = bytearray;
exports.bytes = bytes;

Uint8Array.prototype.__add__ = function (aBytes) {
  var result = new Uint8Array(this.length + aBytes.length);
  result.set(this);
  result.set(aBytes, this.length);
  return result;
};

Uint8Array.prototype.__mul__ = function (scalar) {
  var result = new Uint8Array(scalar * this.length);

  for (var i = 0; i < scalar; i++) {
    result.set(this, i * this.length);
  }

  return result;
};

Uint8Array.prototype.__rmul__ = Uint8Array.prototype.__mul__;

function str(stringable) {
  if (typeof stringable === 'number') return stringable.toString();else {
    try {
      return stringable.__str__();
    } catch (exception) {
      try {
        return repr(stringable);
      } catch (exception) {
        return String(stringable);
      }
    }
  }
}

;
String.prototype.__class__ = str;
str.__name__ = 'str';
str.__bases__ = [object];

String.prototype.__iter__ = function () {
  new __PyIterator__(this);
};

String.prototype.__repr__ = function () {
  return (this.indexOf('\'') == -1 ? '\'' + this + '\'' : '"' + this + '"').py_replace('\t', '\\t').py_replace('\n', '\\n');
};

String.prototype.__str__ = function () {
  return this;
};

String.prototype.capitalize = function () {
  return this.charAt(0).toUpperCase() + this.slice(1);
};

String.prototype.endswith = function (suffix) {
  if (suffix instanceof Array) {
    for (var i = 0; i < suffix.length; i++) {
      if (this.slice(-suffix[i].length) == suffix[i]) return true;
    }
  } else return suffix == '' || this.slice(-suffix.length) == suffix;

  return false;
};

String.prototype.find = function (sub, start) {
  return this.indexOf(sub, start);
};

String.prototype.__getslice__ = function (start, stop, step) {
  if (start < 0) {
    start = this.length + start;
  }

  if (stop == null) {
    stop = this.length;
  } else if (stop < 0) {
    stop = this.length + stop;
  }

  var result = '';

  if (step == 1) {
    result = this.substring(start, stop);
  } else {
    for (var index = start; index < stop; index += step) {
      result = result.concat(this.charAt(index));
    }
  }

  return result;
};

__setproperty__(String.prototype, 'format', {
  get: function get() {
    return __get__(this, function (self) {
      var args = tuple([].slice.apply(arguments).slice(1));
      var autoIndex = 0;
      return self.replace(/\{(\w*)\}/g, function (match, key) {
        if (key == '') {
          key = autoIndex++;
        }

        if (key == +key) {
          return args[key] === undefined ? match : str(args[key]);
        } else {
          for (var index = 0; index < args.length; index++) {
            if (_typeof(args[index]) == 'object' && args[index][key] !== undefined) {
              return str(args[index][key]);
            }
          }

          return match;
        }
      });
    });
  },
  enumerable: true
});

String.prototype.isalnum = function () {
  return /^[0-9a-zA-Z]{1,}$/.test(this);
};

String.prototype.isalpha = function () {
  return /^[a-zA-Z]{1,}$/.test(this);
};

String.prototype.isdecimal = function () {
  return /^[0-9]{1,}$/.test(this);
};

String.prototype.isdigit = function () {
  return this.isdecimal();
};

String.prototype.islower = function () {
  return /^[a-z]{1,}$/.test(this);
};

String.prototype.isupper = function () {
  return /^[A-Z]{1,}$/.test(this);
};

String.prototype.isspace = function () {
  return /^[\s]{1,}$/.test(this);
};

String.prototype.isnumeric = function () {
  return !isNaN(parseFloat(this)) && isFinite(this);
};

String.prototype.join = function (strings) {
  strings = Array.from(strings);
  return strings.join(this);
};

String.prototype.lower = function () {
  return this.toLowerCase();
};

String.prototype.py_replace = function (old, aNew, maxreplace) {
  return this.split(old, maxreplace).join(aNew);
};

String.prototype.lstrip = function () {
  return this.replace(/^\s*/g, '');
};

String.prototype.rfind = function (sub, start) {
  return this.lastIndexOf(sub, start);
};

String.prototype.rsplit = function (sep, maxsplit) {
  if (sep == undefined || sep == null) {
    sep = /\s+/;
    var stripped = this.strip();
  } else {
    var stripped = this;
  }

  if (maxsplit == undefined || maxsplit == -1) {
    return stripped.split(sep);
  } else {
    var result = stripped.split(sep);

    if (maxsplit < result.length) {
      var maxrsplit = result.length - maxsplit;
      return [result.slice(0, maxrsplit).join(sep)].concat(result.slice(maxrsplit));
    } else {
      return result;
    }
  }
};

String.prototype.rstrip = function () {
  return this.replace(/\s*$/g, '');
};

String.prototype.py_split = function (sep, maxsplit) {
  if (sep == undefined || sep == null) {
    sep = /\s+/;
    var stripped = this.strip();
  } else {
    var stripped = this;
  }

  if (maxsplit == undefined || maxsplit == -1) {
    return stripped.split(sep);
  } else {
    var result = stripped.split(sep);

    if (maxsplit < result.length) {
      return result.slice(0, maxsplit).concat([result.slice(maxsplit).join(sep)]);
    } else {
      return result;
    }
  }
};

String.prototype.startswith = function (prefix) {
  if (prefix instanceof Array) {
    for (var i = 0; i < prefix.length; i++) {
      if (this.indexOf(prefix[i]) == 0) return true;
    }
  } else return this.indexOf(prefix) == 0;

  return false;
};

String.prototype.strip = function () {
  return this.trim();
};

String.prototype.upper = function () {
  return this.toUpperCase();
};

String.prototype.__mul__ = function (scalar) {
  var result = '';

  for (var i = 0; i < scalar; i++) {
    result = result + this;
  }

  return result;
};

String.prototype.__rmul__ = String.prototype.__mul__;

function __contains__(element) {
  return this.hasOwnProperty(element);
}

function __keys__() {
  var keys = [];

  for (var attrib in this) {
    if (!__specialattrib__(attrib)) {
      keys.push(attrib);
    }
  }

  return keys;
}

function __items__() {
  var items = [];

  for (var attrib in this) {
    if (!__specialattrib__(attrib)) {
      items.push([attrib, this[attrib]]);
    }
  }

  return items;
}

function __del__(key) {
  delete this[key];
}

function __clear__() {
  for (var attrib in this) {
    delete this[attrib];
  }
}

function __getdefault__(aKey, aDefault) {
  var result = this[aKey];

  if (result == undefined) {
    result = this['py_' + aKey];
  }

  return result == undefined ? aDefault == undefined ? null : aDefault : result;
}

function __setdefault__(aKey, aDefault) {
  var result = this[aKey];

  if (result != undefined) {
    return result;
  }

  var val = aDefault == undefined ? null : aDefault;
  this[aKey] = val;
  return val;
}

function __pop__(aKey, aDefault) {
  var result = this[aKey];

  if (result != undefined) {
    delete this[aKey];
    return result;
  } else {
    if (aDefault === undefined) {
      throw KeyError(aKey, new Error());
    }
  }

  return aDefault;
}

function __popitem__() {
  var aKey = Object.keys(this)[0];

  if (aKey == null) {
    throw KeyError("popitem(): dictionary is empty", new Error());
  }

  var result = tuple([aKey, this[aKey]]);
  delete this[aKey];
  return result;
}

function __update__(aDict) {
  for (var aKey in aDict) {
    this[aKey] = aDict[aKey];
  }
}

function __values__() {
  var values = [];

  for (var attrib in this) {
    if (!__specialattrib__(attrib)) {
      values.push(this[attrib]);
    }
  }

  return values;
}

function __dgetitem__(aKey) {
  return this[aKey];
}

function __dsetitem__(aKey, aValue) {
  this[aKey] = aValue;
}

function dict(objectOrPairs) {
  var instance = {};

  if (!objectOrPairs || objectOrPairs instanceof Array) {
    if (objectOrPairs) {
      for (var index = 0; index < objectOrPairs.length; index++) {
        var pair = objectOrPairs[index];

        if (!(pair instanceof Array) || pair.length != 2) {
          throw ValueError("dict update sequence element #" + index + " has length " + pair.length + "; 2 is required", new Error());
        }

        var key = pair[0];
        var val = pair[1];

        if (!(objectOrPairs instanceof Array) && objectOrPairs instanceof Object) {
          if (!isinstance(objectOrPairs, dict)) {
            val = dict(val);
          }
        }

        instance[key] = val;
      }
    }
  } else {
    if (isinstance(objectOrPairs, dict)) {
      var aKeys = objectOrPairs.py_keys();

      for (var index = 0; index < aKeys.length; index++) {
        var key = aKeys[index];
        instance[key] = objectOrPairs[key];
      }
    } else if (objectOrPairs instanceof Object) {
      instance = objectOrPairs;
    } else {
      throw ValueError("Invalid type of object for dict creation", new Error());
    }
  }

  __setproperty__(instance, '__class__', {
    value: dict,
    enumerable: false,
    writable: true
  });

  __setproperty__(instance, '__contains__', {
    value: __contains__,
    enumerable: false
  });

  __setproperty__(instance, 'py_keys', {
    value: __keys__,
    enumerable: false
  });

  __setproperty__(instance, '__iter__', {
    value: function value() {
      new __PyIterator__(this.py_keys());
    },
    enumerable: false
  });

  __setproperty__(instance, Symbol.iterator, {
    value: function value() {
      new __JsIterator__(this.py_keys());
    },
    enumerable: false
  });

  __setproperty__(instance, 'py_items', {
    value: __items__,
    enumerable: false
  });

  __setproperty__(instance, 'py_del', {
    value: __del__,
    enumerable: false
  });

  __setproperty__(instance, 'py_clear', {
    value: __clear__,
    enumerable: false
  });

  __setproperty__(instance, 'py_get', {
    value: __getdefault__,
    enumerable: false
  });

  __setproperty__(instance, 'py_setdefault', {
    value: __setdefault__,
    enumerable: false
  });

  __setproperty__(instance, 'py_pop', {
    value: __pop__,
    enumerable: false
  });

  __setproperty__(instance, 'py_popitem', {
    value: __popitem__,
    enumerable: false
  });

  __setproperty__(instance, 'py_update', {
    value: __update__,
    enumerable: false
  });

  __setproperty__(instance, 'py_values', {
    value: __values__,
    enumerable: false
  });

  __setproperty__(instance, '__getitem__', {
    value: __dgetitem__,
    enumerable: false
  });

  __setproperty__(instance, '__setitem__', {
    value: __dsetitem__,
    enumerable: false
  });

  return instance;
}

dict.__name__ = 'dict';
dict.__bases__ = [object];

function __setdoc__(docString) {
  this.__doc__ = docString;
  return this;
}

__setproperty__(Function.prototype, '__setdoc__', {
  value: __setdoc__,
  enumerable: false
});

function __jsmod__(a, b) {
  if (_typeof(a) == 'object' && '__mod__' in a) {
    return a.__mod__(b);
  } else if (_typeof(b) == 'object' && '__rmod__' in b) {
    return b.__rmod__(a);
  } else {
    return a % b;
  }
}

;

function __mod__(a, b) {
  if (_typeof(a) == 'object' && '__mod__' in a) {
    return a.__mod__(b);
  } else if (_typeof(b) == 'object' && '__rmod__' in b) {
    return b.__rmod__(a);
  } else {
    return (a % b + b) % b;
  }
}

;

function __pow__(a, b) {
  if (_typeof(a) == 'object' && '__pow__' in a) {
    return a.__pow__(b);
  } else if (_typeof(b) == 'object' && '__rpow__' in b) {
    return b.__rpow__(a);
  } else {
    return Math.pow(a, b);
  }
}

;
var pow = __pow__;
exports.pow = pow;

function __neg__(a) {
  if (_typeof(a) == 'object' && '__neg__' in a) {
    return a.__neg__();
  } else {
    return -a;
  }
}

;

function __matmul__(a, b) {
  return a.__matmul__(b);
}

;

function __mul__(a, b) {
  if (_typeof(a) == 'object' && '__mul__' in a) {
    return a.__mul__(b);
  } else if (_typeof(b) == 'object' && '__rmul__' in b) {
    return b.__rmul__(a);
  } else if (typeof a == 'string') {
    return a.__mul__(b);
  } else if (typeof b == 'string') {
    return b.__rmul__(a);
  } else {
    return a * b;
  }
}

;

function __truediv__(a, b) {
  if (_typeof(a) == 'object' && '__truediv__' in a) {
    return a.__truediv__(b);
  } else if (_typeof(b) == 'object' && '__rtruediv__' in b) {
    return b.__rtruediv__(a);
  } else if (_typeof(a) == 'object' && '__div__' in a) {
    return a.__div__(b);
  } else if (_typeof(b) == 'object' && '__rdiv__' in b) {
    return b.__rdiv__(a);
  } else {
    return a / b;
  }
}

;

function __floordiv__(a, b) {
  if (_typeof(a) == 'object' && '__floordiv__' in a) {
    return a.__floordiv__(b);
  } else if (_typeof(b) == 'object' && '__rfloordiv__' in b) {
    return b.__rfloordiv__(a);
  } else if (_typeof(a) == 'object' && '__div__' in a) {
    return a.__div__(b);
  } else if (_typeof(b) == 'object' && '__rdiv__' in b) {
    return b.__rdiv__(a);
  } else {
    return Math.floor(a / b);
  }
}

;

function __add__(a, b) {
  if (_typeof(a) == 'object' && '__add__' in a) {
    return a.__add__(b);
  } else if (_typeof(b) == 'object' && '__radd__' in b) {
    return b.__radd__(a);
  } else {
    return a + b;
  }
}

;

function __sub__(a, b) {
  if (_typeof(a) == 'object' && '__sub__' in a) {
    return a.__sub__(b);
  } else if (_typeof(b) == 'object' && '__rsub__' in b) {
    return b.__rsub__(a);
  } else {
    return a - b;
  }
}

;

function __lshift__(a, b) {
  if (_typeof(a) == 'object' && '__lshift__' in a) {
    return a.__lshift__(b);
  } else if (_typeof(b) == 'object' && '__rlshift__' in b) {
    return b.__rlshift__(a);
  } else {
    return a << b;
  }
}

;

function __rshift__(a, b) {
  if (_typeof(a) == 'object' && '__rshift__' in a) {
    return a.__rshift__(b);
  } else if (_typeof(b) == 'object' && '__rrshift__' in b) {
    return b.__rrshift__(a);
  } else {
    return a >> b;
  }
}

;

function __or__(a, b) {
  if (_typeof(a) == 'object' && '__or__' in a) {
    return a.__or__(b);
  } else if (_typeof(b) == 'object' && '__ror__' in b) {
    return b.__ror__(a);
  } else {
    return a | b;
  }
}

;

function __xor__(a, b) {
  if (_typeof(a) == 'object' && '__xor__' in a) {
    return a.__xor__(b);
  } else if (_typeof(b) == 'object' && '__rxor__' in b) {
    return b.__rxor__(a);
  } else {
    return a ^ b;
  }
}

;

function __and__(a, b) {
  if (_typeof(a) == 'object' && '__and__' in a) {
    return a.__and__(b);
  } else if (_typeof(b) == 'object' && '__rand__' in b) {
    return b.__rand__(a);
  } else {
    return a & b;
  }
}

;

function __eq__(a, b) {
  if (_typeof(a) == 'object' && '__eq__' in a) {
    return a.__eq__(b);
  } else {
    return a == b;
  }
}

;

function __ne__(a, b) {
  if (_typeof(a) == 'object' && '__ne__' in a) {
    return a.__ne__(b);
  } else {
    return a != b;
  }
}

;

function __lt__(a, b) {
  if (_typeof(a) == 'object' && '__lt__' in a) {
    return a.__lt__(b);
  } else {
    return a < b;
  }
}

;

function __le__(a, b) {
  if (_typeof(a) == 'object' && '__le__' in a) {
    return a.__le__(b);
  } else {
    return a <= b;
  }
}

;

function __gt__(a, b) {
  if (_typeof(a) == 'object' && '__gt__' in a) {
    return a.__gt__(b);
  } else {
    return a > b;
  }
}

;

function __ge__(a, b) {
  if (_typeof(a) == 'object' && '__ge__' in a) {
    return a.__ge__(b);
  } else {
    return a >= b;
  }
}

;

function __imatmul__(a, b) {
  if ('__imatmul__' in a) {
    return a.__imatmul__(b);
  } else {
    return a.__matmul__(b);
  }
}

;

function __ipow__(a, b) {
  if (_typeof(a) == 'object' && '__pow__' in a) {
    return a.__ipow__(b);
  } else if (_typeof(a) == 'object' && '__ipow__' in a) {
    return a.__pow__(b);
  } else if (_typeof(b) == 'object' && '__rpow__' in b) {
    return b.__rpow__(a);
  } else {
    return Math.pow(a, b);
  }
}

;

function __ijsmod__(a, b) {
  if (_typeof(a) == 'object' && '__imod__' in a) {
    return a.__ismod__(b);
  } else if (_typeof(a) == 'object' && '__mod__' in a) {
    return a.__mod__(b);
  } else if (_typeof(b) == 'object' && '__rpow__' in b) {
    return b.__rmod__(a);
  } else {
    return a % b;
  }
}

;

function __imod__(a, b) {
  if (_typeof(a) == 'object' && '__imod__' in a) {
    return a.__imod__(b);
  } else if (_typeof(a) == 'object' && '__mod__' in a) {
    return a.__mod__(b);
  } else if (_typeof(b) == 'object' && '__rmod__' in b) {
    return b.__rmod__(a);
  } else {
    return (a % b + b) % b;
  }
}

;

function __imul__(a, b) {
  if (_typeof(a) == 'object' && '__imul__' in a) {
    return a.__imul__(b);
  } else if (_typeof(a) == 'object' && '__mul__' in a) {
    return a = a.__mul__(b);
  } else if (_typeof(b) == 'object' && '__rmul__' in b) {
    return a = b.__rmul__(a);
  } else if (typeof a == 'string') {
    return a = a.__mul__(b);
  } else if (typeof b == 'string') {
    return a = b.__rmul__(a);
  } else {
    return a *= b;
  }
}

;

function __idiv__(a, b) {
  if (_typeof(a) == 'object' && '__idiv__' in a) {
    return a.__idiv__(b);
  } else if (_typeof(a) == 'object' && '__div__' in a) {
    return a = a.__div__(b);
  } else if (_typeof(b) == 'object' && '__rdiv__' in b) {
    return a = b.__rdiv__(a);
  } else {
    return a /= b;
  }
}

;

function __iadd__(a, b) {
  if (_typeof(a) == 'object' && '__iadd__' in a) {
    return a.__iadd__(b);
  } else if (_typeof(a) == 'object' && '__add__' in a) {
    return a = a.__add__(b);
  } else if (_typeof(b) == 'object' && '__radd__' in b) {
    return a = b.__radd__(a);
  } else {
    return a += b;
  }
}

;

function __isub__(a, b) {
  if (_typeof(a) == 'object' && '__isub__' in a) {
    return a.__isub__(b);
  } else if (_typeof(a) == 'object' && '__sub__' in a) {
    return a = a.__sub__(b);
  } else if (_typeof(b) == 'object' && '__rsub__' in b) {
    return a = b.__rsub__(a);
  } else {
    return a -= b;
  }
}

;

function __ilshift__(a, b) {
  if (_typeof(a) == 'object' && '__ilshift__' in a) {
    return a.__ilshift__(b);
  } else if (_typeof(a) == 'object' && '__lshift__' in a) {
    return a = a.__lshift__(b);
  } else if (_typeof(b) == 'object' && '__rlshift__' in b) {
    return a = b.__rlshift__(a);
  } else {
    return a <<= b;
  }
}

;

function __irshift__(a, b) {
  if (_typeof(a) == 'object' && '__irshift__' in a) {
    return a.__irshift__(b);
  } else if (_typeof(a) == 'object' && '__rshift__' in a) {
    return a = a.__rshift__(b);
  } else if (_typeof(b) == 'object' && '__rrshift__' in b) {
    return a = b.__rrshift__(a);
  } else {
    return a >>= b;
  }
}

;

function __ior__(a, b) {
  if (_typeof(a) == 'object' && '__ior__' in a) {
    return a.__ior__(b);
  } else if (_typeof(a) == 'object' && '__or__' in a) {
    return a = a.__or__(b);
  } else if (_typeof(b) == 'object' && '__ror__' in b) {
    return a = b.__ror__(a);
  } else {
    return a |= b;
  }
}

;

function __ixor__(a, b) {
  if (_typeof(a) == 'object' && '__ixor__' in a) {
    return a.__ixor__(b);
  } else if (_typeof(a) == 'object' && '__xor__' in a) {
    return a = a.__xor__(b);
  } else if (_typeof(b) == 'object' && '__rxor__' in b) {
    return a = b.__rxor__(a);
  } else {
    return a ^= b;
  }
}

;

function __iand__(a, b) {
  if (_typeof(a) == 'object' && '__iand__' in a) {
    return a.__iand__(b);
  } else if (_typeof(a) == 'object' && '__and__' in a) {
    return a = a.__and__(b);
  } else if (_typeof(b) == 'object' && '__rand__' in b) {
    return a = b.__rand__(a);
  } else {
    return a &= b;
  }
}

;

function __getitem__(container, key) {
  if (_typeof(container) == 'object' && '__getitem__' in container) {
    return container.__getitem__(key);
  } else if ((typeof container == 'string' || container instanceof Array) && key < 0) {
    return container[container.length + key];
  } else {
    return container[key];
  }
}

;

function __setitem__(container, key, value) {
  if (_typeof(container) == 'object' && '__setitem__' in container) {
    container.__setitem__(key, value);
  } else if ((typeof container == 'string' || container instanceof Array) && key < 0) {
    container[container.length + key] = value;
  } else {
    container[key] = value;
  }
}

;

function __getslice__(container, lower, upper, step) {
  if (_typeof(container) == 'object' && '__getitem__' in container) {
    return container.__getitem__([lower, upper, step]);
  } else {
    return container.__getslice__(lower, upper, step);
  }
}

;

function __setslice__(container, lower, upper, step, value) {
  if (_typeof(container) == 'object' && '__setitem__' in container) {
    container.__setitem__([lower, upper, step], value);
  } else {
    container.__setslice__(lower, upper, step, value);
  }
}

;

var BaseException = __class__('BaseException', [object], {
  __module__: __name__
});

exports.BaseException = BaseException;

var Exception = __class__('Exception', [BaseException], {
  __module__: __name__,

  get __init__() {
    return __get__(this, function (self) {
      var kwargs = dict();

      if (arguments.length) {
        var __ilastarg0__ = arguments.length - 1;

        if (arguments[__ilastarg0__] && arguments[__ilastarg0__].hasOwnProperty("__kwargtrans__")) {
          var __allkwargs0__ = arguments[__ilastarg0__--];

          for (var __attrib0__ in __allkwargs0__) {
            switch (__attrib0__) {
              case 'self':
                var self = __allkwargs0__[__attrib0__];
                break;

              default:
                kwargs[__attrib0__] = __allkwargs0__[__attrib0__];
            }
          }

          delete kwargs.__kwargtrans__;
        }

        var args = tuple([].slice.apply(arguments).slice(1, __ilastarg0__ + 1));
      } else {
        var args = tuple();
      }

      self.__args__ = args;

      try {
        self.stack = kwargs.error.stack;
      } catch (__except0__) {
        self.stack = 'No stack trace available';
      }
    });
  },

  get __repr__() {
    return __get__(this, function (self) {
      if (len(self.__args__) > 1) {
        return '{}{}'.format(self.__class__.__name__, repr(tuple(self.__args__)));
      } else if (len(self.__args__)) {
        return '{}({})'.format(self.__class__.__name__, repr(self.__args__[0]));
      } else {
        return '{}()'.format(self.__class__.__name__);
      }
    });
  },

  get __str__() {
    return __get__(this, function (self) {
      if (len(self.__args__) > 1) {
        return str(tuple(self.__args__));
      } else if (len(self.__args__)) {
        return str(self.__args__[0]);
      } else {
        return '';
      }
    });
  }

});

exports.Exception = Exception;

var IterableError = __class__('IterableError', [Exception], {
  __module__: __name__,

  get __init__() {
    return __get__(this, function (self, error) {
      Exception.__init__(self, "Can't iterate over non-iterable", __kwargtrans__({
        error: error
      }));
    });
  }

});

exports.IterableError = IterableError;

var StopIteration = __class__('StopIteration', [Exception], {
  __module__: __name__,

  get __init__() {
    return __get__(this, function (self, error) {
      Exception.__init__(self, 'Iterator exhausted', __kwargtrans__({
        error: error
      }));
    });
  }

});

exports.StopIteration = StopIteration;

var ValueError = __class__('ValueError', [Exception], {
  __module__: __name__,

  get __init__() {
    return __get__(this, function (self, message, error) {
      Exception.__init__(self, message, __kwargtrans__({
        error: error
      }));
    });
  }

});

exports.ValueError = ValueError;

var KeyError = __class__('KeyError', [Exception], {
  __module__: __name__,

  get __init__() {
    return __get__(this, function (self, message, error) {
      Exception.__init__(self, message, __kwargtrans__({
        error: error
      }));
    });
  }

});

exports.KeyError = KeyError;

var AssertionError = __class__('AssertionError', [Exception], {
  __module__: __name__,

  get __init__() {
    return __get__(this, function (self, message, error) {
      if (message) {
        Exception.__init__(self, message, __kwargtrans__({
          error: error
        }));
      } else {
        Exception.__init__(self, __kwargtrans__({
          error: error
        }));
      }
    });
  }

});

exports.AssertionError = AssertionError;

var NotImplementedError = __class__('NotImplementedError', [Exception], {
  __module__: __name__,

  get __init__() {
    return __get__(this, function (self, message, error) {
      Exception.__init__(self, message, __kwargtrans__({
        error: error
      }));
    });
  }

});

exports.NotImplementedError = NotImplementedError;

var IndexError = __class__('IndexError', [Exception], {
  __module__: __name__,

  get __init__() {
    return __get__(this, function (self, message, error) {
      Exception.__init__(self, message, __kwargtrans__({
        error: error
      }));
    });
  }

});

exports.IndexError = IndexError;

var AttributeError = __class__('AttributeError', [Exception], {
  __module__: __name__,

  get __init__() {
    return __get__(this, function (self, message, error) {
      Exception.__init__(self, message, __kwargtrans__({
        error: error
      }));
    });
  }

});

exports.AttributeError = AttributeError;

var py_TypeError = __class__('py_TypeError', [Exception], {
  __module__: __name__,

  get __init__() {
    return __get__(this, function (self, message, error) {
      Exception.__init__(self, message, __kwargtrans__({
        error: error
      }));
    });
  }

});

exports.py_TypeError = py_TypeError;

var Warning = __class__('Warning', [Exception], {
  __module__: __name__
});

exports.Warning = Warning;

var UserWarning = __class__('UserWarning', [Warning], {
  __module__: __name__
});

exports.UserWarning = UserWarning;

var DeprecationWarning = __class__('DeprecationWarning', [Warning], {
  __module__: __name__
});

exports.DeprecationWarning = DeprecationWarning;

var RuntimeWarning = __class__('RuntimeWarning', [Warning], {
  __module__: __name__
});

exports.RuntimeWarning = RuntimeWarning;

var __sort__ = function __sort__(iterable, key, reverse) {
  if (typeof key == 'undefined' || key != null && key.hasOwnProperty("__kwargtrans__")) {
    ;
    var key = null;
  }

  ;

  if (typeof reverse == 'undefined' || reverse != null && reverse.hasOwnProperty("__kwargtrans__")) {
    ;
    var reverse = false;
  }

  ;

  if (arguments.length) {
    var __ilastarg0__ = arguments.length - 1;

    if (arguments[__ilastarg0__] && arguments[__ilastarg0__].hasOwnProperty("__kwargtrans__")) {
      var __allkwargs0__ = arguments[__ilastarg0__--];

      for (var __attrib0__ in __allkwargs0__) {
        switch (__attrib0__) {
          case 'iterable':
            var iterable = __allkwargs0__[__attrib0__];
            break;

          case 'key':
            var key = __allkwargs0__[__attrib0__];
            break;

          case 'reverse':
            var reverse = __allkwargs0__[__attrib0__];
            break;
        }
      }
    }
  } else {}

  if (key) {
    iterable.sort(function __lambda__(a, b) {
      if (arguments.length) {
        var __ilastarg0__ = arguments.length - 1;

        if (arguments[__ilastarg0__] && arguments[__ilastarg0__].hasOwnProperty("__kwargtrans__")) {
          var __allkwargs0__ = arguments[__ilastarg0__--];

          for (var __attrib0__ in __allkwargs0__) {
            switch (__attrib0__) {
              case 'a':
                var a = __allkwargs0__[__attrib0__];
                break;

              case 'b':
                var b = __allkwargs0__[__attrib0__];
                break;
            }
          }
        }
      } else {}

      return key(a) > key(b) ? 1 : -1;
    });
  } else {
    iterable.sort();
  }

  if (reverse) {
    iterable.reverse();
  }
};

exports.__sort__ = __sort__;

var sorted = function sorted(iterable, key, reverse) {
  if (typeof key == 'undefined' || key != null && key.hasOwnProperty("__kwargtrans__")) {
    ;
    var key = null;
  }

  ;

  if (typeof reverse == 'undefined' || reverse != null && reverse.hasOwnProperty("__kwargtrans__")) {
    ;
    var reverse = false;
  }

  ;

  if (arguments.length) {
    var __ilastarg0__ = arguments.length - 1;

    if (arguments[__ilastarg0__] && arguments[__ilastarg0__].hasOwnProperty("__kwargtrans__")) {
      var __allkwargs0__ = arguments[__ilastarg0__--];

      for (var __attrib0__ in __allkwargs0__) {
        switch (__attrib0__) {
          case 'iterable':
            var iterable = __allkwargs0__[__attrib0__];
            break;

          case 'key':
            var key = __allkwargs0__[__attrib0__];
            break;

          case 'reverse':
            var reverse = __allkwargs0__[__attrib0__];
            break;
        }
      }
    }
  } else {}

  if (py_typeof(iterable) == dict) {
    var result = copy(iterable.py_keys());
  } else {
    var result = copy(iterable);
  }

  __sort__(result, key, reverse);

  return result;
};

exports.sorted = sorted;

var map = function map(func, iterable) {
  return function () {
    var __accu0__ = [];

    var _iterator11 = _createForOfIteratorHelper(iterable),
        _step11;

    try {
      for (_iterator11.s(); !(_step11 = _iterator11.n()).done;) {
        var item = _step11.value;

        __accu0__.append(func(item));
      }
    } catch (err) {
      _iterator11.e(err);
    } finally {
      _iterator11.f();
    }

    return __accu0__;
  }();
};

exports.map = map;

var filter = function filter(func, iterable) {
  if (func == null) {
    var func = bool;
  }

  return function () {
    var __accu0__ = [];

    var _iterator12 = _createForOfIteratorHelper(iterable),
        _step12;

    try {
      for (_iterator12.s(); !(_step12 = _iterator12.n()).done;) {
        var item = _step12.value;

        if (func(item)) {
          __accu0__.append(item);
        }
      }
    } catch (err) {
      _iterator12.e(err);
    } finally {
      _iterator12.f();
    }

    return __accu0__;
  }();
};

exports.filter = filter;

var divmod = function divmod(n, d) {
  return tuple([Math.floor(n / d), __mod__(n, d)]);
};

exports.divmod = divmod;

var __Terminal__ = __class__('__Terminal__', [object], {
  __module__: __name__,

  get __init__() {
    return __get__(this, function (self) {
      self.buffer = '';

      try {
        self.element = document.getElementById('__terminal__');
      } catch (__except0__) {
        self.element = null;
      }

      if (self.element) {
        self.element.style.overflowX = 'auto';
        self.element.style.boxSizing = 'border-box';
        self.element.style.padding = '5px';
        self.element.innerHTML = '_';
      }
    });
  },

  get print() {
    return __get__(this, function (self) {
      var sep = ' ';
      var end = '\n';

      if (arguments.length) {
        var __ilastarg0__ = arguments.length - 1;

        if (arguments[__ilastarg0__] && arguments[__ilastarg0__].hasOwnProperty("__kwargtrans__")) {
          var __allkwargs0__ = arguments[__ilastarg0__--];

          for (var __attrib0__ in __allkwargs0__) {
            switch (__attrib0__) {
              case 'self':
                var self = __allkwargs0__[__attrib0__];
                break;

              case 'sep':
                var sep = __allkwargs0__[__attrib0__];
                break;

              case 'end':
                var end = __allkwargs0__[__attrib0__];
                break;
            }
          }
        }

        var args = tuple([].slice.apply(arguments).slice(1, __ilastarg0__ + 1));
      } else {
        var args = tuple();
      }

      self.buffer = '{}{}{}'.format(self.buffer, sep.join(function () {
        var __accu0__ = [];

        var _iterator13 = _createForOfIteratorHelper(args),
            _step13;

        try {
          for (_iterator13.s(); !(_step13 = _iterator13.n()).done;) {
            var arg = _step13.value;

            __accu0__.append(str(arg));
          }
        } catch (err) {
          _iterator13.e(err);
        } finally {
          _iterator13.f();
        }

        return __accu0__;
      }()), end).__getslice__(-4096, null, 1);

      if (self.element) {
        self.element.innerHTML = self.buffer.py_replace('\n', '<br>').py_replace(' ', '&nbsp');
        self.element.scrollTop = self.element.scrollHeight;
      } else {
        console.log(sep.join(function () {
          var __accu0__ = [];

          var _iterator14 = _createForOfIteratorHelper(args),
              _step14;

          try {
            for (_iterator14.s(); !(_step14 = _iterator14.n()).done;) {
              var arg = _step14.value;

              __accu0__.append(str(arg));
            }
          } catch (err) {
            _iterator14.e(err);
          } finally {
            _iterator14.f();
          }

          return __accu0__;
        }()));
      }
    });
  },

  get input() {
    return __get__(this, function (self, question) {
      if (arguments.length) {
        var __ilastarg0__ = arguments.length - 1;

        if (arguments[__ilastarg0__] && arguments[__ilastarg0__].hasOwnProperty("__kwargtrans__")) {
          var __allkwargs0__ = arguments[__ilastarg0__--];

          for (var __attrib0__ in __allkwargs0__) {
            switch (__attrib0__) {
              case 'self':
                var self = __allkwargs0__[__attrib0__];
                break;

              case 'question':
                var question = __allkwargs0__[__attrib0__];
                break;
            }
          }
        }
      } else {}

      self.print('{}'.format(question), __kwargtrans__({
        end: ''
      }));
      var answer = window.prompt('\n'.join(self.buffer.py_split('\n').__getslice__(-8, null, 1)));
      self.print(answer);
      return answer;
    });
  }

});

exports.__Terminal__ = __Terminal__;

var __terminal__ = __Terminal__();

exports.__terminal__ = __terminal__;
var print = __terminal__.print;
exports.print = print;
var input = __terminal__.input;
exports.input = input;

/***/ }),

/***/ "./lib/jupyter/plugin.js":
/*!*******************************!*\
  !*** ./lib/jupyter/plugin.js ***!
  \*******************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";


function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }

Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.notebookIcon = exports["default"] = exports.contextToMetannoManagerRegistry = exports.MetannoArea = void 0;
exports.registerMetannoManager = registerMetannoManager;

__webpack_require__(/*! regenerator-runtime/runtime */ "./node_modules/regenerator-runtime/runtime.js");

var _algorithm = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");

var _properties = __webpack_require__(/*! @lumino/properties */ "webpack/sharing/consume/default/@lumino/properties");

var _disposable = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");

var _services = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");

var _docmanager = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");

var _mainmenu = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");

var _logconsole = __webpack_require__(/*! @jupyterlab/logconsole */ "webpack/sharing/consume/default/@jupyterlab/logconsole");

var _rendermime = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");

var _apputils = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");

var _notebook = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");

var _settingregistry = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");

var _application = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");

var _uiComponents = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");

var _widgets = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");

var _coreutils = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");

var _manager = _interopRequireDefault(__webpack_require__(/*! ./manager */ "./lib/jupyter/manager.js"));

var _renderer = _interopRequireDefault(__webpack_require__(/*! ./renderer */ "./lib/jupyter/renderer.js"));

var _icon = _interopRequireDefault(__webpack_require__(/*! ../icon.svg */ "./lib/icon.svg"));

__webpack_require__(/*! ./dontDisplayHiddenOutput */ "./lib/jupyter/dontDisplayHiddenOutput.js");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { Promise.resolve(value).then(_next, _throw); } }

function _asyncToGenerator(fn) { return function () { var self = this, args = arguments; return new Promise(function (resolve, reject) { var gen = fn.apply(self, args); function _next(value) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value); } function _throw(err) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err); } _next(undefined); }); }; }

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); enumerableOnly && (symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; })), keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = null != arguments[i] ? arguments[i] : {}; i % 2 ? ownKeys(Object(source), !0).forEach(function (key) { _defineProperty(target, key, source[key]); }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)) : ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } return target; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); Object.defineProperty(Constructor, "prototype", { writable: false }); return Constructor; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); Object.defineProperty(subClass, "prototype", { writable: false }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }

function _createSuper(Derived) { var hasNativeReflectConstruct = _isNativeReflectConstruct(); return function _createSuperInternal() { var Super = _getPrototypeOf(Derived), result; if (hasNativeReflectConstruct) { var NewTarget = _getPrototypeOf(this).constructor; result = Reflect.construct(Super, arguments, NewTarget); } else { result = Super.apply(this, arguments); } return _possibleConstructorReturn(this, result); }; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } else if (call !== void 0) { throw new TypeError("Derived constructors may only return object or undefined"); } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _isNativeReflectConstruct() { if (typeof Reflect === "undefined" || !Reflect.construct) return false; if (Reflect.construct.sham) return false; if (typeof Proxy === "function") return true; try { Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function () {})); return true; } catch (e) { return false; } }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

var _marked = /*#__PURE__*/regeneratorRuntime.mark(getEditorsFromNotebook),
    _marked2 = /*#__PURE__*/regeneratorRuntime.mark(chain),
    _marked3 = /*#__PURE__*/regeneratorRuntime.mark(getLinkedEditorsFromApp);

function _createForOfIteratorHelper(o, allowArrayLike) { var it = typeof Symbol !== "undefined" && o[Symbol.iterator] || o["@@iterator"]; if (!it) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = it.call(o); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

var MIMETYPE = 'application/vnd.jupyter.annotator+json';
var notebookIcon = new _uiComponents.LabIcon({
  name: 'ui-components:metanno',
  svgstr: _icon.default
});
exports.notebookIcon = notebookIcon;
var contextToMetannoManagerRegistry = new _properties.AttachedProperty({
  name: 'widgetManager',
  create: function create() {
    return undefined;
  }
});
exports.contextToMetannoManagerRegistry = contextToMetannoManagerRegistry;
var SETTINGS = {
  saveState: false
};
/**
 * Iterate through all widget renderers in a notebook.
 */

function getEditorsFromNotebook(notebook) {
  var _iterator, _step, cell, _iterator2, _step2, codecell, _iterator3, _step3, output;

  return regeneratorRuntime.wrap(function getEditorsFromNotebook$(_context) {
    while (1) {
      switch (_context.prev = _context.next) {
        case 0:
          // @ts-ignore
          _iterator = _createForOfIteratorHelper(notebook.widgets);
          _context.prev = 1;

          _iterator.s();

        case 3:
          if ((_step = _iterator.n()).done) {
            _context.next = 41;
            break;
          }

          cell = _step.value;

          if (!(cell.model.type === 'code')) {
            _context.next = 39;
            break;
          }

          _iterator2 = _createForOfIteratorHelper(cell.outputArea.widgets);
          _context.prev = 7;

          _iterator2.s();

        case 9:
          if ((_step2 = _iterator2.n()).done) {
            _context.next = 31;
            break;
          }

          codecell = _step2.value;
          _iterator3 = _createForOfIteratorHelper((0, _algorithm.toArray)(codecell.children()));
          _context.prev = 12;

          _iterator3.s();

        case 14:
          if ((_step3 = _iterator3.n()).done) {
            _context.next = 21;
            break;
          }

          output = _step3.value;

          if (!(output instanceof _renderer.default)) {
            _context.next = 19;
            break;
          }

          _context.next = 19;
          return output;

        case 19:
          _context.next = 14;
          break;

        case 21:
          _context.next = 26;
          break;

        case 23:
          _context.prev = 23;
          _context.t0 = _context["catch"](12);

          _iterator3.e(_context.t0);

        case 26:
          _context.prev = 26;

          _iterator3.f();

          return _context.finish(26);

        case 29:
          _context.next = 9;
          break;

        case 31:
          _context.next = 36;
          break;

        case 33:
          _context.prev = 33;
          _context.t1 = _context["catch"](7);

          _iterator2.e(_context.t1);

        case 36:
          _context.prev = 36;

          _iterator2.f();

          return _context.finish(36);

        case 39:
          _context.next = 3;
          break;

        case 41:
          _context.next = 46;
          break;

        case 43:
          _context.prev = 43;
          _context.t2 = _context["catch"](1);

          _iterator.e(_context.t2);

        case 46:
          _context.prev = 46;

          _iterator.f();

          return _context.finish(46);

        case 49:
        case "end":
          return _context.stop();
      }
    }
  }, _marked, null, [[1, 43, 46, 49], [7, 33, 36, 39], [12, 23, 26, 29]]);
}

function chain() {
  var _len,
      args,
      _key,
      _i,
      _args2,
      it,
      _args3 = arguments;

  return regeneratorRuntime.wrap(function chain$(_context2) {
    while (1) {
      switch (_context2.prev = _context2.next) {
        case 0:
          for (_len = _args3.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
            args[_key] = _args3[_key];
          }

          _i = 0, _args2 = args;

        case 2:
          if (!(_i < _args2.length)) {
            _context2.next = 8;
            break;
          }

          it = _args2[_i];
          return _context2.delegateYield(it, "t0", 5);

        case 5:
          _i++;
          _context2.next = 2;
          break;

        case 8:
        case "end":
          return _context2.stop();
      }
    }
  }, _marked2);
}
/**
 * Iterate through all matching linked output views
 */


function getLinkedEditorsFromApp(jupyterApp, path) {
  var linkedViews, _iterator4, _step4, view, _iterator5, _step5, outputs, _iterator6, _step6, output;

  return regeneratorRuntime.wrap(function getLinkedEditorsFromApp$(_context3) {
    while (1) {
      switch (_context3.prev = _context3.next) {
        case 0:
          linkedViews = (0, _algorithm.filter)(jupyterApp.shell.widgets("main"), // @ts-ignore
          function (w) {
            return w.id.startsWith('LinkedOutputView-') && w.path === path;
          });
          _iterator4 = _createForOfIteratorHelper((0, _algorithm.toArray)(linkedViews));
          _context3.prev = 2;

          _iterator4.s();

        case 4:
          if ((_step4 = _iterator4.n()).done) {
            _context3.next = 41;
            break;
          }

          view = _step4.value;
          _iterator5 = _createForOfIteratorHelper((0, _algorithm.toArray)(view.children()));
          _context3.prev = 7;

          _iterator5.s();

        case 9:
          if ((_step5 = _iterator5.n()).done) {
            _context3.next = 31;
            break;
          }

          outputs = _step5.value;
          _iterator6 = _createForOfIteratorHelper((0, _algorithm.toArray)(outputs.children()));
          _context3.prev = 12;

          _iterator6.s();

        case 14:
          if ((_step6 = _iterator6.n()).done) {
            _context3.next = 21;
            break;
          }

          output = _step6.value;

          if (!(output instanceof _renderer.default)) {
            _context3.next = 19;
            break;
          }

          _context3.next = 19;
          return output;

        case 19:
          _context3.next = 14;
          break;

        case 21:
          _context3.next = 26;
          break;

        case 23:
          _context3.prev = 23;
          _context3.t0 = _context3["catch"](12);

          _iterator6.e(_context3.t0);

        case 26:
          _context3.prev = 26;

          _iterator6.f();

          return _context3.finish(26);

        case 29:
          _context3.next = 9;
          break;

        case 31:
          _context3.next = 36;
          break;

        case 33:
          _context3.prev = 33;
          _context3.t1 = _context3["catch"](7);

          _iterator5.e(_context3.t1);

        case 36:
          _context3.prev = 36;

          _iterator5.f();

          return _context3.finish(36);

        case 39:
          _context3.next = 4;
          break;

        case 41:
          _context3.next = 46;
          break;

        case 43:
          _context3.prev = 43;
          _context3.t2 = _context3["catch"](2);

          _iterator4.e(_context3.t2);

        case 46:
          _context3.prev = 46;

          _iterator4.f();

          return _context3.finish(46);

        case 49:
        case "end":
          return _context3.stop();
      }
    }
  }, _marked3, null, [[2, 43, 46, 49], [7, 33, 36, 39], [12, 23, 26, 29]]);
}
/**
 * A widget hosting a metanno area.
 */


var MetannoArea = /*#__PURE__*/function (_Panel) {
  _inherits(MetannoArea, _Panel);

  var _super = _createSuper(MetannoArea);

  function MetannoArea(options) {
    var _this;

    _classCallCheck(this, MetannoArea);

    _this = _super.call(this);

    _defineProperty(_assertThisInitialized(_this), "_notebook", void 0);

    _defineProperty(_assertThisInitialized(_this), "_editor_id", void 0);

    _defineProperty(_assertThisInitialized(_this), "_editor_type", void 0);

    _defineProperty(_assertThisInitialized(_this), "_path", void 0);

    _defineProperty(_assertThisInitialized(_this), "_cell", null);

    _this._notebook = options.notebook;
    _this._editor_id = options.editor_id;
    _this._editor_type = options.editor_type;
    _this._cell = options.cell || null;

    if (!_this._editor_id || !_this._editor_type) {
      var widget = _this._cell.outputArea.widgets[0].widgets[1];
      _this._editor_id = widget.editor_id;
      _this._editor_type = widget.editor_type;
    }

    _this.id = "MetannoArea-".concat(_coreutils.UUID.uuid4());
    _this.title.label = _this._editor_id;
    _this.title.icon = notebookIcon;
    _this.title.caption = _this._notebook.title.label ? "For Notebook: ".concat(_this._notebook.title.label || '') : '';

    _this.addClass('jp-LinkedOutputView'); // Wait for the notebook to be loaded before
    // cloning the output area.


    void _this._notebook.context.ready.then(function () {
      if (!(_this._editor_id && _this._editor_type)) {
        _this.dispose();

        return;
      }

      var widget = new _renderer.default({
        editor_id: _this._editor_id,
        editor_type: _this._editor_type
      }, contextToMetannoManagerRegistry.get(_this._notebook.context));
      widget.addClass("jp-OutputArea-output");

      _this.addWidget(widget);
    });
    return _this;
  }

  _createClass(MetannoArea, [{
    key: "editor_id",
    get: function get() {
      return this._editor_id;
    }
  }, {
    key: "editor_type",
    get: function get() {
      return this._editor_type;
    }
  }, {
    key: "path",
    get: function get() {
      var _this$_notebook, _this$_notebook$conte;

      return this === null || this === void 0 ? void 0 : (_this$_notebook = this._notebook) === null || _this$_notebook === void 0 ? void 0 : (_this$_notebook$conte = _this$_notebook.context) === null || _this$_notebook$conte === void 0 ? void 0 : _this$_notebook$conte._path;
    }
  }]);

  return MetannoArea;
}(_widgets.Panel);
/*
Here we add the singleton MetannoManager to the given editor (context)
 */


exports.MetannoArea = MetannoArea;

function registerMetannoManager(context, rendermime, renderers) {
  var wManager = contextToMetannoManagerRegistry.get(context);

  if (!wManager) {
    wManager = new _manager.default(context, SETTINGS);
    contextToMetannoManagerRegistry.set(context, wManager);
  }

  var _iterator7 = _createForOfIteratorHelper(renderers),
      _step7;

  try {
    for (_iterator7.s(); !(_step7 = _iterator7.n()).done;) {
      var r = _step7.value;
      r.manager = wManager;
    } // Replace the placeholder widget renderer with one bound to this widget
    // manager.

  } catch (err) {
    _iterator7.e(err);
  } finally {
    _iterator7.f();
  }

  rendermime.removeMimeType(MIMETYPE);
  rendermime.addFactory({
    safe: true,
    mimeTypes: [MIMETYPE],
    createRenderer: function createRenderer(options) {
      return new _renderer.default(options, wManager);
    }
  }, 0);
  return new _disposable.DisposableDelegate(function () {
    if (rendermime) {
      rendermime.removeMimeType(MIMETYPE);
    }

    wManager.dispose();
  });
}
/*
Activate the extension:
-
 */


function activateMetannoExtension(app, rendermime, docManager, notebookTracker, settingRegistry, menu, loggerRegistry, restorer //palette: ICommandPalette,
) {
  var commands = app.commands,
      shell = app.shell,
      contextMenu = app.contextMenu;
  var metannoAreas = new _apputils.WidgetTracker({
    namespace: 'metanno-areas'
  });

  if (restorer) {
    restorer.restore(metannoAreas, {
      command: 'metanno:create-view',
      args: function args(widget) {
        return {
          editor_id: widget.content.editor_id,
          editor_type: widget.content.editor_type,
          path: widget.content.path
        };
      },
      name: function name(widget) {
        return "".concat(widget.content.path, ":").concat(widget.content.editor_type, ":").concat(widget.content.editor_id);
      },
      when: notebookTracker.restored // After the notebook widgets (but not contents).

    });
  }

  var bindUnhandledIOPubMessageSignal = function bindUnhandledIOPubMessageSignal(nb) {
    if (!loggerRegistry) {
      return;
    }

    var wManager = contextToMetannoManagerRegistry[nb.context]; // Don't know what it is

    if (wManager) {
      wManager.onUnhandledIOPubMessage.connect(function (sender, msg) {
        var logger = loggerRegistry.getLogger(nb.context.path);
        var level = 'warning';

        if (_services.KernelMessage.isErrorMsg(msg) || _services.KernelMessage.isStreamMsg(msg) && msg.content.name === 'stderr') {
          level = 'error';
        }

        var data = _objectSpread(_objectSpread({}, msg.content), {}, {
          output_type: msg.header.msg_type
        });

        logger.rendermime = nb.content.rendermime;
        logger.log({
          type: 'output',
          data: data,
          level: level
        });
      });
    }
  }; // Some settings stuff, haven't used it yet


  if (settingRegistry !== null) {
    settingRegistry.load(plugin.id).then(function (settings) {
      settings.changed.connect(updateSettings);
      updateSettings(settings);
    }).catch(function (reason) {
      console.error(reason.message);
    });
  } // Sets the renderer everytime we see our special SpanComponent/TableEditor mimetype


  rendermime.addFactory({
    safe: false,
    mimeTypes: [MIMETYPE],
    // @ts-ignore
    createRenderer: function createRenderer(options) {
      new _renderer.default(options, null);
    }
  }, 0); // Adds the singleton MetannoManager to all existing editors in the labapp/notebook

  if (notebookTracker !== null) {
    notebookTracker.forEach(function (panel) {
      registerMetannoManager(panel.context, panel.content.rendermime, chain( // @ts-ignore
      getEditorsFromNotebook(panel.content), getLinkedEditorsFromApp(app, panel.sessionContext.path)));
      bindUnhandledIOPubMessageSignal(panel);
    });
    notebookTracker.widgetAdded.connect(function (sender, panel) {
      registerMetannoManager(panel.context, panel.content.rendermime, chain( // @ts-ignore
      getEditorsFromNotebook(panel.content), getLinkedEditorsFromApp(app, panel.sessionContext.path)));
      bindUnhandledIOPubMessageSignal(panel);
    });
  } // -----------------
  // Add some commands
  // -----------------


  if (settingRegistry !== null) {
    // Add a command for automatically saving metanno state.
    commands.addCommand('metanno:saveAnnotatorState', {
      label: 'Save Annotator State Automatically',
      execute: function execute() {
        return settingRegistry.set(plugin.id, 'saveState', !SETTINGS.saveState).catch(function (reason) {
          console.error("Failed to set ".concat(plugin.id, ": ").concat(reason.message));
        });
      },
      isToggled: function isToggled() {
        return SETTINGS.saveState;
      }
    });
  }

  if (menu) {
    menu.settingsMenu.addGroup([{
      command: 'metanno:saveAnnotatorState'
    }]);
  }
  /**
   * Whether there is an active notebook.
   */


  function isEnabled() {
    // : boolean
    return notebookTracker.currentWidget !== null && notebookTracker.currentWidget === shell.currentWidget;
  }
  /**
   * Whether there is an notebook active, with a single selected cell.
   */


  function isEnabledAndSingleSelected() {
    // :boolean
    if (!isEnabled()) {
      return false;
    }

    var content = notebookTracker.currentWidget.content;
    var index = content.activeCellIndex; // If there are selections that are not the active cell,
    // this command is confusing, so disable it.

    for (var i = 0; i < content.widgets.length; ++i) {
      if (content.isSelected(content.widgets[i]) && i !== index) {
        return false;
      }
    }

    return true;
  } // CodeCell context menu groups


  contextMenu.addItem({
    command: 'metanno:create-view',
    selector: '.jp-Notebook .jp-CodeCell',
    rank: 10.5
  });
  commands.addCommand('metanno:create-view', {
    label: 'Detach',
    execute: function () {
      var _execute = _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee(args) {
        var cell, current, editor_id, editor_type, path, content, widget;
        return regeneratorRuntime.wrap(function _callee$(_context4) {
          while (1) {
            switch (_context4.prev = _context4.next) {
              case 0:
                // If we are given a notebook path and cell index, then
                // use that, otherwise use the current active cell.
                editor_id = args.editor_id;
                editor_type = args.editor_type;
                path = args.path;

                if (!(editor_id && editor_type && path)) {
                  _context4.next = 9;
                  break;
                }

                current = docManager.findWidget(path, 'Notebook');

                if (current) {
                  _context4.next = 7;
                  break;
                }

                return _context4.abrupt("return");

              case 7:
                _context4.next = 13;
                break;

              case 9:
                current = notebookTracker.currentWidget;

                if (current) {
                  _context4.next = 12;
                  break;
                }

                return _context4.abrupt("return");

              case 12:
                cell = current.content.activeCell;

              case 13:
                // Create a MainAreaWidget
                content = new MetannoArea({
                  notebook: current,
                  cell: cell,
                  editor_id: editor_id,
                  editor_type: editor_type
                });
                widget = new _apputils.MainAreaWidget({
                  content: content
                });
                current.context.addSibling(widget, {
                  ref: current.id,
                  mode: 'split-bottom'
                }); // Add the cloned output to the output widget tracker.

                void metannoAreas.add(widget);
                void metannoAreas.save(widget); // Remove the output view if the parent notebook is closed.

                current.content.disposed.connect(function () {
                  widget.dispose();
                });
                _context4.next = 21;
                return Promise.all([commands.execute("notebook:hide-cell-outputs", args)]);

              case 21:
              case "end":
                return _context4.stop();
            }
          }
        }, _callee);
      }));

      function execute(_x) {
        return _execute.apply(this, arguments);
      }

      return execute;
    }(),
    isEnabled: isEnabledAndSingleSelected
  });
}

function updateSettings(settings) {
  SETTINGS.saveState = !!settings.get('saveState').composite;
}

var plugin = {
  id: 'metanno:plugin',
  // app
  requires: [_rendermime.IRenderMimeRegistry, // rendermime
  _docmanager.IDocumentManager],
  // docManager
  optional: [_notebook.INotebookTracker, // notebookTracker
  _settingregistry.ISettingRegistry, // settingRegistry
  _mainmenu.IMainMenu, // menu
  _logconsole.ILoggerRegistry, // loggerRegistry
  _application.ILayoutRestorer // restorer
  ],
  activate: activateMetannoExtension,
  autoStart: true
};
var _default = plugin;
exports["default"] = _default;

/***/ }),

/***/ "./lib/jupyter/renderer.js":
/*!*********************************!*\
  !*** ./lib/jupyter/renderer.js ***!
  \*********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";


function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }

Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

__webpack_require__(/*! regenerator-runtime/runtime */ "./node_modules/regenerator-runtime/runtime.js");

var _widgets = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");

var _reactDom = _interopRequireDefault(__webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom"));

var _reactRedux = __webpack_require__(/*! react-redux */ "webpack/sharing/consume/default/react-redux/react-redux");

var _react = _interopRequireDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));

var _TextView = _interopRequireDefault(__webpack_require__(/*! ../containers/TextView */ "./lib/containers/TextView/index.js"));

var _TableView = _interopRequireDefault(__webpack_require__(/*! ../containers/TableView */ "./lib/containers/TableView/index.js"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { Promise.resolve(value).then(_next, _throw); } }

function _asyncToGenerator(fn) { return function () { var self = this, args = arguments; return new Promise(function (resolve, reject) { var gen = fn.apply(self, args); function _next(value) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value); } function _throw(err) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err); } _next(undefined); }); }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); Object.defineProperty(Constructor, "prototype", { writable: false }); return Constructor; }

function _get() { if (typeof Reflect !== "undefined" && Reflect.get) { _get = Reflect.get; } else { _get = function _get(target, property, receiver) { var base = _superPropBase(target, property); if (!base) return; var desc = Object.getOwnPropertyDescriptor(base, property); if (desc.get) { return desc.get.call(arguments.length < 3 ? target : receiver); } return desc.value; }; } return _get.apply(this, arguments); }

function _superPropBase(object, property) { while (!Object.prototype.hasOwnProperty.call(object, property)) { object = _getPrototypeOf(object); if (object === null) break; } return object; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); Object.defineProperty(subClass, "prototype", { writable: false }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }

function _createSuper(Derived) { var hasNativeReflectConstruct = _isNativeReflectConstruct(); return function _createSuperInternal() { var Super = _getPrototypeOf(Derived), result; if (hasNativeReflectConstruct) { var NewTarget = _getPrototypeOf(this).constructor; result = Reflect.construct(Super, arguments, NewTarget); } else { result = Super.apply(this, arguments); } return _possibleConstructorReturn(this, result); }; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } else if (call !== void 0) { throw new TypeError("Derived constructors may only return object or undefined"); } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _isNativeReflectConstruct() { if (typeof Reflect === "undefined" || !Reflect.construct) return false; if (Reflect.construct.sham) return false; if (typeof Proxy === "function") return true; try { Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function () {})); return true; } catch (e) { return false; } }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

/**
 * A renderer for widgets.
 */
var MetannoRenderer = /*#__PURE__*/function (_Widget) {
  _inherits(MetannoRenderer, _Widget);

  var _super = _createSuper(MetannoRenderer);

  function MetannoRenderer(options, manager) {
    var _this;

    _classCallCheck(this, MetannoRenderer);

    _this = _super.call(this);

    _defineProperty(_assertThisInitialized(_this), "_mimeType", void 0);

    _defineProperty(_assertThisInitialized(_this), "_manager", void 0);

    _defineProperty(_assertThisInitialized(_this), "setManager", void 0);

    _defineProperty(_assertThisInitialized(_this), "_rerenderMimeModel", void 0);

    _defineProperty(_assertThisInitialized(_this), "model", void 0);

    _defineProperty(_assertThisInitialized(_this), "_editor_id", void 0);

    _defineProperty(_assertThisInitialized(_this), "_editor_type", void 0);

    _this._mimeType = options.mimeType;
    _this._editor_id = options.editor_id;
    _this._editor_type = options.editor_type;

    if (manager) {
      _this._manager = Promise.resolve(manager);
    } else {
      _this._manager = new Promise(function (resolve, reject) {
        _this.setManager = resolve;
      });
    }

    _this._rerenderMimeModel = null;
    _this.model = null; // Widget will either show up "immediately", ie as soon as the manager is ready,
    // or this method will return prematurely (no editor_id/editor_type/model) and will
    // wait for the mimetype manager to assign a model to this widget and call renderModel
    // on its own (which will call showContent)

    _this.showContent();

    return _this;
  }

  _createClass(MetannoRenderer, [{
    key: "editor_id",
    get: function get() {
      if (!this._editor_id) {
        var source = this.model.data[this._mimeType];
        this._editor_id = source['editor-id'];
      }

      return this._editor_id;
    }
  }, {
    key: "editor_type",
    get: function get() {
      if (!this._editor_type) {
        var source = this.model.data[this._mimeType];
        this._editor_type = source['editor-type'];
      }

      return this._editor_type;
    }
    /**
     * The widget manager.
     */

  }, {
    key: "manager",
    set: function set(value) {
      value.restored.connect(this._rerender, this);
      this.setManager(value);
    }
  }, {
    key: "setFlag",
    value: function setFlag(flag) {
      var wasVisible = this.isVisible;

      _get(_getPrototypeOf(MetannoRenderer.prototype), "setFlag", this).call(this, flag);

      if (this.isVisible && !wasVisible) {
        this.showContent();
      } else if (!this.isVisible && wasVisible) {
        this.hideContent();
      }
    }
  }, {
    key: "clearFlag",
    value: function clearFlag(flag) {
      var wasVisible = this.isVisible;

      _get(_getPrototypeOf(MetannoRenderer.prototype), "clearFlag", this).call(this, flag);

      if (this.isVisible && !wasVisible) {
        this.showContent();
      } else if (!this.isVisible && wasVisible) {
        this.hideContent();
      }
    }
  }, {
    key: "renderModel",
    value: function () {
      var _renderModel = _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee(model) {
        return regeneratorRuntime.wrap(function _callee$(_context) {
          while (1) {
            switch (_context.prev = _context.next) {
              case 0:
                this.model = model;
                _context.next = 3;
                return this.showContent();

              case 3:
              case "end":
                return _context.stop();
            }
          }
        }, _callee, this);
      }));

      function renderModel(_x) {
        return _renderModel.apply(this, arguments);
      }

      return renderModel;
    }()
  }, {
    key: "hideContent",
    value: function () {
      var _hideContent = _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee2() {
        var _this2 = this;

        return regeneratorRuntime.wrap(function _callee2$(_context2) {
          while (1) {
            switch (_context2.prev = _context2.next) {
              case 0:
                if (!this.isVisible) {
                  _reactDom.default.unmountComponentAtNode(this.node);

                  this._manager.then(function (manager) {
                    return manager.views.delete(_this2);
                  });
                }

              case 1:
              case "end":
                return _context2.stop();
            }
          }
        }, _callee2, this);
      }));

      function hideContent() {
        return _hideContent.apply(this, arguments);
      }

      return hideContent;
    }()
  }, {
    key: "showContent",
    value: function () {
      var _showContent = _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee3() {
        var editor_id, editor_type, source, manager;
        return regeneratorRuntime.wrap(function _callee3$(_context3) {
          while (1) {
            switch (_context3.prev = _context3.next) {
              case 0:
                if (this.isVisible) {
                  _context3.next = 2;
                  break;
                }

                return _context3.abrupt("return");

              case 2:
                editor_id = this._editor_id;
                editor_type = this._editor_type;

                if (!(!editor_id || !editor_type)) {
                  _context3.next = 12;
                  break;
                }

                if (!this.model) {
                  _context3.next = 11;
                  break;
                }

                source = this.model.data[this._mimeType];
                editor_id = source['editor-id'];
                editor_type = source['editor-type'];
                _context3.next = 12;
                break;

              case 11:
                return _context3.abrupt("return");

              case 12:
                // Let's be optimistic, and hope the widget state will come later.
                this.node.textContent = 'Loading widget...' + editor_id;
                _context3.next = 15;
                return this._manager;

              case 15:
                manager = _context3.sent;
                manager.views.add(this);

                try {
                  _reactDom.default.unmountComponentAtNode(this.node);
                } catch (e) {}

                if (editor_type === "span-editor") {
                  _reactDom.default.render( /*#__PURE__*/_react.default.createElement(_reactRedux.Provider, {
                    store: manager.store
                  }, /*#__PURE__*/_react.default.createElement(_TextView.default, {
                    id: editor_id,
                    selectEditorState: function selectEditorState() {
                      var _manager$app;

                      for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
                        args[_key] = arguments[_key];
                      }

                      return manager.try_catch_exec.apply(manager, [(_manager$app = manager.app) === null || _manager$app === void 0 ? void 0 : _manager$app.select_editor_state].concat(args));
                    },
                    onClickSpan: function onClickSpan() {
                      var _manager$app2;

                      for (var _len2 = arguments.length, args = new Array(_len2), _key2 = 0; _key2 < _len2; _key2++) {
                        args[_key2] = arguments[_key2];
                      }

                      return manager.queue_try_catch_exec.apply(manager, [(_manager$app2 = manager.app) === null || _manager$app2 === void 0 ? void 0 : _manager$app2.handle_click_span, editor_id].concat(args));
                    },
                    onMouseEnterSpan: function onMouseEnterSpan() {
                      var _manager$app3;

                      for (var _len3 = arguments.length, args = new Array(_len3), _key3 = 0; _key3 < _len3; _key3++) {
                        args[_key3] = arguments[_key3];
                      }

                      return manager.queue_try_catch_exec.apply(manager, [(_manager$app3 = manager.app) === null || _manager$app3 === void 0 ? void 0 : _manager$app3.handle_mouse_enter_span, editor_id].concat(args));
                    },
                    onMouseLeaveSpan: function onMouseLeaveSpan() {
                      var _manager$app4;

                      for (var _len4 = arguments.length, args = new Array(_len4), _key4 = 0; _key4 < _len4; _key4++) {
                        args[_key4] = arguments[_key4];
                      }

                      return manager.queue_try_catch_exec.apply(manager, [(_manager$app4 = manager.app) === null || _manager$app4 === void 0 ? void 0 : _manager$app4.handle_mouse_leave_span, editor_id].concat(args));
                    },
                    onKeyPress: function onKeyPress() {
                      var _manager$app5;

                      for (var _len5 = arguments.length, args = new Array(_len5), _key5 = 0; _key5 < _len5; _key5++) {
                        args[_key5] = arguments[_key5];
                      }

                      return manager.queue_try_catch_exec.apply(manager, [(_manager$app5 = manager.app) === null || _manager$app5 === void 0 ? void 0 : _manager$app5.handle_key_press, editor_id].concat(args));
                    } //onKeyDown={(...args) => manager.queue_try_catch_exec(manager.app?.handle_key_down)(editor_id, ...args)}
                    ,
                    onMouseSelect: function onMouseSelect() {
                      var _manager$app6;

                      for (var _len6 = arguments.length, args = new Array(_len6), _key6 = 0; _key6 < _len6; _key6++) {
                        args[_key6] = arguments[_key6];
                      }

                      return manager.queue_try_catch_exec.apply(manager, [(_manager$app6 = manager.app) === null || _manager$app6 === void 0 ? void 0 : _manager$app6.handle_mouse_select, editor_id].concat(args));
                    },
                    onButtonPress: function onButtonPress() {
                      var _manager$app7;

                      for (var _len7 = arguments.length, args = new Array(_len7), _key7 = 0; _key7 < _len7; _key7++) {
                        args[_key7] = arguments[_key7];
                      }

                      return manager.queue_try_catch_exec.apply(manager, [(_manager$app7 = manager.app) === null || _manager$app7 === void 0 ? void 0 : _manager$app7.handle_button_press, editor_id].concat(args));
                    },
                    registerActions: function registerActions(methods) {
                      manager.actions[editor_id] = methods;
                    }
                  })), this.node);
                } else if (editor_type === "table-editor") {
                  _reactDom.default.render( /*#__PURE__*/_react.default.createElement(_reactRedux.Provider, {
                    store: manager.store
                  }, /*#__PURE__*/_react.default.createElement(_TableView.default, {
                    id: editor_id,
                    selectEditorState: function selectEditorState() {
                      var _manager$app8;

                      for (var _len8 = arguments.length, args = new Array(_len8), _key8 = 0; _key8 < _len8; _key8++) {
                        args[_key8] = arguments[_key8];
                      }

                      return manager.try_catch_exec.apply(manager, [(_manager$app8 = manager.app) === null || _manager$app8 === void 0 ? void 0 : _manager$app8.select_editor_state].concat(args));
                    },
                    onKeyPress: function onKeyPress() {
                      var _manager$app9;

                      for (var _len9 = arguments.length, args = new Array(_len9), _key9 = 0; _key9 < _len9; _key9++) {
                        args[_key9] = arguments[_key9];
                      }

                      return manager.queue_try_catch_exec.apply(manager, [(_manager$app9 = manager.app) === null || _manager$app9 === void 0 ? void 0 : _manager$app9.handle_key_press, editor_id].concat(args));
                    },
                    onClickCellContent: function onClickCellContent() {
                      var _manager$app10;

                      for (var _len10 = arguments.length, args = new Array(_len10), _key10 = 0; _key10 < _len10; _key10++) {
                        args[_key10] = arguments[_key10];
                      }

                      return manager.queue_try_catch_exec.apply(manager, [(_manager$app10 = manager.app) === null || _manager$app10 === void 0 ? void 0 : _manager$app10.handle_click_cell_content, editor_id].concat(args));
                    },
                    onMouseEnterRow: function onMouseEnterRow() {
                      var _manager$app11;

                      for (var _len11 = arguments.length, args = new Array(_len11), _key11 = 0; _key11 < _len11; _key11++) {
                        args[_key11] = arguments[_key11];
                      }

                      return manager.queue_try_catch_exec.apply(manager, [(_manager$app11 = manager.app) === null || _manager$app11 === void 0 ? void 0 : _manager$app11.handle_mouse_enter_row, editor_id].concat(args));
                    },
                    onMouseLeaveRow: function onMouseLeaveRow() {
                      var _manager$app12;

                      for (var _len12 = arguments.length, args = new Array(_len12), _key12 = 0; _key12 < _len12; _key12++) {
                        args[_key12] = arguments[_key12];
                      }

                      return manager.queue_try_catch_exec.apply(manager, [(_manager$app12 = manager.app) === null || _manager$app12 === void 0 ? void 0 : _manager$app12.handle_mouse_leave_row, editor_id].concat(args));
                    },
                    onSelectedPositionChange: function onSelectedPositionChange() {
                      var _manager$app13;

                      for (var _len13 = arguments.length, args = new Array(_len13), _key13 = 0; _key13 < _len13; _key13++) {
                        args[_key13] = arguments[_key13];
                      }

                      return manager.queue_try_catch_exec.apply(manager, [(_manager$app13 = manager.app) === null || _manager$app13 === void 0 ? void 0 : _manager$app13.handle_selected_position_change, editor_id].concat(args));
                    },
                    onSelectedRowsChange: function onSelectedRowsChange() {
                      var _manager$app14;

                      for (var _len14 = arguments.length, args = new Array(_len14), _key14 = 0; _key14 < _len14; _key14++) {
                        args[_key14] = arguments[_key14];
                      }

                      return manager.queue_try_catch_exec.apply(manager, [(_manager$app14 = manager.app) === null || _manager$app14 === void 0 ? void 0 : _manager$app14.handle_select_rows, editor_id].concat(args));
                    },
                    onCellChange: function onCellChange() {
                      var _manager$app15;

                      for (var _len15 = arguments.length, args = new Array(_len15), _key15 = 0; _key15 < _len15; _key15++) {
                        args[_key15] = arguments[_key15];
                      }

                      return manager.queue_try_catch_exec.apply(manager, [(_manager$app15 = manager.app) === null || _manager$app15 === void 0 ? void 0 : _manager$app15.handle_cell_change, editor_id].concat(args));
                    },
                    onFiltersChange: function onFiltersChange() {
                      var _manager$app16;

                      for (var _len16 = arguments.length, args = new Array(_len16), _key16 = 0; _key16 < _len16; _key16++) {
                        args[_key16] = arguments[_key16];
                      }

                      return manager.queue_try_catch_exec.apply(manager, [(_manager$app16 = manager.app) === null || _manager$app16 === void 0 ? void 0 : _manager$app16.handle_filters_change, editor_id].concat(args));
                    },
                    registerActions: function registerActions(methods) {
                      manager.actions[editor_id] = methods;
                    },
                    onButtonPress: function onButtonPress() {
                      var _manager$app17;

                      for (var _len17 = arguments.length, args = new Array(_len17), _key17 = 0; _key17 < _len17; _key17++) {
                        args[_key17] = arguments[_key17];
                      }

                      return manager.queue_try_catch_exec.apply(manager, [(_manager$app17 = manager.app) === null || _manager$app17 === void 0 ? void 0 : _manager$app17.handle_button_press, editor_id].concat(args));
                    },
                    onInputChange: function onInputChange() {
                      var _manager$app18;

                      for (var _len18 = arguments.length, args = new Array(_len18), _key18 = 0; _key18 < _len18; _key18++) {
                        args[_key18] = arguments[_key18];
                      }

                      return manager.queue_try_catch_exec.apply(manager, [(_manager$app18 = manager.app) === null || _manager$app18 === void 0 ? void 0 : _manager$app18.handle_input_change, editor_id].concat(args));
                    }
                  })), this.node);
                }
                /*let wModel;
                try {
                    // Presume we have a DOMWidgetModel. Should we check for sure?
                    wModel = (await manager.get_model(source.model_id));
                } catch (err) {
                    if (manager.restoredStatus) {
                        // The manager has been restored, so this error won't be going away.
                        this.node.textContent = 'Error displaying widget: model not found';
                        this.addClass('jupyter-widgets');
                        console.error(err);
                        return;
                    }
                     // Store the model for a possible rerender
                    this._rerenderMimeModel = model;
                    return;
                }
                 // Successful getting the model, so we don't need to try to rerender.
                this._rerenderMimeModel = null;
                 let widget;
                try {
                    widget = (await manager.create_view(wModel)).pWidget;
                } catch (err) {
                    this.node.textContent = 'Error displaying widget';
                    this.addClass('jupyter-widgets');
                    console.error(err);
                    return;
                }
                 // When the widget is disposed, hide this container and make sure we
                // change the output model to reflect the view was closed.
                widget.disposed.connect(() => {
                    this.hide();
                    source.model_id = '';
                });*/


              case 19:
              case "end":
                return _context3.stop();
            }
          }
        }, _callee3, this);
      }));

      function showContent() {
        return _showContent.apply(this, arguments);
      }

      return showContent;
    }()
    /**
     * Get whether the manager is disposed.
     *
     * #### Notes
     * This is a read-only property.
     */
    // @ts-ignore

  }, {
    key: "isDisposed",
    get: function get() {
      return this._manager === null;
    }
    /**
     * Dispose the resources held by the manager.
     */

  }, {
    key: "dispose",
    value: function dispose() {
      if (this.isDisposed) {
        return;
      }

      _get(_getPrototypeOf(MetannoRenderer.prototype), "dispose", this).call(this);

      this._manager = null;
    }
  }, {
    key: "_rerender",
    value: function _rerender() {
      if (this._rerenderMimeModel) {
        // Clear the error message
        this.node.textContent = '';
        this.removeClass('jupyter-widgets'); // Attempt to rerender.

        this.renderModel(this._rerenderMimeModel).then();
      }
    }
    /**
     * The mimetype being rendered.
     */

  }]);

  return MetannoRenderer;
}(_widgets.Widget);

exports["default"] = MetannoRenderer;
;

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./lib/jupyter/metanno.css":
/*!***********************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./lib/jupyter/metanno.css ***!
  \***********************************************************************/
/***/ (function(module, exports, __webpack_require__) {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".jp-toastContainer .Toastify__toast-body {\n    display: flex;\n}", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./lib/icon.svg":
/*!**********************!*\
  !*** ./lib/icon.svg ***!
  \**********************/
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony default export */ __webpack_exports__["default"] = ("<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" version=\"1.1\" width=\"16px\" viewBox=\"-0.5 -0.5 115 123\">\n    <defs/>\n    <g>\n        <rect x=\"4\" y=\"22\" width=\"106\" height=\"96\" rx=\"8.64\" ry=\"8.64\" fill=\"#dae8fc\" stroke=\"#6c8ebf\" stroke-width=\"9\" pointer-events=\"all\"/>\n        <rect x=\"16\" y=\"4\" width=\"65\" height=\"54\" rx=\"4.86\" ry=\"4.86\" fill=\"#ffffff\" stroke=\"#6c8ebf\" stroke-width=\"9\" pointer-events=\"all\"/>\n    </g>\n</svg>");

/***/ }),

/***/ "./lib/jupyter/metanno.css":
/*!*********************************!*\
  !*** ./lib/jupyter/metanno.css ***!
  \*********************************/
/***/ (function(module, __unused_webpack_exports, __webpack_require__) {


var content = __webpack_require__(/*! !!../../node_modules/css-loader/dist/cjs.js!./metanno.css */ "./node_modules/css-loader/dist/cjs.js!./lib/jupyter/metanno.css");

if(typeof content === 'string') content = [[module.id, content, '']];

var transform;
var insertInto;



var options = {"hmr":true}

options.transform = transform
options.insertInto = undefined;

var update = __webpack_require__(/*! !../../node_modules/style-loader/lib/addStyles.js */ "./node_modules/style-loader/lib/addStyles.js")(content, options);

if(content.locals) module.exports = content.locals;

if(false) {}

/***/ })

}]);
//# sourceMappingURL=lib_jupyter_plugin_js.9a9d282bd8d8e026e920.js.map