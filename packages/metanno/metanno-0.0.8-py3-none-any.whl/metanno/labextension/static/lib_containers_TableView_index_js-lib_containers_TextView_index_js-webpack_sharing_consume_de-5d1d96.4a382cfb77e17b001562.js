(self["webpackChunkmetanno"] = self["webpackChunkmetanno"] || []).push([["lib_containers_TableView_index_js-lib_containers_TextView_index_js-webpack_sharing_consume_de-5d1d96"],{

/***/ "./lib/components/BooleanInput/index.js":
/*!**********************************************!*\
  !*** ./lib/components/BooleanInput/index.js ***!
  \**********************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";


function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }

Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = BooleanInput;

var _react = _interopRequireWildcard(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));

__webpack_require__(/*! ./style.css */ "./lib/components/BooleanInput/style.css");

function _getRequireWildcardCache(nodeInterop) { if (typeof WeakMap !== "function") return null; var cacheBabelInterop = new WeakMap(); var cacheNodeInterop = new WeakMap(); return (_getRequireWildcardCache = function _getRequireWildcardCache(nodeInterop) { return nodeInterop ? cacheNodeInterop : cacheBabelInterop; })(nodeInterop); }

function _interopRequireWildcard(obj, nodeInterop) { if (!nodeInterop && obj && obj.__esModule) { return obj; } if (obj === null || _typeof(obj) !== "object" && typeof obj !== "function") { return { default: obj }; } var cache = _getRequireWildcardCache(nodeInterop); if (cache && cache.has(obj)) { return cache.get(obj); } var newObj = {}; var hasPropertyDescriptor = Object.defineProperty && Object.getOwnPropertyDescriptor; for (var key in obj) { if (key !== "default" && Object.prototype.hasOwnProperty.call(obj, key)) { var desc = hasPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : null; if (desc && (desc.get || desc.set)) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } newObj.default = obj; if (cache) { cache.set(obj, newObj); } return newObj; }

var checkboxLabel = "c1w6d5eo700-beta7";
var checkboxLabelClassname = "rdg-checkbox-label ".concat(checkboxLabel);
var checkboxInput = "c1h7iz8d700-beta7";
var checkboxInputClassname = "rdg-checkbox-input ".concat(checkboxInput);
var checkbox = "cc79ydj700-beta7";
var checkboxClassname = "rdg-checkbox ".concat(checkbox);
var checkboxLabelDisabled = "c1e5jt0b700-beta7";
var checkboxLabelDisabledClassname = "rdg-checkbox-label-disabled ".concat(checkboxLabelDisabled);
var useLayoutEffect = typeof window === 'undefined' ? _react.useEffect : _react.useLayoutEffect;

function useFocusRef(isSelected) {
  var ref = (0, _react.useRef)(null);
  useLayoutEffect(function () {
    var _ref$current;

    if (!isSelected) return;
    (_ref$current = ref.current) == null ? void 0 : _ref$current.focus({
      preventScroll: true
    });
  }, [isSelected]);
  return {
    ref: ref,
    tabIndex: isSelected ? 0 : -1
  };
}

function BooleanInput(_ref) {
  var value = _ref.value,
      isCellSelected = _ref.isCellSelected,
      disabled = _ref.disabled,
      onClick = _ref.onClick,
      onChange = _ref.onChange,
      ariaLabel = _ref['aria-label'],
      ariaLabelledBy = _ref['aria-labelledby'];

  var _useFocusRef = useFocusRef(isCellSelected),
      ref = _useFocusRef.ref,
      tabIndex = _useFocusRef.tabIndex;

  function handleChange(e) {
    onChange(e.target.checked, e.nativeEvent.shiftKey);
  }

  return /*#__PURE__*/_react.default.createElement("div", {
    className: 'rdg-checkbox-container'
  }, /*#__PURE__*/_react.default.createElement("label", {
    className: "".concat(checkboxLabelClassname, " ").concat(disabled ? checkboxLabelDisabledClassname : '')
  }, /*#__PURE__*/_react.default.createElement("input", {
    "aria-label": ariaLabel,
    "aria-labelledby": ariaLabelledBy,
    ref: ref,
    type: "checkbox",
    tabIndex: tabIndex,
    className: checkboxInputClassname,
    disabled: disabled,
    checked: value,
    onChange: handleChange
  }), /*#__PURE__*/_react.default.createElement("div", {
    className: checkboxClassname
  })));
}

/***/ }),

/***/ "./lib/components/DraggableHeaderRenderer/index.js":
/*!*********************************************************!*\
  !*** ./lib/components/DraggableHeaderRenderer/index.js ***!
  \*********************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";


function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }

Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;
exports.useFocusRef = useFocusRef;

var _react = _interopRequireWildcard(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));

var _reactDnd = __webpack_require__(/*! react-dnd */ "webpack/sharing/consume/default/react-dnd/react-dnd");

function _getRequireWildcardCache(nodeInterop) { if (typeof WeakMap !== "function") return null; var cacheBabelInterop = new WeakMap(); var cacheNodeInterop = new WeakMap(); return (_getRequireWildcardCache = function _getRequireWildcardCache(nodeInterop) { return nodeInterop ? cacheNodeInterop : cacheBabelInterop; })(nodeInterop); }

function _interopRequireWildcard(obj, nodeInterop) { if (!nodeInterop && obj && obj.__esModule) { return obj; } if (obj === null || _typeof(obj) !== "object" && typeof obj !== "function") { return { default: obj }; } var cache = _getRequireWildcardCache(nodeInterop); if (cache && cache.has(obj)) { return cache.get(obj); } var newObj = {}; var hasPropertyDescriptor = Object.defineProperty && Object.getOwnPropertyDescriptor; for (var key in obj) { if (key !== "default" && Object.prototype.hasOwnProperty.call(obj, key)) { var desc = hasPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : null; if (desc && (desc.get || desc.set)) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } newObj.default = obj; if (cache) { cache.set(obj, newObj); } return newObj; }

function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _iterableToArrayLimit(arr, i) { var _i = arr == null ? null : typeof Symbol !== "undefined" && arr[Symbol.iterator] || arr["@@iterator"]; if (_i == null) return; var _arr = []; var _n = true; var _d = false; var _s, _e; try { for (_i = _i.call(arr); !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

function _createForOfIteratorHelper(o, allowArrayLike) { var it = typeof Symbol !== "undefined" && o[Symbol.iterator] || o["@@iterator"]; if (!it) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e2) { throw _e2; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = it.call(o); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e3) { didErr = true; err = _e3; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

function useCombinedRefs() {
  for (var _len = arguments.length, refs = new Array(_len), _key = 0; _key < _len; _key++) {
    refs[_key] = arguments[_key];
  }

  return (0, _react.useCallback)(function (handle) {
    var _iterator = _createForOfIteratorHelper(refs),
        _step;

    try {
      for (_iterator.s(); !(_step = _iterator.n()).done;) {
        var ref = _step.value;

        if (typeof ref === 'function') {
          ref(handle);
        } else if (ref !== null && 'current' in ref) {
          ref.current = handle;
        }
      }
    } catch (err) {
      _iterator.e(err);
    } finally {
      _iterator.f();
    }
  }, refs);
}

function useFocusRef(isSelected) {
  var ref = (0, _react.useRef)(null);
  (0, _react.useLayoutEffect)(function () {
    var _ref$current;

    if (!isSelected) return;
    (_ref$current = ref.current) === null || _ref$current === void 0 ? void 0 : _ref$current.focus({
      preventScroll: true
    });
  }, [isSelected]);
  return {
    ref: ref,
    tabIndex: isSelected ? 0 : -1
  };
}

function HeaderRenderer(_ref) {
  var isCellSelected = _ref.isCellSelected,
      column = _ref.column,
      children = _ref.children,
      onColumnsReorder = _ref.onColumnsReorder;

  var _useFocusRef = useFocusRef(isCellSelected),
      ref = _useFocusRef.ref,
      tabIndex = _useFocusRef.tabIndex;

  var _useDrag = (0, _reactDnd.useDrag)({
    item: {
      key: column.key,
      type: 'COLUMN_DRAG'
    },
    collect: function collect(monitor) {
      return {
        isDragging: !!monitor.isDragging()
      };
    }
  }),
      _useDrag2 = _slicedToArray(_useDrag, 2),
      isDragging = _useDrag2[0].isDragging,
      drag = _useDrag2[1];

  var _useDrop = (0, _reactDnd.useDrop)({
    accept: 'COLUMN_DRAG',
    // @ts-ignore
    drop: function drop(_ref2) {
      var key = _ref2.key,
          type = _ref2.type;

      if (type === 'COLUMN_DRAG') {
        onColumnsReorder(key, column.key);
      }
    },
    collect: function collect(monitor) {
      return {
        isOver: !!monitor.isOver(),
        canDrop: !!monitor.canDrop()
      };
    }
  }),
      _useDrop2 = _slicedToArray(_useDrop, 2),
      isOver = _useDrop2[0].isOver,
      drop = _useDrop2[1];

  return /*#__PURE__*/_react.default.createElement("div", {
    ref: useCombinedRefs(drag, drop),
    style: {
      opacity: isDragging ? 0.5 : 1,
      backgroundColor: isOver ? '#ececec' : 'transparent',
      cursor: 'move'
    }
  }, /*#__PURE__*/_react.default.createElement("div", null, column.name), children ? /*#__PURE__*/_react.default.createElement("div", null, " ", children({
    ref: ref,
    tabIndex: tabIndex
  }), " ") : null);
}

var _default = HeaderRenderer;
exports["default"] = _default;

/***/ }),

/***/ "./lib/components/Loading/index.js":
/*!*****************************************!*\
  !*** ./lib/components/Loading/index.js ***!
  \*****************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var _react = _interopRequireDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));

__webpack_require__(/*! ./style.css */ "./lib/components/Loading/style.css");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var _default = function _default() {
  return /*#__PURE__*/_react.default.createElement("div", {
    className: "loading",
    style: {
      'position': 'absolute',
      'top': '50%',
      'left': '50%',
      'transform': 'translateX(-50%) translateY(-50%)',
      'textAlign': 'center'
    }
  }, /*#__PURE__*/_react.default.createElement("p", {
    style: {
      fontSize: '1.5em',
      fontWeight: 300,
      marginBottom: '5px'
    }
  }, "Editor is loading..."), /*#__PURE__*/_react.default.createElement("svg", {
    width: "38",
    height: "38",
    viewBox: "0 0 38 38",
    xmlns: "http://www.w3.org/2000/svg"
  }, /*#__PURE__*/_react.default.createElement("defs", null, /*#__PURE__*/_react.default.createElement("linearGradient", {
    x1: "8.042%",
    y1: "0%",
    x2: "65.682%",
    y2: "23.865%",
    id: "a"
  }, /*#__PURE__*/_react.default.createElement("stop", {
    stopOpacity: "0",
    offset: "0%"
  }), /*#__PURE__*/_react.default.createElement("stop", {
    stopOpacity: ".631",
    offset: "63.146%"
  }), /*#__PURE__*/_react.default.createElement("stop", {
    offset: "100%"
  }))), /*#__PURE__*/_react.default.createElement("g", {
    fill: "none",
    fillRule: "evenodd"
  }, /*#__PURE__*/_react.default.createElement("g", {
    transform: "translate(1 1)"
  }, /*#__PURE__*/_react.default.createElement("path", {
    d: "M36 18c0-9.94-8.06-18-18-18",
    id: "Oval-2",
    stroke: "url(#a)",
    strokeWidth: "2"
  }, /*#__PURE__*/_react.default.createElement("animateTransform", {
    attributeName: "transform",
    type: "rotate",
    from: "0 18 18",
    to: "360 18 18",
    dur: "0.9s",
    repeatCount: "indefinite"
  })), /*#__PURE__*/_react.default.createElement("circle", {
    cx: "36",
    cy: "18",
    r: "1"
  }, /*#__PURE__*/_react.default.createElement("animateTransform", {
    attributeName: "transform",
    type: "rotate",
    from: "0 18 18",
    to: "360 18 18",
    dur: "0.9s",
    repeatCount: "indefinite"
  }))))));
};

exports["default"] = _default;

/***/ }),

/***/ "./lib/components/MultiInputSuggest/index.js":
/*!***************************************************!*\
  !*** ./lib/components/MultiInputSuggest/index.js ***!
  \***************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";


function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }

Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = exports.InputTag = void 0;

var _react = _interopRequireDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));

var _reactAutosuggest = _interopRequireDefault(__webpack_require__(/*! react-autosuggest */ "webpack/sharing/consume/default/react-autosuggest/react-autosuggest"));

__webpack_require__(/*! ./style.css */ "./lib/components/MultiInputSuggest/style.css");

var _excluded = ["hyperlink"];

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _objectWithoutProperties(source, excluded) { if (source == null) return {}; var target = _objectWithoutPropertiesLoose(source, excluded); var key, i; if (Object.getOwnPropertySymbols) { var sourceSymbolKeys = Object.getOwnPropertySymbols(source); for (i = 0; i < sourceSymbolKeys.length; i++) { key = sourceSymbolKeys[i]; if (excluded.indexOf(key) >= 0) continue; if (!Object.prototype.propertyIsEnumerable.call(source, key)) continue; target[key] = source[key]; } } return target; }

function _objectWithoutPropertiesLoose(source, excluded) { if (source == null) return {}; var target = {}; var sourceKeys = Object.keys(source); var key, i; for (i = 0; i < sourceKeys.length; i++) { key = sourceKeys[i]; if (excluded.indexOf(key) >= 0) continue; target[key] = source[key]; } return target; }

function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }

function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _iterableToArray(iter) { if (typeof Symbol !== "undefined" && iter[Symbol.iterator] != null || iter["@@iterator"] != null) return Array.from(iter); }

function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

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

function _extends() { _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; }; return _extends.apply(this, arguments); }

function get_text(value) {
  return typeof value === "string" ? value : value && value.text ? value.text : "";
}

var InputTag = function InputTag(_ref) {
  var value = _ref.value,
      _ref$inputProps = _ref.inputProps,
      inputProps = _ref$inputProps === void 0 ? {} : _ref$inputProps,
      _ref$autocontain = _ref.autocontain,
      autocontain = _ref$autocontain === void 0 ? false : _ref$autocontain,
      _ref$readOnly = _ref.readOnly,
      readOnly = _ref$readOnly === void 0 ? false : _ref$readOnly,
      _ref$hyperlink = _ref.hyperlink,
      hyperlink = _ref$hyperlink === void 0 ? false : _ref$hyperlink,
      _ref$onRemoveTag = _ref.onRemoveTag,
      onRemoveTag = _ref$onRemoveTag === void 0 ? null : _ref$onRemoveTag,
      _ref$onClick = _ref.onClick,
      _onClick = _ref$onClick === void 0 ? null : _ref$onClick;

  var res = /*#__PURE__*/_react.default.createElement("div", {
    className: "input-tag ".concat(readOnly ? '' : 'editable')
  }, /*#__PURE__*/_react.default.createElement("ul", {
    className: "input-tag__tags"
  }, value.map(function (tag, i) {
    return /*#__PURE__*/_react.default.createElement("li", {
      key: i
    }, hyperlink ? /*#__PURE__*/_react.default.createElement("a", {
      onClick: function onClick() {
        return _onClick(tag.key);
      }
    }, tag.text) : /*#__PURE__*/_react.default.createElement("span", null, tag), readOnly ? null : /*#__PURE__*/_react.default.createElement("button", {
      type: "button",
      onClick: function onClick() {
        return !!onRemoveTag && onRemoveTag(i);
      }
    }, "\u2715"));
  }), readOnly ? null : /*#__PURE__*/_react.default.createElement("li", {
    className: "input-tag__tags__input"
  }, /*#__PURE__*/_react.default.createElement("input", _extends({
    autoFocus: true,
    type: "text"
  }, inputProps)))));

  if (autocontain) {
    return /*#__PURE__*/_react.default.createElement("div", {
      className: "input-tag-container"
    }, res);
  }

  return res;
};

exports.InputTag = InputTag;

