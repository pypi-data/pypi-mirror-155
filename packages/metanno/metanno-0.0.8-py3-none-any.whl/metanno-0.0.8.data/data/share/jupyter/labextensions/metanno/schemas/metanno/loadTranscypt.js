"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.eval_code = eval_code;

var _immer = require("immer");

function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { Promise.resolve(value).then(_next, _throw); } }

function _asyncToGenerator(fn) { return function () { var self = this, args = arguments; return new Promise(function (resolve, reject) { var gen = fn.apply(self, args); function _next(value) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value); } function _throw(err) { asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err); } _next(undefined); }); }; }

var _require = require('./org.transcrypt.__runtime__.js'),
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