var MultiInputSuggest = /*#__PURE__*/function (_React$Component) {
  _inherits(MultiInputSuggest, _React$Component);

  var _super = _createSuper(MultiInputSuggest);

  function MultiInputSuggest(props) {
    var _this;

    _classCallCheck(this, MultiInputSuggest);

    _this = _super.call(this, props);

    _defineProperty(_assertThisInitialized(_this), "needsInputScroll", void 0);

    _defineProperty(_assertThisInitialized(_this), "onInputChange", function (event, _ref2) {
      var _this$props$onInputCh, _this$props;

      var newValue = _ref2.newValue,
          method = _ref2.method;

      var newTags = _toConsumableArray(_this.getInputValue() || []);

      newTags[newTags.length - 1] = newValue;
      (_this$props$onInputCh = (_this$props = _this.props).onInputChange) === null || _this$props$onInputCh === void 0 ? void 0 : _this$props$onInputCh.call(_this$props, newTags, method);
    });

    _defineProperty(_assertThisInitialized(_this), "removeTag", function (i) {
      var _this$props$onInputCh2, _this$props2;

      var newTags = _toConsumableArray(_this.props.inputValue || []);

      newTags.splice(i, 1);
      (_this$props$onInputCh2 = (_this$props2 = _this.props).onInputChange) === null || _this$props$onInputCh2 === void 0 ? void 0 : _this$props$onInputCh2.call(_this$props2, newTags, "remove");
    });

    _defineProperty(_assertThisInitialized(_this), "addTag", function () {
      var newTags = _toConsumableArray(_this.props.inputValue || []);

      newTags.push("");

      _this.props.onInputChange(newTags, "add");
    });

    _defineProperty(_assertThisInitialized(_this), "inputKeyDown", function (event) {
      var commit = false;
      var val = event.target.value;

      var inputValue = _this.getInputValue();

      if ((event.key === 'Tab' || event.key === 'Enter') && val) {
        _this.addTag();

        _this.needsInputScroll = true;
        event.preventDefault();
        event.stopPropagation();
      } else if (event.key === 'Backspace' && !val) {
        _this.removeTag(inputValue.length - 1);
      } else if (!!_this.props.suggestions && ['ArrowUp', 'ArrowDown'].includes(event.key)) {
        commit = false;
      } else if (['Enter', 'Tab', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(event.key)) {
        commit = true;
      } else if (['Escape'].includes(event.key)) {
        _this.props.onClose();
      }

      if (commit) {
        if (_this.getEditedValue() === "") {
          _this.props.onRowChange(_defineProperty({}, _this.props.column, inputValue.slice(0, inputValue.length - 1)), true);
        } else {
          _this.props.onRowChange(_defineProperty({}, _this.props.column, inputValue), true);
        }
      }
    });

    _defineProperty(_assertThisInitialized(_this), "onAutoSuggestRef", function (ref) {
      if (_this.props.inputRef) {
        // @ts-ignore
        _this.props.inputRef.current = ref ? ref.input : null;

        if (ref) {
          ref.input.focus();
        }
      }
    });

    _defineProperty(_assertThisInitialized(_this), "renderSuggestion", function (suggestion) {
      return /*#__PURE__*/_react.default.createElement("div", null, _this.props.hyperlink ? /*#__PURE__*/_react.default.createElement("a", {
        onClick: function onClick() {
          var _this$props$onClick, _this$props3;

          return (_this$props$onClick = (_this$props3 = _this.props).onClick) === null || _this$props$onClick === void 0 ? void 0 : _this$props$onClick.call(_this$props3, _this.props.row_id, _this.props.column, suggestion.key);
        }
      }, suggestion.text) : suggestion);
    });

    _defineProperty(_assertThisInitialized(_this), "renderInput", function (_ref3) {
      var hyperlink = _ref3.hyperlink,
          inputProps = _objectWithoutProperties(_ref3, _excluded);

      var inputValue = _this.getInputValue();

      return /*#__PURE__*/_react.default.createElement(InputTag, {
        value: inputValue.slice(0, inputValue.length - 1),
        inputProps: inputProps,
        onRemoveTag: _this.removeTag,
        hyperlink: !!hyperlink
      });
    });

    _defineProperty(_assertThisInitialized(_this), "onSuggestionsFetchRequested", function () {});

    _defineProperty(_assertThisInitialized(_this), "onSuggestionsClearRequested", function () {});

    _this.needsInputScroll = false;
    return _this;
  }

  _createClass(MultiInputSuggest, [{
    key: "getInputValue",
    value: function getInputValue() {
      return Array.isArray(this.props.inputValue) ? this.props.inputValue : [];
    }
  }, {
    key: "getEditedValue",
    value: function getEditedValue() {
      return Array.isArray(this.props.inputValue) ? this.props.inputValue[this.props.inputValue.length - 1] : null;
    }
  }, {
    key: "componentDidMount",
    value: function componentDidMount() {
      this.props.onInputChange([].concat(_toConsumableArray(this.props.value), [""]), "mount");
    }
  }, {
    key: "componentWillUnmount",
    value: function componentWillUnmount() {
      this.props.onInputChange(null, "unmount");
    }
  }, {
    key: "render",
    value: function render() {
      var inputValue = get_text(this.getEditedValue());
      var inputProps = {
        placeholder: 'Type here',
        value: inputValue,
        onChange: this.onInputChange,
        onKeyDown: this.inputKeyDown,
        hyperlink: this.props.hyperlink
      };
      return /*#__PURE__*/_react.default.createElement("div", {
        onKeyDown: function onKeyDown(event) {
          return event.defaultPrevented && event.stopPropagation();
        }
      }, /*#__PURE__*/_react.default.createElement(_reactAutosuggest.default, {
        ref: this.onAutoSuggestRef,
        alwaysRenderSuggestions: true,
        suggestions: this.props.suggestions,
        onSuggestionsFetchRequested: this.onSuggestionsFetchRequested,
        onSuggestionsClearRequested: this.onSuggestionsClearRequested,
        renderInputComponent: this.renderInput,
        getSuggestionValue: function getSuggestionValue(val) {
          return val;
        },
        renderSuggestion: this.renderSuggestion,
        inputProps: inputProps
      }));
    }
  }, {
    key: "componentDidUpdate",
    value: function componentDidUpdate() {
      if (this.needsInputScroll && this.props.inputRef && this.props.inputRef.current) {
        // @ts-ignore
        this.props.inputRef.current.scrollIntoViewIfNeeded({
          behavior: 'smooth'
        });
      }

      this.needsInputScroll = false;
    }
  }]);

  return MultiInputSuggest;
}(_react.default.Component);

_defineProperty(MultiInputSuggest, "defaultProps", {
  hyperlink: false,
  suggestions: []
});

var _default = MultiInputSuggest;
exports["default"] = _default;

/***/ }),

/***/ "./lib/components/SingleInputSuggest/index.js":
/*!****************************************************!*\
  !*** ./lib/components/SingleInputSuggest/index.js ***!
  \****************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = exports.Input = void 0;

var _react = _interopRequireDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));

var _reactAutosuggest = _interopRequireDefault(__webpack_require__(/*! react-autosuggest */ "webpack/sharing/consume/default/react-autosuggest/react-autosuggest"));

__webpack_require__(/*! ./style.css */ "./lib/components/SingleInputSuggest/style.css");

var _excluded = ["hyperlink"];

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _objectWithoutProperties(source, excluded) { if (source == null) return {}; var target = _objectWithoutPropertiesLoose(source, excluded); var key, i; if (Object.getOwnPropertySymbols) { var sourceSymbolKeys = Object.getOwnPropertySymbols(source); for (i = 0; i < sourceSymbolKeys.length; i++) { key = sourceSymbolKeys[i]; if (excluded.indexOf(key) >= 0) continue; if (!Object.prototype.propertyIsEnumerable.call(source, key)) continue; target[key] = source[key]; } } return target; }

function _objectWithoutPropertiesLoose(source, excluded) { if (source == null) return {}; var target = {}; var sourceKeys = Object.keys(source); var key, i; for (i = 0; i < sourceKeys.length; i++) { key = sourceKeys[i]; if (excluded.indexOf(key) >= 0) continue; target[key] = source[key]; } return target; }

function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }

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

function _extends() { _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; }; return _extends.apply(this, arguments); }

function get_text(value) {
  return typeof value === "string" ? value : value && value.text ? value.text : "";
}

var Input = function Input(_ref) {
  var value = _ref.value,
      _ref$inputProps = _ref.inputProps,
      inputProps = _ref$inputProps === void 0 ? {} : _ref$inputProps,
      _ref$autocontain = _ref.autocontain,
      autocontain = _ref$autocontain === void 0 ? false : _ref$autocontain,
      _ref$readOnly = _ref.readOnly,
      readOnly = _ref$readOnly === void 0 ? false : _ref$readOnly,
      _ref$hyperlink = _ref.hyperlink,
      hyperlink = _ref$hyperlink === void 0 ? false : _ref$hyperlink,
      _ref$onRemoveTag = _ref.onRemoveTag,
      onRemoveTag = _ref$onRemoveTag === void 0 ? null : _ref$onRemoveTag,
      _ref$onClick = _ref.onClick,
      _onClick = _ref$onClick === void 0 ? null : _ref$onClick;

  var res = /*#__PURE__*/_react.default.createElement("div", {
    className: "input-tag ".concat(readOnly ? '' : 'editable')
  }, /*#__PURE__*/_react.default.createElement("ul", {
    className: "input-tag__tags"
  }, value.map(function (tag, i) {
    return /*#__PURE__*/_react.default.createElement("li", {
      key: i
    }, hyperlink ? /*#__PURE__*/_react.default.createElement("a", {
      onClick: function onClick() {
        return _onClick(tag.key);
      }
    }, tag.text) : /*#__PURE__*/_react.default.createElement("span", null, tag), readOnly ? null : /*#__PURE__*/_react.default.createElement("button", {
      type: "button",
      onClick: function onClick() {
        return !!onRemoveTag && onRemoveTag(i);
      }
    }, "\u2715"));
  }), readOnly ? null : /*#__PURE__*/_react.default.createElement("li", {
    className: "input-tag__tags__input"
  }, /*#__PURE__*/_react.default.createElement("input", _extends({
    autoFocus: true,
    type: "text"
  }, inputProps)))));

  if (autocontain) {
    return /*#__PURE__*/_react.default.createElement("div", {
      className: "input-tag-container"
    }, res);
  }

  return res;
};

exports.Input = Input;

var SingleInputSuggest = /*#__PURE__*/function (_React$Component) {
  _inherits(SingleInputSuggest, _React$Component);

  var _super = _createSuper(SingleInputSuggest);

  function SingleInputSuggest(props) {
    var _this;

    _classCallCheck(this, SingleInputSuggest);

    _this = _super.call(this, props);

    _defineProperty(_assertThisInitialized(_this), "onInputChange", function (event, _ref2) {
      var newValue = _ref2.newValue,
          method = _ref2.method;

      if (method === "click") {
        _this.props.onRowChange(_defineProperty({}, _this.props.column, newValue), true);

        _this.props.onClose();
      } else {
        var _this$props$onInputCh, _this$props;

        (_this$props$onInputCh = (_this$props = _this.props).onInputChange) === null || _this$props$onInputCh === void 0 ? void 0 : _this$props$onInputCh.call(_this$props, newValue, method);
      }
    });

    _defineProperty(_assertThisInitialized(_this), "inputKeyDown", function (event) {
      var stop = false;

      if (event.key === 'Tab' || event.key === 'Enter') {
        if (!_this.props.hyperlink || _typeof(_this.props.inputValue) === 'object') {
          _this.props.onRowChange(_defineProperty({}, _this.props.column, _this.props.inputValue), true);
        }
      } else if (['ArrowUp', 'ArrowDown'].includes(event.key) && _this.props.suggestions) {
        stop = true;
      } else if (['Escape'].includes(event.key)) {
        _this.props.onClose();
      }

      if (stop) {
        event.preventDefault();
        event.stopPropagation();
      }
    });

    _defineProperty(_assertThisInitialized(_this), "onAutoSuggestRef", function (ref) {
      if (_this.props.inputRef) {
        // @ts-ignore
        _this.props.inputRef.current = ref ? ref.input : null;

        if (ref) {
          ref.input.focus();
        }
      }
    });

    _defineProperty(_assertThisInitialized(_this), "renderSuggestion", function (suggestion) {
      return /*#__PURE__*/_react.default.createElement("div", null, _this.props.hyperlink ? /*#__PURE__*/_react.default.createElement("a", {
        onClick: function onClick() {
          var _this$props$onClick, _this$props2;

          return (_this$props$onClick = (_this$props2 = _this.props).onClick) === null || _this$props$onClick === void 0 ? void 0 : _this$props$onClick.call(_this$props2, suggestion.key);
        }
      }, suggestion.text) : suggestion);
    });

    _defineProperty(_assertThisInitialized(_this), "renderInput", function (_ref3) {
      var hyperlink = _ref3.hyperlink,
          inputProps = _objectWithoutProperties(_ref3, _excluded);

      return hyperlink ? /*#__PURE__*/_react.default.createElement("a", null, /*#__PURE__*/_react.default.createElement("input", inputProps)) : /*#__PURE__*/_react.default.createElement("input", inputProps);
    });

    _defineProperty(_assertThisInitialized(_this), "onSuggestionsFetchRequested", function () {});

    _defineProperty(_assertThisInitialized(_this), "onSuggestionsClearRequested", function () {});

    return _this;
  }

  _createClass(SingleInputSuggest, [{
    key: "componentDidMount",
    value: function componentDidMount() {
      this.props.onInputChange(this.props.value, 'mount');
    }
  }, {
    key: "componentWillUnmount",
    value: function componentWillUnmount() {
      this.props.onInputChange(null, 'unmount');
    }
  }, {
    key: "render",
    value: function render() {
      var inputProps = {
        placeholder: 'Type here',
        value: get_text(this.props.inputValue),
        onChange: this.onInputChange,
        onKeyDown: this.inputKeyDown,
        hyperlink: this.props.hyperlink
      };
      return /*#__PURE__*/_react.default.createElement("div", {
        onKeyDown: function onKeyDown(event) {
          return event.defaultPrevented && event.stopPropagation();
        }
      }, /*#__PURE__*/_react.default.createElement(_reactAutosuggest.default, {
        ref: this.onAutoSuggestRef,
        alwaysRenderSuggestions: true,
        onSuggestionsFetchRequested: this.onSuggestionsFetchRequested,
        onSuggestionsClearRequested: this.onSuggestionsClearRequested,
        suggestions: this.props.suggestions,
        renderInputComponent: this.renderInput,
        getSuggestionValue: function getSuggestionValue(val) {
          return val;
        },
        renderSuggestion: this.renderSuggestion,
        inputProps: inputProps
      }));
    }
  }]);

  return SingleInputSuggest;
}(_react.default.Component);

_defineProperty(SingleInputSuggest, "defaultProps", {
  hyperlink: false,
  suggestions: []
});

var _default = SingleInputSuggest;
exports["default"] = _default;

/***/ }),

/***/ "./lib/components/TableComponent/index.js":
/*!************************************************!*\
  !*** ./lib/components/TableComponent/index.js ***!
  \************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";


function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }

Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var _react = _interopRequireDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));

var _reactDnd = __webpack_require__(/*! react-dnd */ "webpack/sharing/consume/default/react-dnd/react-dnd");

var _reactDndHtml5Backend = _interopRequireDefault(__webpack_require__(/*! react-dnd-html5-backend */ "webpack/sharing/consume/default/react-dnd-html5-backend/react-dnd-html5-backend"));

var _reactDataGrid = _interopRequireWildcard(__webpack_require__(/*! react-data-grid */ "webpack/sharing/consume/default/react-data-grid/react-data-grid"));

__webpack_require__(/*! ./style.css */ "./lib/components/TableComponent/style.css");

var _utils = __webpack_require__(/*! ../../utils */ "./lib/utils.js");

var _DraggableHeaderRenderer = _interopRequireDefault(__webpack_require__(/*! ../DraggableHeaderRenderer */ "./lib/components/DraggableHeaderRenderer/index.js"));

var _MultiInputSuggest = _interopRequireWildcard(__webpack_require__(/*! ../MultiInputSuggest */ "./lib/components/MultiInputSuggest/index.js"));

var _SingleInputSuggest = _interopRequireDefault(__webpack_require__(/*! ../SingleInputSuggest */ "./lib/components/SingleInputSuggest/index.js"));

var _BooleanInput = _interopRequireDefault(__webpack_require__(/*! ../BooleanInput */ "./lib/components/BooleanInput/index.js"));

var _current_event = __webpack_require__(/*! ../../current_event */ "./lib/current_event.js");

var _excluded = ["row"],
    _excluded2 = ["row"],
    _excluded3 = ["formatter", "editor"];

function _getRequireWildcardCache(nodeInterop) { if (typeof WeakMap !== "function") return null; var cacheBabelInterop = new WeakMap(); var cacheNodeInterop = new WeakMap(); return (_getRequireWildcardCache = function _getRequireWildcardCache(nodeInterop) { return nodeInterop ? cacheNodeInterop : cacheBabelInterop; })(nodeInterop); }

function _interopRequireWildcard(obj, nodeInterop) { if (!nodeInterop && obj && obj.__esModule) { return obj; } if (obj === null || _typeof(obj) !== "object" && typeof obj !== "function") { return { default: obj }; } var cache = _getRequireWildcardCache(nodeInterop); if (cache && cache.has(obj)) { return cache.get(obj); } var newObj = {}; var hasPropertyDescriptor = Object.defineProperty && Object.getOwnPropertyDescriptor; for (var key in obj) { if (key !== "default" && Object.prototype.hasOwnProperty.call(obj, key)) { var desc = hasPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : null; if (desc && (desc.get || desc.set)) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } newObj.default = obj; if (cache) { cache.set(obj, newObj); } return newObj; }

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }

function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _iterableToArray(iter) { if (typeof Symbol !== "undefined" && iter[Symbol.iterator] != null || iter["@@iterator"] != null) return Array.from(iter); }

function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); enumerableOnly && (symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; })), keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = null != arguments[i] ? arguments[i] : {}; i % 2 ? ownKeys(Object(source), !0).forEach(function (key) { _defineProperty(target, key, source[key]); }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)) : ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } return target; }

function _objectWithoutProperties(source, excluded) { if (source == null) return {}; var target = _objectWithoutPropertiesLoose(source, excluded); var key, i; if (Object.getOwnPropertySymbols) { var sourceSymbolKeys = Object.getOwnPropertySymbols(source); for (i = 0; i < sourceSymbolKeys.length; i++) { key = sourceSymbolKeys[i]; if (excluded.indexOf(key) >= 0) continue; if (!Object.prototype.propertyIsEnumerable.call(source, key)) continue; target[key] = source[key]; } } return target; }

function _objectWithoutPropertiesLoose(source, excluded) { if (source == null) return {}; var target = {}; var sourceKeys = Object.keys(source); var key, i; for (i = 0; i < sourceKeys.length; i++) { key = sourceKeys[i]; if (excluded.indexOf(key) >= 0) continue; target[key] = source[key]; } return target; }

function _extends() { _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; }; return _extends.apply(this, arguments); }

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

function inputStopPropagation(event) {
  if (['ArrowLeft', 'ArrowRight'].includes(event.key)) {
    event.stopPropagation();
  }
}

var TableComponent = /*#__PURE__*/function (_React$Component) {
  _inherits(TableComponent, _React$Component);

  var _super = _createSuper(TableComponent);

  function TableComponent(_props) {
    var _this;

    _classCallCheck(this, TableComponent);

    _this = _super.call(this, _props);

    _defineProperty(_assertThisInitialized(_this), "gridRef", void 0);

    _defineProperty(_assertThisInitialized(_this), "inputRef", void 0);

    _defineProperty(_assertThisInitialized(_this), "handleMouseEnterRow", function (event, row_id) {
      _this.props.onMouseEnterRow && _this.props.onMouseEnterRow(row_id, (0, _utils.makeModKeys)(event));
    });

    _defineProperty(_assertThisInitialized(_this), "handleMouseLeaveRow", function (event, row_id) {
      _this.props.onMouseLeaveRow && _this.props.onMouseLeaveRow(row_id, (0, _utils.makeModKeys)(event));
    });

    _defineProperty(_assertThisInitialized(_this), "buildFormatter", function (type, readonly, filterable) {
      switch (type) {
        case 'hyperlink':
          return {
            editor: readonly ? null : /*#__PURE__*/_react.default.forwardRef(function (_ref, ref) {
              var row = _ref.row,
                  column = _ref.column,
                  onRowChange = _ref.onRowChange,
                  onClose = _ref.onClose;
              return /*#__PURE__*/_react.default.createElement(_SingleInputSuggest.default, {
                ref: ref,
                row_id: row[_this.props.rowKey],
                inputRef: _this.inputRef,
                value: row[column.key],
                column: column.key,
                inputValue: _this.props.inputValue,
                onInputChange: function onInputChange(value, cause) {
                  return _this.props.onInputChange(row[_this.props.rowKey], column.key, value, cause);
                },
                suggestions: _this.props.suggestions,
                onRowChange: onRowChange,
                onClose: onClose,
                hyperlink: true
              });
            }),
            headerCellClass: filterable ? "metanno-table-header-filter" : undefined,
            headerRenderer: function headerRenderer(p) {
              return /*#__PURE__*/_react.default.createElement(_DraggableHeaderRenderer.default, _extends({}, p, {
                onColumnsReorder: _this.onHeaderDrop
              }), // @ts-ignore
              p.column.filterable ? function (inputProps) {
                return /*#__PURE__*/_react.default.createElement("input", _extends({}, inputProps, {
                  className: "metanno-table-filter",
                  value: _this.props.filters[p.column.key],
                  onChange: function onChange(e) {
                    return _this.props.onFiltersChange(p.column.key, e.target.value);
                  },
                  onKeyDown: inputStopPropagation
                }));
              } : null);
            },
            formatter: function formatter(_ref2) {
              var row = _ref2.row,
                  column = _ref2.column;
              return row[column.key] ? /*#__PURE__*/_react.default.createElement("a", {
                onClick: function onClick() {
                  return _this.props.onClickCellContent(row[_this.props.rowKey], column.key, row[column.key].key);
                }
              }, row[column.key].text) : null;
            }
          };

        case 'multi-hyperlink':
          return {
            editor: readonly ? null : /*#__PURE__*/_react.default.forwardRef(function (_ref3, ref) {
              var row = _ref3.row,
                  column = _ref3.column,
                  onRowChange = _ref3.onRowChange,
                  onClose = _ref3.onClose;
              return /*#__PURE__*/_react.default.createElement(_MultiInputSuggest.default, {
                ref: ref,
                row_id: row[_this.props.rowKey],
                inputRef: _this.inputRef,
                value: row[column.key],
                inputValue: _this.props.inputValue,
                column: column.key,
                suggestions: _this.props.suggestions,
                onRowChange: onRowChange,
                onInputChange: function onInputChange(value, cause) {
                  return _this.props.onInputChange(row[_this.props.rowKey], column.key, value, cause);
                },
                onClose: onClose,
                hyperlink: true
              });
            }),
            headerCellClass: filterable ? "metanno-table-header-filter" : undefined,
            headerRenderer: function headerRenderer(p) {
              return /*#__PURE__*/_react.default.createElement(_DraggableHeaderRenderer.default, _extends({}, p, {
                onColumnsReorder: _this.onHeaderDrop
              }), // @ts-ignore
              p.column.filterable ? function (inputProps) {
                return /*#__PURE__*/_react.default.createElement("input", _extends({}, inputProps, {
                  className: "metanno-table-filter",
                  value: _this.props.filters[p.column.key],
                  onChange: function onChange(e) {
                    return _this.props.onFiltersChange(p.column.key, e.target.value);
                  },
                  onKeyDown: inputStopPropagation
                }));
              } : null);
            },
            formatter: function formatter(_ref4) {
              var row = _ref4.row,
                  props = _objectWithoutProperties(_ref4, _excluded);

              return /*#__PURE__*/_react.default.createElement(_MultiInputSuggest.InputTag, _extends({
                autocontain: true,
                readOnly: true
              }, props, {
                hyperlink: true,
                onClick: function onClick(value) {
                  return _this.props.onClickCellContent(row[_this.props.rowKey], props.column.key, value);
                },
                value: row[props.column.key]
              }));
            }
          };

        case 'text':
          return {
            editor: readonly ? null : /*#__PURE__*/_react.default.forwardRef(function (_ref5, ref) {
              var row = _ref5.row,
                  column = _ref5.column,
                  onRowChange = _ref5.onRowChange,
                  onClose = _ref5.onClose;
              return /*#__PURE__*/_react.default.createElement(_SingleInputSuggest.default, {
                ref: ref,
                row_id: row[_this.props.rowKey],
                inputRef: _this.inputRef,
                value: row[column.key],
                column: column.key,
                inputValue: _this.props.inputValue,
                onInputChange: function onInputChange(value, cause) {
                  return _this.props.onInputChange(row[_this.props.rowKey], column.key, value, cause);
                },
                suggestions: _this.props.suggestions,
                onRowChange: onRowChange,
                onClose: onClose
              });
            }),
            headerCellClass: filterable ? "metanno-table-header-filter" : undefined,
            headerRenderer: function headerRenderer(p) {
              return /*#__PURE__*/_react.default.createElement(_DraggableHeaderRenderer.default, _extends({}, p, {
                onColumnsReorder: _this.onHeaderDrop
              }), // @ts-ignore
              p.column.filterable ? function (inputProps) {
                return /*#__PURE__*/_react.default.createElement("input", _extends({}, inputProps, {
                  className: "metanno-table-filter",
                  value: _this.props.filters[p.column.key],
                  onChange: function onChange(e) {
                    return _this.props.onFiltersChange(p.column.key, e.target.value);
                  },
                  onKeyDown: inputStopPropagation
                }));
              } : null);
            },
            formatter: function formatter(_ref6) {
              var row = _ref6.row,
                  props = _objectWithoutProperties(_ref6, _excluded2);

              return /*#__PURE__*/_react.default.createElement("span", null, row[props.column.key]);
            }
          };

        case 'multi-text':
          return {
            editor: readonly ? null : /*#__PURE__*/_react.default.forwardRef(function (_ref7, ref) {
              var row = _ref7.row,
                  column = _ref7.column,
                  onRowChange = _ref7.onRowChange,
                  onClose = _ref7.onClose;
              return /*#__PURE__*/_react.default.createElement(_MultiInputSuggest.default, {
                ref: ref,
                row_id: row[_this.props.rowKey],
                inputRef: _this.inputRef,
                value: row[column.key],
                column: column.key,
                inputValue: _this.props.inputValue,
                onInputChange: function onInputChange(value, cause) {
                  return _this.props.onInputChange(row[_this.props.rowKey], column.key, value, cause);
                },
                suggestions: _this.props.suggestions,
                onRowChange: onRowChange,
                onClose: onClose
              });
            }),
            headerCellClass: filterable ? "metanno-table-header-filter" : undefined,
            headerRenderer: function headerRenderer(p) {
              return /*#__PURE__*/_react.default.createElement(_DraggableHeaderRenderer.default, _extends({}, p, {
                onColumnsReorder: _this.onHeaderDrop
              }), // @ts-ignore
              p.column.filterable ? function (inputProps) {
                return /*#__PURE__*/_react.default.createElement("input", _extends({}, inputProps, {
                  className: "metanno-table-filter",
                  value: _this.props.filters[p.column.key],
                  onChange: function onChange(e) {
                    return _this.props.onFiltersChange(p.column.key, e.target.value);
                  },
                  onKeyDown: inputStopPropagation
                }));
              } : null);
            },
            formatter: function formatter(props) {
              return /*#__PURE__*/_react.default.createElement(_MultiInputSuggest.InputTag, _extends({
                autocontain: true,
                readOnly: true
              }, props, {
                value: props.row[props.column.key]
              }));
            }
          };

        case 'boolean':
          return {
            formatter: function formatter(_ref8) {
              var row = _ref8.row,
                  column = _ref8.column,
                  onRowChange = _ref8.onRowChange,
                  isCellSelected = _ref8.isCellSelected;
              return /*#__PURE__*/_react.default.createElement(_BooleanInput.default, {
                isCellSelected: isCellSelected,
                value: row[column.key],
                onChange: function onChange(value) {
                  return onRowChange(_objectSpread(_objectSpread({}, row), {}, _defineProperty({}, column.key, value)));
                }
              });
            },
            headerCellClass: filterable ? "metanno-table-header-filter" : undefined,
            headerRenderer: function headerRenderer(p) {
              return /*#__PURE__*/_react.default.createElement(_DraggableHeaderRenderer.default, _extends({}, p, {
                onColumnsReorder: _this.onHeaderDrop
              }), // @ts-ignore
              p.column.filterable ? function (inputProps) {
                return /*#__PURE__*/_react.default.createElement("input", _extends({}, inputProps, {
                  className: "metanno-table-filter",
                  value: _this.props.filters[p.column.key],
                  onChange: function onChange(e) {
                    return _this.props.onFiltersChange(p.column.key, e.target.value);
                  },
                  onKeyDown: inputStopPropagation
                }));
              } : null);
            }
          };

        case 'button':
          return {
            formatter: function formatter(_ref9) {
              var row = _ref9.row,
                  column = _ref9.column,
                  isCellSelected = _ref9.isCellSelected;
              return /*#__PURE__*/_react.default.createElement("button", {
                onClick: function onClick() {
                  return _this.props.onClickCellContent(row[_this.props.rowKey], column.key);
                }
              }, column.key);
            }
          };

        default:
          return {};
      }
    });

    _defineProperty(_assertThisInitialized(_this), "buildColumns", (0, _utils.memoize)(function () {
      var columnObjects = _this.props.columns.map(function (column) {
        var _this$buildFormatter = _this.buildFormatter(column.type, !column.mutable, column.filterable),
            formatter = _this$buildFormatter.formatter,
            editor = _this$buildFormatter.editor,
            columnProps = _objectWithoutProperties(_this$buildFormatter, _excluded3);

        return _defineProperty({}, column.name, _objectSpread(_objectSpread(_objectSpread(_objectSpread({}, {
          key: column.name,
          name: column.name,
          draggable: true,
          resizable: true,
          editable: !!editor,
          filterable: column.filterable,
          editorOptions: {
            commitOnOutsideClick: column.type !== "hyperlink" && column.type !== "multi-hyperlink"
          }
        }), formatter ? {
          formatter: formatter
        } : {}), !!editor ? {
          editor: editor
        } : {}), columnProps));
      });

      var nameToCol = Object.assign.apply(Object, [{}].concat(_toConsumableArray(columnObjects)));
      return _toConsumableArray(_this.state.columnsOrder.map(function (name) {
        return nameToCol[name];
      }));
    }, function () {
      return {
        columns: _this.props.columns,
        columnsOrder: _this.state.columnsOrder,
        filters: _this.props.filters
      };
    }));

    _defineProperty(_assertThisInitialized(_this), "onRowsChange", function (newRows) {
      var updatedRows = newRows.map(function (newRow, i) {
        return {
          "oldRow": _this.props.rows[i],
          "newRow": newRow
        };
      }).filter(function (_ref11) {
        var newRow = _ref11.newRow,
            oldRow = _ref11.oldRow;
        return newRow !== oldRow;
      });

      if (updatedRows.length === 1) {
        var _this$props$onCellCha, _this$props;

        var _updatedRows$ = updatedRows[0],
            newRow = _updatedRows$.newRow,
            oldRow = _updatedRows$.oldRow;
        var changedKeys = Object.keys(newRow).filter(function (key) {
          return newRow[key] !== oldRow[key];
        });
        (_this$props$onCellCha = (_this$props = _this.props).onCellChange) === null || _this$props$onCellCha === void 0 ? void 0 : _this$props$onCellCha.call(_this$props, oldRow[_this.props.rowKey], changedKeys[0], newRow[changedKeys[0]]);
      }
    });

    _defineProperty(_assertThisInitialized(_this), "onHeaderDrop", function (source, target) {
      var columnSourceIndex = _this.state.columnsOrder.indexOf(source);

      var columnTargetIndex = _this.state.columnsOrder.indexOf(target);

      var reorderedColumns = _toConsumableArray(_this.state.columnsOrder);

      reorderedColumns.splice(columnTargetIndex, 0, reorderedColumns.splice(columnSourceIndex, 1)[0]);

      _this.setState(function (state) {
        return _objectSpread(_objectSpread({}, state), {}, {
          columnsOrder: []
        });
      });

      _this.setState(function (state) {
        return _objectSpread(_objectSpread({}, state), {}, {
          columnsOrder: reorderedColumns
        });
      });
    });

    _defineProperty(_assertThisInitialized(_this), "onSelectedRowsChange", function (row_ids) {
      var _this$props$onSelecte, _this$props2;

      (_this$props$onSelecte = (_this$props2 = _this.props).onSelectedRowsChange) === null || _this$props$onSelecte === void 0 ? void 0 : _this$props$onSelecte.call(_this$props2, Array.from(row_ids));
    });

    _defineProperty(_assertThisInitialized(_this), "renderRow", function (props) {
      return /*#__PURE__*/_react.default.createElement(_reactDataGrid.Row, _extends({}, props, {
        onMouseEnter: function onMouseEnter(event) {
          return _this.handleMouseEnterRow(event, props.row[_this.props.rowKey]);
        },
        onMouseLeave: function onMouseLeave(event) {
          return _this.handleMouseLeaveRow(event, props.row[_this.props.rowKey]);
        },
        className: _this.props.highlightedRows.includes(props.row[_this.props.rowKey]) ? 'metanno-row--highlighted' : ''
      }));
    });

    _defineProperty(_assertThisInitialized(_this), "rowKeyGetter", function (row) {
      return row[_this.props.rowKey];
    });

    _defineProperty(_assertThisInitialized(_this), "onBlur", function (event) {
      var _this$props$selectedP;

      if (event.currentTarget.contains(event.relatedTarget)) return;
      if (((_this$props$selectedP = _this.props.selectedPosition) === null || _this$props$selectedP === void 0 ? void 0 : _this$props$selectedP.mode) === "EDIT") return;

      _this.props.onSelectedPositionChange(null, null, "SELECT", "blur");
    });

    _defineProperty(_assertThisInitialized(_this), "handleSelectedPositionChange", function (_ref12) {
      var idx = _ref12.idx,
          rowIdx = _ref12.rowIdx,
          mode = _ref12.mode,
          _ref12$cause = _ref12.cause,
          cause = _ref12$cause === void 0 ? "key" : _ref12$cause;

      _this.props.onSelectedPositionChange(rowIdx >= 0 ? _this.props.rows[rowIdx][_this.props.rowKey] : null, idx >= 0 ? _this.state.columnsOrder[idx] : null, mode, cause);
    });

    _defineProperty(_assertThisInitialized(_this), "getSelectedPositionIndices", (0, _utils.cachedReconcile)(function (selectedPosition) {
      var _ref13 = selectedPosition || {
        row_id: null,
        col: null,
        mode: 'SELECT'
      },
          row_id = _ref13.row_id,
          col = _ref13.col,
          mode = _ref13.mode;

      var row_idx = row_id === null ? -1 : row_id ? _this.props.rows.findIndex(function (row) {
        return row[_this.props.rowKey] === row_id;
      }) : -2;
      var col_idx = col ? _this.state.columnsOrder.findIndex(function (name) {
        return col === name;
      }) : -2;
      return {
        rowIdx: row_idx,
        idx: col_idx,
        mode: mode
      };
    }));

    _this.state = {
      columnsOrder: _props.columns.map(function (column) {
        return column.name;
      })
    };
    _this.gridRef = /*#__PURE__*/_react.default.createRef();
    _this.inputRef = /*#__PURE__*/_react.default.createRef();

    _props.registerActions({
      scroll_to_row: function scroll_to_row(row_id) {
        for (var i = 0; i < _this.props.rows.length; i++) {
          if (_this.props.rows[i][_this.props.rowKey] === row_id) {
            var _this$gridRef$current;

            (_this$gridRef$current = _this.gridRef.current) === null || _this$gridRef$current === void 0 ? void 0 : _this$gridRef$current.scrollToRow(i);
          }
        }
      },
      focus: function focus() {
        var _this$inputRef$curren;

        var input = ((_this$inputRef$curren = _this.inputRef.current) === null || _this$inputRef$curren === void 0 ? void 0 : _this$inputRef$curren.input) || _this.inputRef.current;
        var event = (0, _current_event.getCurrentEvent)();
        event.preventDefault();

        if (input) {
          input.focus();
        } else {
          var _this$gridRef$current2;

          (_this$gridRef$current2 = _this.gridRef.current) === null || _this$gridRef$current2 === void 0 ? void 0 : _this$gridRef$current2.element.focus();
        }
      }
    });

    return _this;
  }

  _createClass(TableComponent, [{
    key: "render",
    value: function render() {
      var _ref14, _this$inputRef$curren2;

      (_ref14 = ((_this$inputRef$curren2 = this.inputRef.current) === null || _this$inputRef$curren2 === void 0 ? void 0 : _this$inputRef$curren2.input) || this.inputRef.current) === null || _ref14 === void 0 ? void 0 : _ref14.focus();
      return /*#__PURE__*/_react.default.createElement("div", {
        className: "metanno-table",
        onBlur: this.onBlur
      }, /*#__PURE__*/_react.default.createElement(_reactDnd.DndProvider, {
        backend: _reactDndHtml5Backend.default
      }, /*#__PURE__*/_react.default.createElement(_reactDataGrid.default, {
        ref: this.gridRef,
        rowKeyGetter: this.rowKeyGetter,
        rowHeight: 25,
        selectedPosition: this.getSelectedPositionIndices(this.props.selectedPosition),
        onSelectedPositionChange: this.handleSelectedPositionChange,
        columns: this.buildColumns(),
        rows: this.props.rows,
        rowRenderer: this.renderRow,
        headerRowHeight: this.props.columns.some(function (col) {
          return col.filterable;
        }) ? 65 : undefined // selectedRows={new Set(this.props.selectedRows)}
        // onSelectedRowsChange={this.onSelectedRowsChange}
        ,
        onRowsChange: this.onRowsChange
      })));
    }
  }]);

  return TableComponent;
}(_react.default.Component);

var _default = TableComponent;
exports["default"] = _default;

/***/ }),

/***/ "./lib/components/TextComponent/index.js":
/*!***********************************************!*\
  !*** ./lib/components/TextComponent/index.js ***!
  \***********************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";


function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }

Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var _react = _interopRequireWildcard(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));

var _tokenize = _interopRequireDefault(__webpack_require__(/*! ./tokenize */ "./lib/components/TextComponent/tokenize.js"));

var _color = _interopRequireDefault(__webpack_require__(/*! color */ "webpack/sharing/consume/default/color/color"));

var _utils = __webpack_require__(/*! ../../utils */ "./lib/utils.js");

__webpack_require__(/*! ./style.css */ "./lib/components/TextComponent/style.css");

var _excluded = ["color", "shape", "autoNestingLayout", "labelPosition"];

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _getRequireWildcardCache(nodeInterop) { if (typeof WeakMap !== "function") return null; var cacheBabelInterop = new WeakMap(); var cacheNodeInterop = new WeakMap(); return (_getRequireWildcardCache = function _getRequireWildcardCache(nodeInterop) { return nodeInterop ? cacheNodeInterop : cacheBabelInterop; })(nodeInterop); }

function _interopRequireWildcard(obj, nodeInterop) { if (!nodeInterop && obj && obj.__esModule) { return obj; } if (obj === null || _typeof(obj) !== "object" && typeof obj !== "function") { return { default: obj }; } var cache = _getRequireWildcardCache(nodeInterop); if (cache && cache.has(obj)) { return cache.get(obj); } var newObj = {}; var hasPropertyDescriptor = Object.defineProperty && Object.getOwnPropertyDescriptor; for (var key in obj) { if (key !== "default" && Object.prototype.hasOwnProperty.call(obj, key)) { var desc = hasPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : null; if (desc && (desc.get || desc.set)) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } newObj.default = obj; if (cache) { cache.set(obj, newObj); } return newObj; }

function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }

function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _iterableToArray(iter) { if (typeof Symbol !== "undefined" && iter[Symbol.iterator] != null || iter["@@iterator"] != null) return Array.from(iter); }

function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }

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

function _extends() { _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; }; return _extends.apply(this, arguments); }

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); enumerableOnly && (symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; })), keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = null != arguments[i] ? arguments[i] : {}; i % 2 ? ownKeys(Object(source), !0).forEach(function (key) { _defineProperty(target, key, source[key]); }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)) : ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _objectWithoutProperties(source, excluded) { if (source == null) return {}; var target = _objectWithoutPropertiesLoose(source, excluded); var key, i; if (Object.getOwnPropertySymbols) { var sourceSymbolKeys = Object.getOwnPropertySymbols(source); for (i = 0; i < sourceSymbolKeys.length; i++) { key = sourceSymbolKeys[i]; if (excluded.indexOf(key) >= 0) continue; if (!Object.prototype.propertyIsEnumerable.call(source, key)) continue; target[key] = source[key]; } } return target; }

function _objectWithoutPropertiesLoose(source, excluded) { if (source == null) return {}; var target = {}; var sourceKeys = Object.keys(source); var key, i; for (i = 0; i < sourceKeys.length; i++) { key = sourceKeys[i]; if (excluded.indexOf(key) >= 0) continue; target[key] = source[key]; } return target; }

function _slicedToArray(arr, i) { return _arrayWithHoles(arr) || _iterableToArrayLimit(arr, i) || _unsupportedIterableToArray(arr, i) || _nonIterableRest(); }

function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

function _iterableToArrayLimit(arr, i) { var _i = arr == null ? null : typeof Symbol !== "undefined" && arr[Symbol.iterator] || arr["@@iterator"]; if (_i == null) return; var _arr = []; var _n = true; var _d = false; var _s, _e; try { for (_i = _i.call(arr); !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"] != null) _i["return"](); } finally { if (_d) throw _e; } } return _arr; }

function _arrayWithHoles(arr) { if (Array.isArray(arr)) return arr; }

var toLuminance = function toLuminance(color) {
  var y = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 0.6;

  var _color$rgb$color = _slicedToArray(color.rgb().color, 3),
      r = _color$rgb$color[0],
      g = _color$rgb$color[1],
      b = _color$rgb$color[2]; // let y = ((0.299 * r) + ( 0.587 * g) + ( 0.114 * b)) / 255;


  var i = (0.596 * r + -0.275 * g + -0.321 * b) / 255;
  var q = (0.212 * r + -0.523 * g + 0.311 * b) / 255;
  r = (y + 0.956 * i + 0.621 * q) * 255;
  g = (y + -0.272 * i + -0.647 * q) * 255;
  b = (y + -1.105 * i + 1.702 * q) * 255; // bounds-checking

  if (r < 0) {
    r = 0;
  } else if (r > 255) {
    r = 255;
  }

  ;

  if (g < 0) {
    g = 0;
  } else if (g > 255) {
    g = 255;
  }

  ;

  if (b < 0) {
    b = 0;
  } else if (b > 255) {
    b = 255;
  }

  ;
  return _color.default.rgb(r, g, b);
};

var processStyle = function processStyle(_ref) {
  var color = _ref.color,
      shape = _ref.shape,
      autoNestingLayout = _ref.autoNestingLayout,
      labelPosition = _ref.labelPosition,
      rest = _objectWithoutProperties(_ref, _excluded);

  var colorObject = (0, _color.default)(color);
  var highlightedColor, highlightedTextColor, backgroundColor, textColor;
  highlightedColor = toLuminance(colorObject.saturate(1.), 0.6).toString();

  if (colorObject.isLight() || shape === 'underline') {
    highlightedTextColor = '#ffffffde';
    textColor = '#000000de';
    backgroundColor = colorObject.lighten(0.02).toString();
  } else {
    highlightedTextColor = '#000000de';
    textColor = '#ffffffde';
    backgroundColor = colorObject.darken(0.02).toString();
  }

  if (shape === 'underline') textColor = '#000000de';
  return {
    base: _objectSpread({
      'borderColor': color,
      'backgroundColor': shape === 'underline' ? 'transparent' : backgroundColor,
      'color': textColor
    }, rest),
    highlighted: _objectSpread({
      'borderColor': highlightedColor,
      'backgroundColor': highlightedColor,
      'color': highlightedTextColor
    }, rest),
    autoNestingLayout: autoNestingLayout,
    labelPosition: labelPosition,
    shape: shape
  };
}; // Create your Styles. Remember, since React-JSS uses the default preset,
// most plugins are available without further configuration needed.


var Token = /*#__PURE__*/_react.default.memo(function (_ref2) {
  var _styles$lastAnnotatio, _styles$lastAnnotatio2, _lastAnnotation, _lastAnnotation2;

  var text = _ref2.text,
      begin = _ref2.begin,
      end = _ref2.end,
      isFirstTokenOfChunk = _ref2.isFirstTokenOfChunk,
      isLastTokenOfChunk = _ref2.isLastTokenOfChunk,
      token_annotations = _ref2.token_annotations,
      refs = _ref2.refs,
      styles = _ref2.styles,
      handleMouseEnterSpan = _ref2.handleMouseEnterSpan,
      handleMouseLeaveSpan = _ref2.handleMouseLeaveSpan,
      handleClickSpan = _ref2.handleClickSpan;
  var hoveredKeys = (0, _react.useRef)(new Set());
  var elements = (0, _react.useRef)([]);
  var lastAnnotation = token_annotations[0];
  var labelIdx = {
    box: 0,
    underline: 0
  };
  var nLabels = {
    box: 0,
    underline: 0
  };
  var shape;
  var zIndices = {};
  token_annotations.forEach(function (a) {
    var _styles$a$style;

    if (a.mouseSelected) return;

    if (a.highlighted > lastAnnotation.highlighted || a.highlighted === lastAnnotation.highlighted && a.depth > lastAnnotation.depth) {
      lastAnnotation = a;
    }

    if (a.isFirstTokenOfSpan && a.label) if (((_styles$a$style = styles[a.style]) === null || _styles$a$style === void 0 ? void 0 : _styles$a$style.shape) !== 'underline') {
      nLabels.box++;
    } else {
      nLabels.underline++;
    }
    zIndices[a.id] = a.zIndex;
  });
  var elementsCount = 0;
  (0, _react.useEffect)(function () {
    if (elements) elements.current.length = annotations.length * 2;
  });
  var annotations = [];
  var verticalOffset = 0;

  var _loop = function _loop(annotation_i) {
    var _styles$annotation$st4;

    var annotation = token_annotations[annotation_i];
    var isUnderline = (styles === null || styles === void 0 ? void 0 : (_styles$annotation$st4 = styles[annotation.style]) === null || _styles$annotation$st4 === void 0 ? void 0 : _styles$annotation$st4.shape) === 'underline';

    if (annotation.mouseSelected) {
      annotations.push( /*#__PURE__*/_react.default.createElement("span", {
        key: "mouse-selection",
        className: "mention_token mouse_selected"
      }));
    } else {
      verticalOffset = 9 + annotation.depth * 2.5;
      annotations.push( /*#__PURE__*/_react.default.createElement("span", {
        key: "annotation-".concat(annotation_i),
        id: "span-".concat(begin, "-").concat(end) // @ts-ignore
        ,
        span_key: annotation.id,
        ref: function ref(element) {
          if (elements) elements.current[elementsCount++] = element;

          if (isFirstTokenOfChunk && refs[annotation.id]) {
            refs[annotation.id].current = element;
          }
        }
        /*onMouseEnter={(event) => handleMouseEnterSpan(event, annotation.id)}*/

        /*onMouseLeave={(event) => handleMouseLeaveSpan(event, annotation.id)}*/

        /*onMouseDown={(event) => handleClickSpan(event, annotation.id)}*/
        ,
        className: "mention_token mention_".concat(isUnderline && !annotation.highlighted ? 'underline' : 'box', "\n                               ").concat(annotation.highlighted ? 'highlighted' : '', "\n                               ").concat(annotation.selected ? 'selected' : '', "\n                               ").concat(isFirstTokenOfChunk && !annotation.openleft ? 'closedleft' : "", "\n                               ").concat(isLastTokenOfChunk && !annotation.openright ? 'closedright' : ""),
        style: _objectSpread({
          top: isUnderline && !annotation.highlighted ? 22 : verticalOffset,
          bottom: verticalOffset,
          zIndex: annotation.zIndex + 2 + (annotation.highlighted ? 50 : 0)
        }, styles[annotation.style][annotation.highlighted ? 'highlighted' : 'base'])
      }));
    }
  };

  for (var annotation_i = 0; annotation_i < token_annotations.length; annotation_i++) {
    _loop(annotation_i);
  }

  var component = /*#__PURE__*/_react.default.createElement("span", {
    className: "text-chunk" // @ts-ignore
    ,
    span_begin: begin,
    onMouseMove: token_annotations.length > 0 ? function (e) {
      if (!elements || !hoveredKeys) return;
      var newSet = new Set(elements.current.map(function (element) {
        if (!element) return;
        var rect = element.getBoundingClientRect();

        if (e.clientX >= rect.left && e.clientX <= rect.right && (token_annotations.length === 1 || e.clientY >= rect.top && e.clientY <= rect.bottom)) {
          return element.getAttribute("span_key");
        }
      }).filter(function (key) {
        return !!key;
      }));
      hoveredKeys.current.forEach(function (x) {
        return !newSet.has(x) && handleMouseLeaveSpan(e, x);
      });
      newSet.forEach(function (x) {
        return !hoveredKeys.current.has(x) && handleMouseEnterSpan(e, x);
      });
      hoveredKeys.current = newSet;
    } : null
    /*onMouseEnter={(event) => token_annotations.map(annotation => handleMouseEnterSpan(event, annotation.id))}*/
    ,
    onMouseLeave: token_annotations.length > 0 ? function (event) {
      if (!hoveredKeys) return;
      hoveredKeys.current.forEach(function (x) {
        return handleMouseLeaveSpan(event, x);
      });
      hoveredKeys.current.clear();
    } : null,
    onMouseUp: token_annotations.length > 0 ? function (e) {
      var hits = elements.current.map(function (element) {
        if (!element) return;
        var rect = element.getBoundingClientRect();

        if (e.clientX >= rect.left && e.clientX <= rect.right && (token_annotations.length === 1 || e.clientY >= rect.top && e.clientY <= rect.bottom)) {
          return element.getAttribute("span_key");
        }
      }).filter(function (key) {
        return !!key;
      }).sort(function (a, b) {
        return zIndices[b] - zIndices[a];
      });

      if (hits.length > 0) {
        handleClickSpan(e, hits[0]);
      }
    } : null
    /*style={{color: styles?.[token_annotations?.[token_annotations.length - 1]?.style]?.color}}*/

  }, annotations, /*#__PURE__*/_react.default.createElement("span", {
    className: "text-chunk-content" // @ts-ignore
    ,
    style: {
      color: styles === null || styles === void 0 ? void 0 : (_styles$lastAnnotatio = styles[(_lastAnnotation = lastAnnotation) === null || _lastAnnotation === void 0 ? void 0 : _lastAnnotation.style]) === null || _styles$lastAnnotatio === void 0 ? void 0 : (_styles$lastAnnotatio2 = _styles$lastAnnotatio[(_lastAnnotation2 = lastAnnotation) !== null && _lastAnnotation2 !== void 0 && _lastAnnotation2.highlighted ? 'highlighted' : 'base']) === null || _styles$lastAnnotatio2 === void 0 ? void 0 : _styles$lastAnnotatio2.color
    }
  }, text), isFirstTokenOfChunk && token_annotations.map(function (annotation, annotation_i) {
    if (annotation.isFirstTokenOfSpan && annotation.label) {
      var _styles$annotation$st, _styles$annotation$st2, _styles$annotation$st3, _ref3;

      shape = ((_styles$annotation$st = styles[annotation.style]) === null || _styles$annotation$st === void 0 ? void 0 : _styles$annotation$st.shape) || 'box';
      var isUnderline = styles[annotation.style].shape === 'underline';
      labelIdx[shape] += 1;
      return /*#__PURE__*/_react.default.createElement("span", {
        /*onMouseEnter={(event) => handleMouseEnterSpan(event, annotation.id)}*/

        /*onMouseLeave={(event) => handleMouseLeaveSpan(event, annotation.id)}*/

        /*onMouseDown={(event) => {handleClickSpan(event, annotation.id);}}*/
        className: "label ".concat(annotation.highlighted || annotation.selected ? 'highlighted' : ''),
        ref: function ref(element) {
          elements.current[elementsCount++] = element;
        },
        key: annotation.id // @ts-ignore
        ,
        span_key: annotation.id,
        style: (_ref3 = {
          borderColor: styles === null || styles === void 0 ? void 0 : (_styles$annotation$st2 = styles[annotation === null || annotation === void 0 ? void 0 : annotation.style]) === null || _styles$annotation$st2 === void 0 ? void 0 : (_styles$annotation$st3 = _styles$annotation$st2[annotation !== null && annotation !== void 0 && annotation.highlighted ? 'highlighted' : 'base']) === null || _styles$annotation$st3 === void 0 ? void 0 : _styles$annotation$st3.borderColor
        }, _defineProperty(_ref3, isUnderline ? 'bottom' : 'top', 0), _defineProperty(_ref3, "left", (nLabels[shape] - labelIdx[shape]) * 6 + (shape === 'box' ? -1 : 2)), _defineProperty(_ref3, "zIndex", 50 + annotation.zIndex + (annotation.highlighted ? 50 : 0)), _ref3)
      }, annotation.label.toUpperCase());
    }
  }));

  elements.current.length = elementsCount;
  return component;
});

var Line = /*#__PURE__*/_react.default.memo(function (_ref4) {
  var index = _ref4.index,
      styles = _ref4.styles,
      tokens = _ref4.tokens,
      spansRef = _ref4.spansRef,
      handleMouseEnterSpan = _ref4.handleMouseEnterSpan,
      handleMouseLeaveSpan = _ref4.handleMouseLeaveSpan,
      handleClickSpan = _ref4.handleClickSpan,
      divRef = _ref4.divRef;
  return /*#__PURE__*/_react.default.createElement("div", {
    ref: divRef,
    className: "line"
  }, /*#__PURE__*/_react.default.createElement("span", {
    className: "line-number",
    key: "line-number"
  }, index), tokens.map(function (token) {
    return /*#__PURE__*/_react.default.createElement(Token, _extends({}, token, {
      refs: spansRef,
      styles: styles,
      handleMouseEnterSpan: handleMouseEnterSpan,
      handleMouseLeaveSpan: handleMouseLeaveSpan,
      handleClickSpan: handleClickSpan
    }));
  }));
});

var TextComponent = /*#__PURE__*/function (_React$Component) {
  _inherits(TextComponent, _React$Component);

  var _super = _createSuper(TextComponent);

  function TextComponent(props) {
    var _this;

    _classCallCheck(this, TextComponent);

    _this = _super.call(this, props);

    _defineProperty(_assertThisInitialized(_this), "tokenize", void 0);

    _defineProperty(_assertThisInitialized(_this), "containerRef", void 0);

    _defineProperty(_assertThisInitialized(_this), "spansRef", void 0);

    _defineProperty(_assertThisInitialized(_this), "linesRef", void 0);

    _defineProperty(_assertThisInitialized(_this), "previousSelectedSpans", void 0);

    _defineProperty(_assertThisInitialized(_this), "processStyles", void 0);

    _defineProperty(_assertThisInitialized(_this), "handleKeyUp", function (event) {
      // if (event.metaKey || event.key === 'Meta' || event.shiftKey || event.key === 'Shift') {
      //     return;
      // }
      var key = event.key;

      if (key === 'Spacebar' || key === " ") {
        key = " ";
      }

      var spans = (0, _utils.getDocumentSelectedRanges)();

      _this.props.onKeyPress(key, (0, _utils.makeModKeys)(event), [].concat(_toConsumableArray(_this.props.mouse_selection), _toConsumableArray(spans)));
    });

    _defineProperty(_assertThisInitialized(_this), "handleKeyDown", function (event) {
      if (event.key === 'Spacebar' || event.key === " ") {
        event.preventDefault();
      }
    });

    _defineProperty(_assertThisInitialized(_this), "handleMouseUp", function (event) {
      if (event.type === "mouseup") {
        var _spans = (0, _utils.getDocumentSelectedRanges)();

        window.getSelection().removeAllRanges();

        if (_spans.length > 0) {
          //this.props.onMouseSelect([...this.props.mouse_selection, ...spans]);
          _this.props.onMouseSelect((0, _utils.makeModKeys)(event), _spans);
        } else {
          _this.props.onMouseSelect((0, _utils.makeModKeys)(event), []);
        }
      }
    });

    _defineProperty(_assertThisInitialized(_this), "handleClickSpan", function (event, span_id) {
      _this.props.onClickSpan && _this.props.onClickSpan(span_id, (0, _utils.makeModKeys)(event));
      /*event.stopPropagation();
      event.preventDefault();*/
    });

    _defineProperty(_assertThisInitialized(_this), "handleMouseEnterSpan", function (event, span_id) {
      _this.props.onMouseEnterSpan && _this.props.onMouseEnterSpan(span_id, (0, _utils.makeModKeys)(event));
    });

    _defineProperty(_assertThisInitialized(_this), "handleMouseLeaveSpan", function (event, span_id) {
      _this.props.onMouseLeaveSpan && _this.props.onMouseLeaveSpan(span_id, (0, _utils.makeModKeys)(event));
    });

    props.registerActions({
      scroll_to_line: function scroll_to_line(line) {
        if (line >= 0 && line < _this.linesRef.length) {
          var _this$linesRef$line$c;

          (_this$linesRef$line$c = _this.linesRef[line].current) === null || _this$linesRef$line$c === void 0 ? void 0 : _this$linesRef$line$c.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
          });
        }
      },
      scroll_to_span: function scroll_to_span(span_id) {
        setTimeout(function () {
          if (_this.spansRef[span_id]) {
            var _this$spansRef$span_i;

            (_this$spansRef$span_i = _this.spansRef[span_id].current) === null || _this$spansRef$span_i === void 0 ? void 0 : _this$spansRef$span_i.scrollIntoView({
              behavior: 'smooth',
              block: 'center'
            });
          }
        }, 10);
      },
      clear_current_mouse_selection: function clear_current_mouse_selection() {
        window.getSelection().removeAllRanges();
      }
    });
    _this.linesRef = [];
    _this.spansRef = {};
    _this.containerRef = /*#__PURE__*/_react.default.createRef();
    _this.previousSelectedSpans = "";
    _this.tokenize = (0, _utils.cachedReconcile)(_tokenize.default);
    _this.processStyles = (0, _utils.memoize)(function (styles) {
      return Object.assign.apply(Object, [{}].concat(_toConsumableArray(Object.keys(styles).map(function (key) {
        return _objectSpread(_objectSpread({}, styles[key]), {}, _defineProperty({}, key, processStyle(styles[key])));
      }))));
    });
    return _this;
  }

  _createClass(TextComponent, [{
    key: "render",
    value: function render() {
      var _this2 = this;

      var styles = this.processStyles(this.props.styles);
      var text = this.props.text;
      var newSelectedSpans = JSON.stringify(this.props.spans.filter(function (span) {
        return span.selected;
      }).map(function (span) {
        return span.id;
      }));

      if (newSelectedSpans != this.previousSelectedSpans) {
        document.documentElement.style.setProperty("--blink-animation", '');
        setTimeout(function () {
          document.documentElement.style.setProperty("--blink-animation", 'blink .5s step-end infinite alternate');
        }, 1);
        this.previousSelectedSpans = newSelectedSpans;
      }

      var _this$tokenize = this.tokenize([].concat(_toConsumableArray(this.props.mouse_selection.map(function (span) {
        return _objectSpread(_objectSpread({}, span), {}, {
          'mouseSelected': true
        });
      })), _toConsumableArray(this.props.spans)), text, styles),
          lines = _this$tokenize.lines,
          ids = _this$tokenize.ids; // Define the right number of references


      for (var line_i = this.linesRef.length; line_i < lines.length; line_i++) {
        this.linesRef.push( /*#__PURE__*/_react.default.createRef());
      }

      this.linesRef = this.linesRef.slice(0, lines.length);
      (0, _utils.replaceObject)(this.spansRef, Object.fromEntries(ids.map(function (id) {
        return [id, _this2.spansRef[id] || /*#__PURE__*/_react.default.createRef()];
      }))); // Return jsx elements

      return /*#__PURE__*/_react.default.createElement("div", {
        className: "span-editor",
        ref: this.containerRef,
        onMouseUp: this.handleMouseUp,
        onKeyDown: this.handleKeyDown,
        onKeyUp: this.handleKeyUp,
        tabIndex: 0
      }, /*#__PURE__*/_react.default.createElement("div", {
        className: "text"
      }, lines.map(function (tokens, lineIndex) {
        return /*#__PURE__*/_react.default.createElement(Line, {
          key: lineIndex,
          divRef: _this2.linesRef[lineIndex],
          spansRef: _this2.spansRef,
          index: lineIndex,
          tokens: tokens,
          styles: styles,
          handleMouseEnterSpan: _this2.handleMouseEnterSpan,
          handleMouseLeaveSpan: _this2.handleMouseLeaveSpan,
          handleClickSpan: _this2.handleClickSpan
        });
      })));
    }
  }]);

  return TextComponent;
}(_react.default.Component);

_defineProperty(TextComponent, "defaultProps", {
  spans: [],
  mouse_selection: [],
  text: "",
  styles: {}
});

var _default = TextComponent;
exports["default"] = _default;

/***/ }),

/***/ "./lib/components/TextComponent/tokenize.js":
/*!**************************************************!*\
  !*** ./lib/components/TextComponent/tokenize.js ***!
  \**************************************************/
/***/ (function(__unused_webpack_module, exports) {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = tokenize;
var _excluded = ["begin", "end", "label", "style"];

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); enumerableOnly && (symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; })), keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = null != arguments[i] ? arguments[i] : {}; i % 2 ? ownKeys(Object(source), !0).forEach(function (key) { _defineProperty(target, key, source[key]); }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)) : ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _createForOfIteratorHelper(o, allowArrayLike) { var it = typeof Symbol !== "undefined" && o[Symbol.iterator] || o["@@iterator"]; if (!it) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = it.call(o); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

function _objectWithoutProperties(source, excluded) { if (source == null) return {}; var target = _objectWithoutPropertiesLoose(source, excluded); var key, i; if (Object.getOwnPropertySymbols) { var sourceSymbolKeys = Object.getOwnPropertySymbols(source); for (i = 0; i < sourceSymbolKeys.length; i++) { key = sourceSymbolKeys[i]; if (excluded.indexOf(key) >= 0) continue; if (!Object.prototype.propertyIsEnumerable.call(source, key)) continue; target[key] = source[key]; } } return target; }

function _objectWithoutPropertiesLoose(source, excluded) { if (source == null) return {}; var target = {}; var sourceKeys = Object.keys(source); var key, i; for (i = 0; i < sourceKeys.length; i++) { key = sourceKeys[i]; if (excluded.indexOf(key) >= 0) continue; target[key] = source[key]; } return target; }

function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }

function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _iterableToArray(iter) { if (typeof Symbol !== "undefined" && iter[Symbol.iterator] != null || iter["@@iterator"] != null) return Array.from(iter); }

function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

function chunkText(spans, text) {
  // Find the minimum text split indices, ie the entities boundaries + split each new chunk into tokens
  var indices = [];

  for (var span_i = 0; span_i < spans.length; span_i++) {
    var _begin = spans[span_i].begin;
    var _end = spans[span_i].end;
    indices.push(_begin, _end);
  }

  indices.push(0, text.length);
  indices = _toConsumableArray(new Set(indices)).sort(function (a, b) {
    return a - b;
  });
  var text_chunks = [];
  var begin, end, text_slice;

  for (var indice_i = 1; indice_i < indices.length; indice_i++) {
    begin = indices[indice_i - 1];
    end = indices[indice_i];
    text_slice = text.slice(begin, end);
    text_chunks.push({
      begin: indices[indice_i - 1],
      end: indices[indice_i],
      label: null,
      token_annotations: [],
      tokens: text_slice.length > 0 ? text_slice.match(/\n|[^ \n]+|[ ]+/g).filter(function (text) {
        return text.length > 0;
      }) : [""]
    });
  }

  return text_chunks;
}
/**
 * Compute the layout properties of each token depending on the spans that contain it
 * To compute the depth (annotation top-bottom offsets) of box and underline annotations,
 * we iterate over spans (left to right) and find out which tokens are contained within each span.
 * For each of these tokens, we take a depth that has not been assigned to another annotation
 * and propagate it to the tokens of the span.
 *
 * To obtain underline depths, we have to reverse those depths (-1, -2, ... instead of 1, 2, 3)
 * To know which value to substract (it is not just multiplying by -1), we must cluster underlined
 * tokens together and detect the biggest depth.
 *
 * @param text_chunks
 * @param spans
 * @param styles
 */


function styleTextChunks_(text_chunks, spans, styles) {
  var isNot = function isNot(filled) {
    return !filled;
  };

  var underlineCluster = new Set();
  var underlineClusterDepth = 0;
  var rightMostOffset = 0;

  var reverseUnderlineClusterDepths = function reverseUnderlineClusterDepths() {
    underlineCluster.forEach(function (text_chunk_i) {
      text_chunks[text_chunk_i].token_annotations.forEach(function (annotation) {
        var _styles$annotation$st;

        if ((styles === null || styles === void 0 ? void 0 : (_styles$annotation$st = styles[annotation.style]) === null || _styles$annotation$st === void 0 ? void 0 : _styles$annotation$st.shape) === 'underline') {
          annotation.depth = annotation.depth - underlineClusterDepth - 1;
        }
      });
    });
  };

  spans.forEach(function (_ref, span_i) {
    var begin = _ref.begin,
        end = _ref.end,
        label = _ref.label,
        style = _ref.style,
        rest = _objectWithoutProperties(_ref, _excluded);

    var newDepth = null,
        newZIndex = null;

    if (begin >= rightMostOffset) {
      reverseUnderlineClusterDepths();
      underlineCluster.clear();
      rightMostOffset = end;
    } else if (rightMostOffset < end) {
      rightMostOffset = end;
    }

    for (var text_chunk_i = 0; text_chunk_i < text_chunks.length; text_chunk_i++) {
      if (text_chunks[text_chunk_i].begin < end && begin < text_chunks[text_chunk_i].end) {
        var _styles$style, _styles$style2;

        underlineCluster.add(text_chunk_i);

        if (text_chunks[text_chunk_i].begin === begin) {
          text_chunks[text_chunk_i].label = label;
        }

        if (newDepth === null && !rest.mouseSelected && ((_styles$style = styles[style]) === null || _styles$style === void 0 ? void 0 : _styles$style.autoNestingLayout) !== false) {
          var missingBoxDepths = [undefined];
          var missingUnderlineDepths = [undefined];
          var missingZIndices = [undefined];

          var _iterator = _createForOfIteratorHelper(text_chunks[text_chunk_i].token_annotations),
              _step;

          try {
            for (_iterator.s(); !(_step = _iterator.n()).done;) {
              var _step$value = _step.value,
                  depth = _step$value.depth,
                  zIndex = _step$value.zIndex,
                  mouseSelected = _step$value.mouseSelected,
                  tokenStyle = _step$value.style;

              if (!mouseSelected) {
                (styles[tokenStyle].shape === 'underline' ? missingUnderlineDepths : missingBoxDepths)[depth] = true;
                missingZIndices[zIndex] = true;
              }
            }
          } catch (err) {
            _iterator.e(err);
          } finally {
            _iterator.f();
          }

          newDepth = (styles[style].shape === 'underline' ? missingUnderlineDepths : missingBoxDepths).findIndex(isNot);

          if (newDepth === -1) {
            newDepth = (styles[style].shape === 'underline' ? missingUnderlineDepths : missingBoxDepths).length;
          }

          newZIndex = missingZIndices.findIndex(isNot);

          if (newZIndex === -1) {
            newZIndex = missingZIndices.length;
          }
        }

        var annotation = _objectSpread({
          depth: newDepth,
          openleft: text_chunks[text_chunk_i].begin !== begin,
          openright: text_chunks[text_chunk_i].end !== end,
          label: label,
          isFirstTokenOfSpan: text_chunks[text_chunk_i].begin === begin,
          style: style,
          zIndex: newZIndex
        }, rest);

        if ((styles === null || styles === void 0 ? void 0 : (_styles$style2 = styles[style]) === null || _styles$style2 === void 0 ? void 0 : _styles$style2.shape) === 'underline' && underlineClusterDepth < newDepth) underlineClusterDepth = newDepth;
        text_chunks[text_chunk_i].token_annotations.unshift(annotation);
      }
    }
  });
  reverseUnderlineClusterDepths();
}
/**
 * Split text chunks into multiple lines, each composed of a subset of the total text chunks
 * @param text_chunks: text chunks obtained by the `segment` function
 */


function tokenizeTextChunks(text_chunks) {
  var current_line = [];
  var all_lines = [];
  var tokens = [];

  for (var i = 0; i < text_chunks.length; i++) {
    var text_chunk = text_chunks[i];
    var begin = text_chunk.begin;
    var token_annotations = text_chunk.token_annotations;
    tokens = text_chunk.tokens;
    var offset_in_text_chunk = 0;

    for (var token_i = 0; token_i < tokens.length; token_i++) {
      var span_begin = begin + offset_in_text_chunk;
      var span_end = begin + offset_in_text_chunk + tokens[token_i].length;

      if (tokens[token_i] === "\n") {
        all_lines.push(current_line);
        current_line = [];
      } else {
        current_line.push({
          text: tokens[token_i],
          key: "".concat(span_begin, "-").concat(span_end),
          begin: span_begin,
          end: span_end,
          token_annotations: token_annotations,
          isFirstTokenOfChunk: token_i === 0,
          isLastTokenOfChunk: token_i === tokens.length - 1
        });
      }

      offset_in_text_chunk += tokens[token_i].length;
    }
  }

  if (current_line.length > 0 || tokens.length && tokens[tokens.length - 1] === "\n") {
    all_lines.push(current_line);
  }

  return all_lines;
}

function tokenize(spans, text, styles) {
  // Sort the original spans to display
  spans = spans.sort(function (_ref2, _ref3) {
    var begin_a = _ref2.begin,
        end_a = _ref2.end,
        mouseSelected_a = _ref2.mouseSelected;
    var begin_b = _ref3.begin,
        end_b = _ref3.end,
        mouseSelected_b = _ref3.mouseSelected;
    return mouseSelected_a === mouseSelected_b ? begin_a !== begin_b ? begin_a - begin_b : end_b - end_a : mouseSelected_a ? -1 : 1;
  }).map(function (span) {
    return _objectSpread(_objectSpread({}, span), {}, {
      text: text.slice(span.begin, span.end)
    });
  });
  var text_chunks = chunkText(spans, text);
  styleTextChunks_(text_chunks, spans, styles);
  var ids = spans.map(function (span) {
    return span.id;
  });
  var linesOfTokens = tokenizeTextChunks(text_chunks);
  return {
    lines: linesOfTokens,
    ids: ids
  }; //.filter(({ token_annotations }) => token_annotations.length > 0);
}

/***/ }),

/***/ "./lib/components/Toolbar/index.js":
/*!*****************************************!*\
  !*** ./lib/components/Toolbar/index.js ***!
  \*****************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";


function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }

Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var _react = _interopRequireDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));

__webpack_require__(/*! ./style.css */ "./lib/components/Toolbar/style.css");

var _color = _interopRequireDefault(__webpack_require__(/*! color */ "webpack/sharing/consume/default/color/color"));

var _excluded = ["type"];

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _objectWithoutProperties(source, excluded) { if (source == null) return {}; var target = _objectWithoutPropertiesLoose(source, excluded); var key, i; if (Object.getOwnPropertySymbols) { var sourceSymbolKeys = Object.getOwnPropertySymbols(source); for (i = 0; i < sourceSymbolKeys.length; i++) { key = sourceSymbolKeys[i]; if (excluded.indexOf(key) >= 0) continue; if (!Object.prototype.propertyIsEnumerable.call(source, key)) continue; target[key] = source[key]; } } return target; }

function _objectWithoutPropertiesLoose(source, excluded) { if (source == null) return {}; var target = {}; var sourceKeys = Object.keys(source); var key, i; for (i = 0; i < sourceKeys.length; i++) { key = sourceKeys[i]; if (excluded.indexOf(key) >= 0) continue; target[key] = source[key]; } return target; }

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

var Button = function Button(_ref) {
  var label = _ref.label,
      secondary = _ref.secondary,
      color = _ref.color,
      onMouseDown = _ref.onMouseDown;
  var hsl = (0, _color.default)(color).hsl(); // hsl.color[2] = Math.max(hsl.color[2], 60);

  return /*#__PURE__*/_react.default.createElement("div", {
    className: "toolbar-button"
  }, /*#__PURE__*/_react.default.createElement("div", {
    className: "bp3-button bp3-minimal toolbar-button-component button",
    onMouseDown: onMouseDown
  }, /*#__PURE__*/_react.default.createElement("div", {
    style: {
      background: hsl.toString(),
      color: hsl.isLight() ? '#464646' : 'white'
    },
    className: "toolbar-button-text"
  }, /*#__PURE__*/_react.default.createElement("span", null, label)), secondary ? /*#__PURE__*/_react.default.createElement("div", {
    style: {
      background: 'white',
      color: "#464646"
    },
    className: "toolbar-button-secondary"
  }, /*#__PURE__*/_react.default.createElement("span", null, secondary)) : null));
};

var Spacer = function Spacer() {
  return /*#__PURE__*/_react.default.createElement("div", {
    className: "toolbar-spacer"
  });
};

var Toolbar = /*#__PURE__*/function (_React$Component) {
  _inherits(Toolbar, _React$Component);

  var _super = _createSuper(Toolbar);

  function Toolbar(_props) {
    var _this;

    _classCallCheck(this, Toolbar);

    _this = _super.call(this, _props);

    _defineProperty(_assertThisInitialized(_this), "renderComponent", function (_ref2, idx) {
      var type = _ref2.type,
          props = _objectWithoutProperties(_ref2, _excluded);

      if (type === "button") return /*#__PURE__*/_react.default.createElement(Button, {
        label: props.label,
        color: props.color,
        secondary: props.secondary,
        onMouseDown: function onMouseDown() {
          return _this.props.onButtonPress(idx);
        }
      });else if (type === "spacer") {
        return /*#__PURE__*/_react.default.createElement(Spacer, null);
      } else {
        throw Error("Unkown toolbar component type \"".concat(type, "\""));
      }
    });

    return _this;
  }

  _createClass(Toolbar, [{
    key: "render",
    value: function render() {
      return /*#__PURE__*/_react.default.createElement("div", {
        className: "toolbar toolbar-wrap"
      }, /*#__PURE__*/_react.default.createElement("div", {
        className: "toolbar-content"
      }, this.props.buttons.map(this.renderComponent)));
    }
  }]);

  return Toolbar;
}(_react.default.Component);

exports["default"] = Toolbar;

_defineProperty(Toolbar, "defaultProps", {
  buttons: []
});

/***/ }),

/***/ "./lib/containers/TableView/index.js":
/*!*******************************************!*\
  !*** ./lib/containers/TableView/index.js ***!
  \*******************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";


function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }

Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var _react = _interopRequireWildcard(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));

var _reactRedux = __webpack_require__(/*! react-redux */ "webpack/sharing/consume/default/react-redux/react-redux");

var _TableComponent = _interopRequireDefault(__webpack_require__(/*! ../../components/TableComponent */ "./lib/components/TableComponent/index.js"));

var _Toolbar = _interopRequireDefault(__webpack_require__(/*! ../../components/Toolbar */ "./lib/components/Toolbar/index.js"));

var _Loading = _interopRequireDefault(__webpack_require__(/*! ../../components/Loading */ "./lib/components/Loading/index.js"));

var _utils = __webpack_require__(/*! ../../utils */ "./lib/utils.js");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _getRequireWildcardCache(nodeInterop) { if (typeof WeakMap !== "function") return null; var cacheBabelInterop = new WeakMap(); var cacheNodeInterop = new WeakMap(); return (_getRequireWildcardCache = function _getRequireWildcardCache(nodeInterop) { return nodeInterop ? cacheNodeInterop : cacheBabelInterop; })(nodeInterop); }

function _interopRequireWildcard(obj, nodeInterop) { if (!nodeInterop && obj && obj.__esModule) { return obj; } if (obj === null || _typeof(obj) !== "object" && typeof obj !== "function") { return { default: obj }; } var cache = _getRequireWildcardCache(nodeInterop); if (cache && cache.has(obj)) { return cache.get(obj); } var newObj = {}; var hasPropertyDescriptor = Object.defineProperty && Object.getOwnPropertyDescriptor; for (var key in obj) { if (key !== "default" && Object.prototype.hasOwnProperty.call(obj, key)) { var desc = hasPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : null; if (desc && (desc.get || desc.set)) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } newObj.default = obj; if (cache) { cache.set(obj, newObj); } return newObj; }

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); enumerableOnly && (symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; })), keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = null != arguments[i] ? arguments[i] : {}; i % 2 ? ownKeys(Object(source), !0).forEach(function (key) { _defineProperty(target, key, source[key]); }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)) : ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

var TableView = function TableView(_ref) {
  var id = _ref.id,
      className = _ref.className,
      onKeyPress = _ref.onKeyPress,
      onClickCellContent = _ref.onClickCellContent,
      onSelectedPositionChange = _ref.onSelectedPositionChange,
      registerActions = _ref.registerActions,
      onFiltersChange = _ref.onFiltersChange,
      onSelectedRowsChange = _ref.onSelectedRowsChange,
      onMouseEnterRow = _ref.onMouseEnterRow,
      onMouseLeaveRow = _ref.onMouseLeaveRow,
      _onButtonPress = _ref.onButtonPress,
      onCellChange = _ref.onCellChange,
      onInputChange = _ref.onInputChange,
      selectEditorState = _ref.selectEditorState;

  var _useSelector = (0, _reactRedux.useSelector)((0, _react.useCallback)((0, _utils.cachedReconcile)(function (state) {
    var derived = null;

    if (selectEditorState && state) {
      derived = selectEditorState(state, id);
    }

    return derived ? _objectSpread(_objectSpread({
      rows: [],
      columns: [],
      rowKey: '',
      buttons: [],
      selectedCells: [],
      styles: [],
      filters: {},
      suggestions: [],
      selectedRows: [],
      selectedPosition: {},
      highlightedRows: [],
      inputValue: undefined
    }, derived), {}, {
      loading: false
    }) : {
      loading: true
    };
  }), [id, selectEditorState])),
      rows = _useSelector.rows,
      rowKey = _useSelector.rowKey,
      columns = _useSelector.columns,
      buttons = _useSelector.buttons,
      loading = _useSelector.loading,
      inputValue = _useSelector.inputValue,
      filters = _useSelector.filters,
      suggestions = _useSelector.suggestions,
      selectedRows = _useSelector.selectedRows,
      selectedPosition = _useSelector.selectedPosition,
      highlightedRows = _useSelector.highlightedRows;

  if (loading) {
    return /*#__PURE__*/_react.default.createElement("div", {
      className: "container is-loading"
    }, /*#__PURE__*/_react.default.createElement(_Loading.default, null));
  }

  return /*#__PURE__*/_react.default.createElement("div", {
    className: "container ".concat(buttons.length > 0 ? "has-toolbar" : '', " ").concat(className)
  }, buttons.length > 0 ? /*#__PURE__*/_react.default.createElement(_Toolbar.default, {
    buttons: buttons,
    onButtonPress: function onButtonPress(idx) {
      return _onButtonPress(idx);
    }
  }) : null, /*#__PURE__*/_react.default.createElement(_TableComponent.default, {
    id: id,
    rows: rows,
    selectedRows: selectedRows,
    highlightedRows: highlightedRows,
    columns: columns,
    filters: filters,
    rowKey: rowKey,
    inputValue: inputValue,
    suggestions: suggestions,
    selectedPosition: selectedPosition,
    onKeyPress: onKeyPress,
    onMouseEnterRow: onMouseEnterRow,
    onMouseLeaveRow: onMouseLeaveRow,
    onFiltersChange: onFiltersChange,
    onSelectedRowsChange: onSelectedRowsChange,
    onSelectedPositionChange: onSelectedPositionChange,
    onClickCellContent: onClickCellContent,
    onCellChange: onCellChange,
    onInputChange: onInputChange,
    registerActions: registerActions
  }));
};

var _default = TableView;
exports["default"] = _default;

/***/ }),

/***/ "./lib/containers/TextView/index.js":
/*!******************************************!*\
  !*** ./lib/containers/TextView/index.js ***!
  \******************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";


function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }

Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports["default"] = void 0;

var _react = _interopRequireWildcard(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));

var _reactRedux = __webpack_require__(/*! react-redux */ "webpack/sharing/consume/default/react-redux/react-redux");

var _TextComponent = _interopRequireDefault(__webpack_require__(/*! ../../components/TextComponent */ "./lib/components/TextComponent/index.js"));

var _Toolbar = _interopRequireDefault(__webpack_require__(/*! ../../components/Toolbar */ "./lib/components/Toolbar/index.js"));

var _Loading = _interopRequireDefault(__webpack_require__(/*! ../../components/Loading */ "./lib/components/Loading/index.js"));

var _utils = __webpack_require__(/*! ../../utils */ "./lib/utils.js");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _getRequireWildcardCache(nodeInterop) { if (typeof WeakMap !== "function") return null; var cacheBabelInterop = new WeakMap(); var cacheNodeInterop = new WeakMap(); return (_getRequireWildcardCache = function _getRequireWildcardCache(nodeInterop) { return nodeInterop ? cacheNodeInterop : cacheBabelInterop; })(nodeInterop); }

function _interopRequireWildcard(obj, nodeInterop) { if (!nodeInterop && obj && obj.__esModule) { return obj; } if (obj === null || _typeof(obj) !== "object" && typeof obj !== "function") { return { default: obj }; } var cache = _getRequireWildcardCache(nodeInterop); if (cache && cache.has(obj)) { return cache.get(obj); } var newObj = {}; var hasPropertyDescriptor = Object.defineProperty && Object.getOwnPropertyDescriptor; for (var key in obj) { if (key !== "default" && Object.prototype.hasOwnProperty.call(obj, key)) { var desc = hasPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : null; if (desc && (desc.get || desc.set)) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } newObj.default = obj; if (cache) { cache.set(obj, newObj); } return newObj; }

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); enumerableOnly && (symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; })), keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = null != arguments[i] ? arguments[i] : {}; i % 2 ? ownKeys(Object(source), !0).forEach(function (key) { _defineProperty(target, key, source[key]); }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)) : ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

var TextView = function TextView(_ref) {
  var id = _ref.id,
      _onButtonPress = _ref.onButtonPress,
      onKeyPress = _ref.onKeyPress,
      onClickSpan = _ref.onClickSpan,
      onMouseEnterSpan = _ref.onMouseEnterSpan,
      onMouseLeaveSpan = _ref.onMouseLeaveSpan,
      onMouseSelect = _ref.onMouseSelect,
      registerActions = _ref.registerActions,
      selectEditorState = _ref.selectEditorState;

  var _useSelector = (0, _reactRedux.useSelector)((0, _react.useCallback)((0, _utils.cachedReconcile)(function (state) {
    var derived = null;

    if (selectEditorState && state) {
      derived = selectEditorState(state, id);
    }

    return derived ? _objectSpread(_objectSpread({
      text: '',
      spans: [],
      mouse_selection: [],
      buttons: [],
      styles: []
    }, derived), {}, {
      loading: false
    }) : {
      loading: true
    };
  }), [id, selectEditorState])),
      spans = _useSelector.spans,
      text = _useSelector.text,
      mouse_selection = _useSelector.mouse_selection,
      buttons = _useSelector.buttons,
      styles = _useSelector.styles,
      loading = _useSelector.loading;

  if (loading) {
    return /*#__PURE__*/_react.default.createElement("div", {
      className: "container is-loading"
    }, /*#__PURE__*/_react.default.createElement(_Loading.default, null));
  }

  return /*#__PURE__*/_react.default.createElement("div", {
    className: "container ".concat(buttons.length > 0 ? "has-toolbar" : '')
  }, buttons.length > 0 ? /*#__PURE__*/_react.default.createElement(_Toolbar.default, {
    buttons: buttons,
    onButtonPress: function onButtonPress(idx) {
      return _onButtonPress(idx, mouse_selection);
    }
  }) : null, /*#__PURE__*/_react.default.createElement(_TextComponent.default, {
    id: id,
    spans: spans,
    text: text,
    styles: styles,
    mouse_selection: mouse_selection,
    onKeyPress: onKeyPress,
    onClickSpan: onClickSpan,
    onMouseEnterSpan: onMouseEnterSpan,
    onMouseLeaveSpan: onMouseLeaveSpan,
    onMouseSelect: onMouseSelect //mouse_selection => this.setState(state => ({...state, mouse_selection}))}
    ,
    registerActions: registerActions
  }));
};

var _default = TextView;
exports["default"] = _default;

/***/ }),

/***/ "./lib/current_event.js":
/*!******************************!*\
  !*** ./lib/current_event.js ***!
  \******************************/
/***/ (function(__unused_webpack_module, exports) {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.getCurrentEvent = getCurrentEvent;
exports.setCurrentEvent = setCurrentEvent;
var current_event = {
  current: null
};
document.addEventListener("click", setCurrentEvent, {
  capture: true
});
document.addEventListener("mousedown", setCurrentEvent, {
  capture: true
});
document.addEventListener("mouseup", setCurrentEvent, {
  capture: true
});

function getCurrentEvent() {
  return current_event.current;
}

function setCurrentEvent(event) {
  current_event.current = event;
}

/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.cachedReconcile = cachedReconcile;
exports.getDocumentSelectedRanges = getDocumentSelectedRanges;
Object.defineProperty(exports, "isEqual", ({
  enumerable: true,
  get: function get() {
    return _reactFastCompare.default;
  }
}));
exports.memoize = exports.makeModKeys = void 0;
exports.reconcile = reconcile;
exports.shallowCompare = exports.replaceObject = void 0;

var _reactFastCompare = _interopRequireDefault(__webpack_require__(/*! react-fast-compare */ "webpack/sharing/consume/default/react-fast-compare/react-fast-compare"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }

var shallowCompare = function shallowCompare(obj1, obj2) {
  return obj1 === obj2 || _typeof(obj1) === 'object' && _typeof(obj2) == 'object' && obj1 !== null && obj2 !== null && Object.keys(obj1).length === Object.keys(obj2).length && Object.keys(obj1).every(function (key) {
    return obj2.hasOwnProperty(key) && obj1[key] === obj2[key];
  });
};

exports.shallowCompare = shallowCompare;

var replaceObject = function replaceObject(obj, new_obj) {
  Object.keys(obj).forEach(function (key) {
    delete obj[key];
  });
  Object.assign(obj, new_obj);
};

exports.replaceObject = replaceObject;

var memoize = function memoize(factory) {
  var checkDeps = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : function () {
    return arguments.length > 0 ? arguments.length <= 0 ? undefined : arguments[0] : null;
  };
  var shallow = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
  var post = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : false;
  var last = null;
  var cache = null;
  return function () {
    if (post) {
      var new_state = factory.apply(void 0, arguments);

      if (!(shallow && shallowCompare(new_state, cache) || !shallow && (0, _reactFastCompare.default)(new_state, cache))) {
        cache = new_state;
      }

      return cache;
    } else {
      var state = checkDeps.apply(void 0, arguments);

      if (!(shallow && shallowCompare(last, state) && last !== null || !shallow && (0, _reactFastCompare.default)(last, state) && last !== null)) {
        last = state;
        cache = factory.apply(void 0, arguments);
      }

      return cache;
    }
  };
};

exports.memoize = memoize;

var makeModKeys = function makeModKeys(event) {
  var modkeys = [];
  if (event.shiftKey) modkeys.push("Shift");
  if (event.metaKey) modkeys.push("Meta");
  if (event.ctrlKey) modkeys.push("Control");
  return modkeys;
};

exports.makeModKeys = makeModKeys;

function internalReconcile(a, b) {
  // 7.1. All identical values are equivalent, as determined by ===.
  if (a === b) {
    return true;
  }

  var typeA = _typeof(a);

  var typeB = _typeof(b);

  if (typeA !== typeB) {
    return false;
  } // 7.3. Other pairs that do not both pass typeof value == 'object', equivalence is determined by ==.


  if (!a || !b || typeA !== "object" && typeB !== "object") {
    return a == b; // eslint-disable-line eqeqeq
  }

  if (Object.isFrozen(a)) {
    return false;
  }

  var i, key;

  if (a === null || b === null) {
    return false;
  }

  var ka = Object.keys(a);
  var kb = Object.keys(b);
  var has_diff = ka.length !== kb.length;

  for (i = kb.length - 1; i >= 0; i--) {
    key = kb[i];

    if (internalReconcile(a[key], b[key])) {
      a[key] = b[key];
    } else {
      has_diff = true;
    }
  }

  return !has_diff;
}

function reconcile(a, b) {
  var reconciled = internalReconcile(a, b);
  return reconciled ? b : a;
}
/**
 * Reconciles the previous and the new output of a function call
 * to maximize referential equality (===) between any item of the output object
 * This allows React to quickly detect parts of the state that haven't changed
 * when the state selectors are monolithic blocks, as in our case.
 *
 * For instance
 * ```es6
 * func = cachedReconcile((value) => {a: {subkey: 3}, b: value})
 * res4 = func(4)
 * res5 = func(5)
 * res4 !== res5 (the object has changed)
 * res4['a'] === res5['a'] (but the 'a' entry has not)
 * ```
 * @param fn: Function whose output we want to cache
 */


function cachedReconcile(fn) {
  var cache = null;
  return function () {
    var a = fn.apply(void 0, arguments);
    var reconciled = internalReconcile(a, cache);
    cache = reconciled ? cache : a;
    return cache;
  };
}

function getDocumentSelectedRanges() {
  var ranges = [];
  var range = null;

  var get_span_begin = function get_span_begin(range) {
    var _range$getAttribute;

    return (range === null || range === void 0 ? void 0 : (_range$getAttribute = range.getAttribute) === null || _range$getAttribute === void 0 ? void 0 : _range$getAttribute.call(range, "span_begin")) || range.parentElement.getAttribute("span_begin") || range.parentElement.parentElement.getAttribute("span_begin");
  };

  if (window.getSelection) {
    var selection = window.getSelection();
    var begin = null,
        end = null;

    for (var i = 0; i < selection.rangeCount; i++) {
      range = selection.getRangeAt(i);
      var startContainerBegin = parseInt( // @ts-ignore
      get_span_begin(range.startContainer), 10);
      var endContainerBegin = parseInt( // @ts-ignore
      get_span_begin(range.endContainer), 10);

      if (!isNaN(startContainerBegin)) {
        begin = range.startOffset + startContainerBegin;
      }

      if (!isNaN(endContainerBegin)) {
        end = range.endOffset + endContainerBegin;
      }

      if (isNaN(startContainerBegin) || isNaN(endContainerBegin)) {
        continue;
      }

      if (begin !== end) {
        ranges.push({
          begin: begin,
          end: end
        });
      }
    }

    if (ranges.length === 0 && !isNaN(begin) && begin !== null && !isNaN(end) && end !== null && begin !== end) {
      ranges.push({
        begin: begin,
        end: end
      });
    }

    return ranges;
  } else {
    // @ts-ignore
    if (document.selection && document.selection.type !== "Control") {}
  }

  return ranges;
}

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./lib/components/BooleanInput/style.css":
/*!*************************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./lib/components/BooleanInput/style.css ***!
  \*************************************************************************************/
/***/ (function(module, exports, __webpack_require__) {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".rdg-checkbox-container {\n    display: flex;\n    height: 100%;\n    align-items: center;\n    justify-content: center;\n}\n\n.rdg-checkbox-container > .rdg-checkbox-label {\n    position: relative;\n}", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./lib/components/Loading/style.css":
/*!********************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./lib/components/Loading/style.css ***!
  \********************************************************************************/
/***/ (function(module, exports, __webpack_require__) {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".container.is-loading {\n    min-height: 100px;\n}\n\n.loading {\n    fill: var(--jp-ui-font-color1);\n    stop-color: var(--jp-ui-font-color1);\n    color: var(--jp-ui-font-color1);\n}\n\n.loading svg stop {\n    stop-color: var(--jp-ui-font-color1);\n}\n\n.loading svg circle {\n    fill: var(--jp-ui-font-color1);\n}", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./lib/components/MultiInputSuggest/style.css":
/*!******************************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./lib/components/MultiInputSuggest/style.css ***!
  \******************************************************************************************/
/***/ (function(module, exports, __webpack_require__) {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".react-autosuggest__container, .input-tag-container {\n    position: relative;\n    height: 100%;\n    /*width: 282px;*/\n    margin: 0 auto;\n    display: flex;\n    align-items: center;\n}\n\n.rdg-editor-container > div > .react-autosuggest__container {\n    padding-left: 8px;\n    padding-right: 8px;\n    margin-right: 1px;\n    background: white;\n    /*border-bottom: 1px solid #dddddd;*/\n    box-sizing: border-box;\n}\n\n.react-autosuggest__input {\n}\n\n.react-autosuggest__input::-ms-clear {\n    display: none;\n}\n\n.react-autosuggest__input--open {\n    border-bottom-left-radius: 0;\n    border-bottom-right-radius: 0;\n}\n\n.react-autosuggest__input--focused {\n    outline: none;\n}\n\n.react-autosuggest__suggestions-container {\n    display: none;\n}\n\n.rdg-editor-container > div {\n    /*background: white;*/\n}\n\n.rdg-editor-container > div, .rdg-cell-value, .rdg-cell-value > div {\n    height: 100%;\n    width: 100%;\n}\n\n.rdg-editor-container > div > .react-autosuggest__container--open > .react-autosuggest__suggestions-container {\n    left: -1px;\n    right: 0px;\n}\n.react-autosuggest__suggestions-container--open {\n    display: block;\n    position: absolute;\n    top: 100%;\n    min-width: 100%;\n    box-sizing: border-box;\n    border: 1px solid #aaa;\n    background-color: #fff;\n    font-family: 'Open Sans', sans-serif;\n    font-weight: 300;\n    font-size: 14px;\n    border-bottom-left-radius: 4PX;\n    border-bottom-right-radius: 4PX;\n    z-index: 2;\n    max-height: 200px;\n    overflow-y: auto;\n}\n\n.react-autosuggest__suggestions-list {\n    margin: 0;\n    padding: 0;\n    list-style-type: none;\n}\n\n.react-autosuggest__suggestion {\n    cursor: pointer;\n    padding: 5px 5px;\n}\n\n.react-autosuggest__suggestion--highlighted {\n    background-color: #ddd;\n}\n\n.react-autosuggest__section-container {\n    border-top: 1px dashed #ccc;\n}\n\n.react-autosuggest__section-container-first {\n    border-top: 0;\n}\n\n.react-autosuggest__section-title {\n    padding: 10px 0 0 10px;\n    font-size: 12px;\n    color: #777;\n}\n\n.input-tag {\n    /*border: 1px solid #d6d6d6;\n    border-radius: 2px;*/\n    display: flex;\n    flex-wrap: nowrap;\n    width: 100%;\n    /*padding: 2px;*/\n}\n\n.input-tag.editable {\n    background: white;\n}\n\n.input-tag input {\n    border: none;\n    width: 100%;\n\n    /*height: 30px;\n    padding: 10px 20px;*/\n    font-family: 'Open Sans', sans-serif;\n    font-weight: 300;\n    font-size: 14px;\n    border-radius: 4PX;\n    -webkit-appearance: none;\n}\n\n.input-tag input:focus {\n    outline: none;\n}\n\nul.input-tag__tags {\n    display: inline-flex;\n    flex-wrap: nowrap;\n    /*padding: 0 2px;*/\n    padding: 2px 8px;\n    margin: 0 -8px;\n    width: 100%;\n    overflow: scroll;\n    -ms-overflow-style: none;\n}\n\n/* Hide scrollbar for Chrome, Safari and Opera */\n.input-tag__tags::-webkit-scrollbar {\n  display: none;\n}\n\n/* Hide scrollbar for IE and Edge */\n.example {\n}\n\n.input-tag__tags li {\n    align-items: center;\n    background: white;\n    border-radius: 2px;\n    color: black;\n    display: flex;\n    font-size: 14px;\n    line-height: 15px;\n    font-weight: 300;\n    list-style: none;\n    margin-right: 2px;\n    padding: 1px 5px;\n    position: relative;\n}\n\n.input-tag__tags li button {\n    align-items: center;\n    appearance: none;\n    background: #333333;\n    border: none;\n    border-radius: 50%;\n    color: white;\n    cursor: pointer;\n    display: inline-flex;\n    font-size: 10px;\n    height: 15px;\n    justify-content: center;\n    line-height: 0;\n    margin-left: 8px;\n    /*transform: rotate(45deg);*/\n    width: 15px;\n    flex: 0 0 15px;\n    padding: 0px;\n}\n.input-tag__tags li button:focus {\n    outline: none;\n}\n\n\n.input-tag__tags li:not(.input-tag__tags__input) {\n    border: 1px solid #b3b3b3;\n}\n\n.input-tag__tags li.input-tag__tags__input {\n    background: none;\n    flex-grow: 1;\n    flex-basis: 50%;\n    min-width: 60px;\n    flex-shrink: 0;\n    padding: 0;\n}", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./lib/components/SingleInputSuggest/style.css":
/*!*******************************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./lib/components/SingleInputSuggest/style.css ***!
  \*******************************************************************************************/
/***/ (function(module, exports, __webpack_require__) {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".rdg-cell .rdg-editor-container > div > .react-autosuggest__container {\n    padding-left: 8px;\n    padding-right: 8px;\n    background: transparent;\n    /*border-bottom: 1px solid #dddddd;*/\n    margin-right: 0px;\n    /*border-right: 1px solid #dddddd;*/\n    box-sizing: border-box;\n}\n\n.rdg-cell .react-autosuggest__input {\n    font-family: inherit;\n    border: none;\n    padding-left: 0;\n    font-size: 14px;\n    width: 100%;\n    height: 100%;\n    color: var(--jp-ui-font-color1);\n    background: transparent;\n}\n\n.rdg-cell .react-autosuggest__input::-ms-clear {\n    display: none;\n}\n\n.rdg-cell .react-autosuggest__input--open {\n    border-bottom-left-radius: 0;\n    border-bottom-right-radius: 0;\n}\n\n.rdg-cell .react-autosuggest__input--focused {\n    outline: none;\n}\n\n.rdg-cell .react-autosuggest__suggestions-container {\n    display: none;\n}\n\n.rdg-cell .rdg-editor-container > div {\n    /*background: white;*/\n}\n\n.rdg-editor-container > div, .rdg-cell-value, .rdg-cell-value > div {\n    height: 100%;\n    width: 100%;\n}\n\n.rdg-editor-container > div > .react-autosuggest__container--open > .react-autosuggest__suggestions-container {\n    left: -1px;\n    right: 0px;\n}\n\n.rdg-cell .react-autosuggest__suggestions-container--open {\n    display: block;\n    position: absolute;\n    top: 100%;\n    min-width: 100%;\n    box-sizing: border-box;\n    border: 1px solid #aaa;\n    background-color: #fff;\n    font-family: 'Open Sans', sans-serif;\n    font-weight: 300;\n    font-size: 14px;\n    border-bottom-left-radius: 4PX;\n    border-bottom-right-radius: 4PX;\n    z-index: 2;\n    max-height: 200px;\n    overflow-y: auto;\n\n    overflow-y: scroll;\n    scrollbar-width: none; /* Firefox */\n    -ms-overflow-style: none; /* Internet Explorer 10+ */\n}\n\n.rdg-cell .react-autosuggest__suggestions-container--open::-webkit-scrollbar {\n    width: 0;\n    height: 0;\n}\n\n.rdg-cell .react-autosuggest__suggestions-list {\n    margin: 0;\n    padding: 0;\n    list-style-type: none;\n}\n\n.rdg-cell .react-autosuggest__suggestion {\n    cursor: pointer;\n    padding: 5px 5px;\n}\n\n.rdg-cell .react-autosuggest__suggestion--highlighted {\n    background-color: #ddd;\n}\n\n.rdg-cell .react-autosuggest__section-container {\n    border-top: 1px dashed #ccc;\n}\n\n.rdg-cell .react-autosuggest__section-container-first {\n    border-top: 0;\n}\n\n.rdg-cell .react-autosuggest__section-title {\n    padding: 10px 0 0 10px;\n    font-size: 12px;\n    color: #777;\n}", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./lib/components/TableComponent/style.css":
/*!***************************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./lib/components/TableComponent/style.css ***!
  \***************************************************************************************/
/***/ (function(module, exports, __webpack_require__) {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".jp-Notebook .metanno-table {\n    min-height: 300px;\n}\n\n.metanno-table {\n    height: 100%;\n    width: 100%;\n    overflow: hidden;\n}\n\n.metanno-table-filter {\n    inline-size: 100%;\n    padding: 4px;\n    font-size: 14px;\n    background: var(--jp-input-background);\n    color: var(--jp-ui-font-color0);\n    border: 1px solid var(--jp-input-border-color)\n}\n\n.metanno-table-header-filter {\n    line-height: 30px;\n    padding: 0;\n}\n\n.metanno-table-header-filter > div > div {\n    padding-block: 0;\n    padding-inline: 4px;\n}\n\n.metanno-table-header-filter > div > div:first-child {\n    border-block-end: 1px solid var(--rdg-border-color);\n    padding-inline: 8px;\n}\n\n.metanno-table > div {\n    height: 100%;\n}\n\n.metanno-table a {\n    color: #106ba3;\n}\n\n.metanno-table a:hover {\n    text-decoration: underline;\n}\n\n.metanno-table .rdg-cell-mask:focus {\n    outline: none;\n}\n\n.metanno-table .react-tagsinput {\n    background: transparent;\n    border: none;\n    padding-top: 0;\n    padding-bottom: 0;\n}\n\n.metanno-table .react-tagsinput > span {\n    line-height: 14px;\n}\n\n.metanno-table .react-tagsinput-tag, .metanno-table .react-tagsinput-input {\n    padding-top: 0;\n    padding-bottom: 0;\n    margin-top: 0;\n    margin-bottom: 0;\n}\n\n.metanno-table .react-tagsinput-tag {\n    background-color: #ffffff;\n    border-radius: 2px;\n    border: 1px solid #4a9bd2;\n    color: #000000;\n}\n\n.metanno-table .react-tagsinput-input:focus {\n    outline: none;\n}\n\n.metanno-table .react-tagsinput.disabled .react-tagsinput-input {\n    display: none;\n}\n\n\n.metanno-tagscell-container {\n\n}\n\n.rdg-row.metanno-row--highlighted {\n    background-color: var(--row-hover-background-color);\n}\n\n.metanno-table .rdg-row, .metanno-table .rdg-cell {\n    contain: initial;\n    overflow: visible;\n}\n\n.metanno-table .rdg-cell {\n    position: relative;\n}\n\n/* TAGS INPUT */\n.react-tagsinput {\n    background-color: #fff;\n    border: 1px solid #ccc;\n    overflow: hidden;\n    padding-left: 5px;\n    padding-top: 5px;\n}\n\n.react-tagsinput--focused {\n    border-color: #a5d24a;\n}\n\n.react-tagsinput-tag {\n    background-color: #cde69c;\n    border-radius: 2px;\n    border: 1px solid #a5d24a;\n    color: #638421;\n    display: inline-block;\n    font-family: sans-serif;\n    font-size: 13px;\n    font-weight: 400;\n    margin-bottom: 5px;\n    margin-right: 5px;\n    padding: 5px;\n}\n\n.react-tagsinput-remove {\n    cursor: pointer;\n    font-weight: bold;\n}\n\n.react-tagsinput-tag a::before {\n    content: \" ×\";\n}\n\n.react-tagsinput-input {\n    background: transparent;\n    border: 0;\n    color: #777;\n    font-family: sans-serif;\n    font-size: 13px;\n    font-weight: 400;\n    margin-bottom: 6px;\n    margin-top: 1px;\n    outline: none;\n    padding: 5px;\n    width: 80px;\n}\n\n.rdg-cell > button {\n    width: 100%;\n    cursor: pointer;\n    outline: none;\n    -webkit-appearance: none;\n    -moz-appearance: none;\n    color: black;\n    padding: 0;\n    background: #f8f8f8;\n    border: none;\n    box-shadow: var(--jp-toolbar-box-shadow);\n    border-radius: 2px 2px 2px 2px;\n}\n\n.rdg-cell-editing {\n    padding: 0\n}\n\n.rdg-cell:focus, .rdg-cell[aria-selected=true] {\n    outline: 0\n}\n\n.metanno-table > div {\n    overflow-y: scroll;\n    scrollbar-width: none; /* Firefox */\n    -ms-overflow-style: none;  /* Internet Explorer 10+ */\n}\n.metanno-table > div::-webkit-scrollbar { /* WebKit */\n    width: 0;\n    height: 0;\n}\n", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./lib/components/TextComponent/style.css":
/*!**************************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./lib/components/TextComponent/style.css ***!
  \**************************************************************************************/
/***/ (function(module, exports, __webpack_require__) {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
exports.push([module.id, "@import url(//fonts.googleapis.com/css?family=Roboto+Mono&display=swap);"]);
exports.push([module.id, "@import url(//cdn.jsdelivr.net/npm/hack-font@3/build/web/hack.css);"]);
// Module
exports.push([module.id, ".span-editor {\n    font-family: sans-serif;\n    text-align: left;\n    overflow-y: scroll;\n    overflow-x: hidden;\n    height: 100%;\n    width: 100%;\n}\n\n.text {\n    font-family: Verdana, Arial, sans-serif;\n    /*font-family: 'Menlo', 'Hack', 'DejaVu Sans Mono', 'Roboto Mono', monospace;*/\n    font-size: 0.92em;\n    margin-top: 10px;\n    margin-bottom: 5px;\n    line-height: 2.8em;\n    color: var(--jp-ui-font-color1);\n    position: relative;\n\n    width: 100%;\n    overflow-x: hidden;\n}\n\n.line {\n    padding-left: 41px;\n    box-sizing: border-box;\n    width: 100%;\n    overflow-x: hidden;\n}\n\n.line-number {\n    margin-left: -41px;\n    width: 0;\n    display: inline-block;\n    padding: 0 30px 0 11px;\n    color: #959da5;\n}\n\n.rdg.rdg.rdg {\n    --color: var(--jp-content-font-color0);\n    --border-color: var(--jp-border-color2);\n    --summary-border-color: var(--jp-border-color2);\n    --background-color: var(--jp-layout-color0);\n    --header-background-color: var(--jp-layout-color2);\n    --row-hover-background-color: var(--jp-rendermime-table-row-hover-background);\n    --row-selected-background-color: var(--jp-rendermime-table-row-hover-background);\n    --row-selected-hover-background-color: var(--jp-rendermime-table-row-hover-background);\n    --checkbox-color: var(--jp-private-notebook-selected-color);\n    --checkbox-focus-color: var(--jp-rendermime-table-row-hover-background);\n    --checkbox-disabled-border-color: black;\n    --checkbox-disabled-background-color: #333;\n}\n\n.rdg-cell a, .rdg-cell span {\n    width: 100%;\n    display: inline-block;\n    text-overflow: ellipsis;\n    overflow: hidden;\n}\n\n.line-number,\n.label {\n    -webkit-touch-callout: none; /* iOS Safari */\n    -webkit-user-select: none; /* Safari */\n    -khtml-user-select: none; /* Konqueror HTML */\n    -moz-user-select: none; /* Old versions of Firefox */\n    -ms-user-select: none; /* Internet Explorer/Edge */\n    user-select: none; /* Non-prefixed version, currently supported by Chrome, Opera and Firefox */\n}\n\n.text-chunk {\n    word-break: break-word;\n    white-space: pre-wrap;\n    display: inline-block;\n    position: relative;\n}\n\n.text-chunk-content {\n    position: relative;\n    z-index: 1001;\n}\n\n.mention_token {\n    box-sizing: content-box;\n    border-radius: 0.0000001em;\n    display: inline-block;\n\n    pointer-events: none;\n    position: absolute;\n    background-color: var(--background-color);\n    border-color: var(--border-color);\n    left: 0px;\n    right: 0px;\n    border-width: 2px;\n    border-style: solid;\n    border-right-width: 0;\n    border-left-width: 0;\n}\n\n.label {\n    box-sizing: content-box;\n    position: absolute;\n    white-space: pre;\n    border-radius: 0.2em;\n    font-size: 0.6em;\n    padding: 0.5em 0.1em 0em;\n    background: white;\n    line-height: 0em;\n    height: 0.4em;\n    pointer-events: none;\n    background: var(--jp-layout-color0);\n    color: var(--jp-ui-font-color1);\n    border: 2px solid var(--jp-ui-font-color1);\n}\n\n.mention_token.mention_underline, .mention_token.mention_underline.closed_left, .mention_token.mention_underline.closed_right {\n    top: unset;\n    border-top: 0;\n    border-top-left-radius: 0;\n    border-top-right-radius: 0;\n}\n\n.mention_token.closedleft {\n    left: -1px;\n    border-left-width: 2px;\n    border-top-left-radius: 2px;\n    border-bottom-left-radius: 2px;\n}\n\n.mention_token.closedright {\n    right: -1px;\n    border-right-width: 2px;\n    border-top-right-radius: 2px;\n    border-bottom-right-radius: 2px;\n}\n\n.mention_token.highlighted {\n    border-top-width: 4px;\n    border-bottom-width: 4px;\n}\n\n.mention_token.mention_underline, .mention_token.closedright.mention_underline, .mention_token.closedleft.mention_underline {\n    right: -2px;\n    border-top: 0;\n    border-top-left-radius: 0;\n    border-top-right-radius: 0;\n}\n\n.mention_token.closedleft.highlighted {\n    border-left-width: 4px;\n    left: -2px;\n}\n\n.mouse_selected {\n    line-height: 2.2em;\n    background: rgba(137, 188, 250, 0.6); /*#b2d7ff88;*/\n    border: none;\n    top: 0;\n    bottom: 0;\n    z-index: 1000;\n}\n\n@keyframes blink {\n    from, to {\n        border-color: white\n    }\n    50% {\n        border-color: black\n    }\n}\n\n.mention_token.selected {\n    animation: var(--blink-animation);\n}\n/*.text.select_mode .mention_token.hover {\n  filter: invert(100%);\n}*/\n", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./lib/components/Toolbar/style.css":
/*!********************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./lib/components/Toolbar/style.css ***!
  \********************************************************************************/
/***/ (function(module, exports, __webpack_require__) {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ":root {\n    --metanno-toolbar-item-height: 2em;\n    --metanno-toolbar-spacing: 4px;\n}\n\n.toolbar {\n    display: flex;\n    width: 100%;\n\n    box-sizing: border-box;\n    color: var(--jp-ui-font-color1);\n    overflow: auto;\n\n    border-bottom: var(--jp-border-width) solid var(--jp-toolbar-border-color);\n    box-shadow: var(--jp-toolbar-box-shadow);\n    padding: var(--metanno-toolbar-spacing);\n    z-index: 1;\n}\n\n.toolbar-content {\n    flex: 1;\n    display: flex;\n    flex-direction: row;\n    gap: var(--metanno-toolbar-spacing);\n}\n\n.toolbar.toolbar-wrap .toolbar-content {\n    flex-wrap: wrap;\n}\n\n.toolbar.toolbar-wrap {\n    overflow: unset;\n}\n\n.toolbar-spacer {\n    margin: calc((-1) * var(--metanno-toolbar-spacing)) calc(2 * var(--metanno-toolbar-spacing)) calc((-1) * var(--metanno-toolbar-spacing)) var(--metanno-toolbar-spacing);\n    /*width: 1px;\n    background: #dadada;*/\n}\n\n.toolbar div.toolbar-button {\n    display: flex;\n    flex-direction: row;\n    align-items: stretch;\n    height: var(--metanno-toolbar-item-height);\n\n    box-sizing: border-box;\n    outline: none;\n    -webkit-appearance: none;\n    -moz-appearance: none;\n    margin-right: var(--metanno-toolbar-spacing);\n\n    color: transparent;\n\n    padding: 0;\n    /*line-height: var(--jp-private-toolbar-height);*/\n    border: none; /*1px solid var(--jp-toolbar-border-color);*/\n    box-shadow: var(--jp-toolbar-box-shadow);\n    border-radius: 2px 2px 2px 2px;\n}\n\n.toolbar-button:hover {\n    filter: brightness(90%);\n}\n\n.toolbar-button > .toolbar-button-component {\n    display: flex;\n    flex-direction: row;\n    align-items: stretch;\n    flex: 1;\n\n    background: var(--jp-layout-color1);\n    padding: 0 0px;\n    font-size: 1em;\n    /* height: 24px; */\n    border-radius: 0;\n\n    text-align: center;\n    min-width: unset;\n    min-height: unset;\n}\n\n.button {\n    font-family: 'Open Sans', serif;\n    font-family: -apple-system, BlinkMacSystemFont, \"Helvetica Neue\", YuGothic, \"ヒラギノ角ゴ ProN W3\", Hiragino Kaku Gothic ProN, Arial, \"メイリオ\", Meiryo, sans-serif;\n}\n\n.container {\n    height: 100%;\n    position: relative;\n    box-sizing: border-box;\n    display: flex;\n    align-items: stretch;\n    flex-direction: column;\n}\n\n.toolbar-button > .toolbar-button-component > .toolbar-button-text,\n.toolbar-button > .toolbar-button-component > .toolbar-button-secondary {\n    display: flex;\n    flex-direction: row;\n    align-items: center;\n    padding: 0 6px;\n    margin: 0;\n    white-space: nowrap;\n\n    font-weight: 700;\n}\n\n.toolbar-button > .toolbar-button-component > .toolbar-button-text {\n    flex: 1;\n    justify-content: center;\n}\n\n.toolbar-button > .toolbar-button-component > .toolbar-button-secondary {\n    flex-grow: 0;\n}\n\n.toolbar-button > .toolbar-button-component > :last-child {\n    border-bottom-right-radius: 2px;\n    border-top-right-radius: 2px;\n    overflow: hidden;\n}\n\n.toolbar-button > .toolbar-button-component > :first-child {\n    border-bottom-left-radius: 2px;\n    border-top-left-radius: 2px;\n    overflow: hidden;\n}\n\n.toolbar-button > .toolbar-button-component > span {\n    line-height: 0;\n}\n\n\n.toolbar {\n    scrollbar-width: none; /* Firefox */\n    -ms-overflow-style: none; /* Internet Explorer 10+ */\n}\n\n.toolbar::-webkit-scrollbar { /* WebKit */\n    width: 0;\n    height: 0;\n}", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./lib/components/BooleanInput/style.css":
/*!***********************************************!*\
  !*** ./lib/components/BooleanInput/style.css ***!
  \***********************************************/
/***/ (function(module, __unused_webpack_exports, __webpack_require__) {


var content = __webpack_require__(/*! !!../../../node_modules/css-loader/dist/cjs.js!./style.css */ "./node_modules/css-loader/dist/cjs.js!./lib/components/BooleanInput/style.css");

if(typeof content === 'string') content = [[module.id, content, '']];

var transform;
var insertInto;



var options = {"hmr":true}

options.transform = transform
options.insertInto = undefined;

var update = __webpack_require__(/*! !../../../node_modules/style-loader/lib/addStyles.js */ "./node_modules/style-loader/lib/addStyles.js")(content, options);

if(content.locals) module.exports = content.locals;

if(false) {}

/***/ }),

/***/ "./lib/components/Loading/style.css":
/*!******************************************!*\
  !*** ./lib/components/Loading/style.css ***!
  \******************************************/
/***/ (function(module, __unused_webpack_exports, __webpack_require__) {


var content = __webpack_require__(/*! !!../../../node_modules/css-loader/dist/cjs.js!./style.css */ "./node_modules/css-loader/dist/cjs.js!./lib/components/Loading/style.css");

if(typeof content === 'string') content = [[module.id, content, '']];

var transform;
var insertInto;



var options = {"hmr":true}

options.transform = transform
options.insertInto = undefined;

var update = __webpack_require__(/*! !../../../node_modules/style-loader/lib/addStyles.js */ "./node_modules/style-loader/lib/addStyles.js")(content, options);

if(content.locals) module.exports = content.locals;

if(false) {}

/***/ }),

/***/ "./lib/components/MultiInputSuggest/style.css":
/*!****************************************************!*\
  !*** ./lib/components/MultiInputSuggest/style.css ***!
  \****************************************************/
/***/ (function(module, __unused_webpack_exports, __webpack_require__) {


var content = __webpack_require__(/*! !!../../../node_modules/css-loader/dist/cjs.js!./style.css */ "./node_modules/css-loader/dist/cjs.js!./lib/components/MultiInputSuggest/style.css");

if(typeof content === 'string') content = [[module.id, content, '']];

var transform;
var insertInto;



var options = {"hmr":true}

options.transform = transform
options.insertInto = undefined;

var update = __webpack_require__(/*! !../../../node_modules/style-loader/lib/addStyles.js */ "./node_modules/style-loader/lib/addStyles.js")(content, options);

if(content.locals) module.exports = content.locals;

if(false) {}

/***/ }),

/***/ "./lib/components/SingleInputSuggest/style.css":
/*!*****************************************************!*\
  !*** ./lib/components/SingleInputSuggest/style.css ***!
  \*****************************************************/
/***/ (function(module, __unused_webpack_exports, __webpack_require__) {


var content = __webpack_require__(/*! !!../../../node_modules/css-loader/dist/cjs.js!./style.css */ "./node_modules/css-loader/dist/cjs.js!./lib/components/SingleInputSuggest/style.css");

if(typeof content === 'string') content = [[module.id, content, '']];

var transform;
var insertInto;



var options = {"hmr":true}

options.transform = transform
options.insertInto = undefined;

var update = __webpack_require__(/*! !../../../node_modules/style-loader/lib/addStyles.js */ "./node_modules/style-loader/lib/addStyles.js")(content, options);

if(content.locals) module.exports = content.locals;

if(false) {}

/***/ }),

/***/ "./lib/components/TableComponent/style.css":
/*!*************************************************!*\
  !*** ./lib/components/TableComponent/style.css ***!
  \*************************************************/
/***/ (function(module, __unused_webpack_exports, __webpack_require__) {


var content = __webpack_require__(/*! !!../../../node_modules/css-loader/dist/cjs.js!./style.css */ "./node_modules/css-loader/dist/cjs.js!./lib/components/TableComponent/style.css");

if(typeof content === 'string') content = [[module.id, content, '']];

var transform;
var insertInto;



var options = {"hmr":true}

options.transform = transform
options.insertInto = undefined;

var update = __webpack_require__(/*! !../../../node_modules/style-loader/lib/addStyles.js */ "./node_modules/style-loader/lib/addStyles.js")(content, options);

if(content.locals) module.exports = content.locals;

if(false) {}

/***/ }),

/***/ "./lib/components/TextComponent/style.css":
/*!************************************************!*\
  !*** ./lib/components/TextComponent/style.css ***!
  \************************************************/
/***/ (function(module, __unused_webpack_exports, __webpack_require__) {


var content = __webpack_require__(/*! !!../../../node_modules/css-loader/dist/cjs.js!./style.css */ "./node_modules/css-loader/dist/cjs.js!./lib/components/TextComponent/style.css");

if(typeof content === 'string') content = [[module.id, content, '']];

var transform;
var insertInto;



var options = {"hmr":true}

options.transform = transform
options.insertInto = undefined;

var update = __webpack_require__(/*! !../../../node_modules/style-loader/lib/addStyles.js */ "./node_modules/style-loader/lib/addStyles.js")(content, options);

if(content.locals) module.exports = content.locals;

if(false) {}

/***/ }),

/***/ "./lib/components/Toolbar/style.css":
/*!******************************************!*\
  !*** ./lib/components/Toolbar/style.css ***!
  \******************************************/
/***/ (function(module, __unused_webpack_exports, __webpack_require__) {


var content = __webpack_require__(/*! !!../../../node_modules/css-loader/dist/cjs.js!./style.css */ "./node_modules/css-loader/dist/cjs.js!./lib/components/Toolbar/style.css");

if(typeof content === 'string') content = [[module.id, content, '']];

var transform;
var insertInto;



var options = {"hmr":true}

options.transform = transform
options.insertInto = undefined;

var update = __webpack_require__(/*! !../../../node_modules/style-loader/lib/addStyles.js */ "./node_modules/style-loader/lib/addStyles.js")(content, options);

if(content.locals) module.exports = content.locals;

if(false) {}

/***/ })

}]);
//# sourceMappingURL=lib_containers_TableView_index_js-lib_containers_TextView_index_js-webpack_sharing_consume_de-5d1d96.4a382cfb77e17b001562.js.map