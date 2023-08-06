"use strict";

function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.notebookIcon = exports.default = exports.contextToMetannoManagerRegistry = exports.MetannoArea = void 0;
exports.registerMetannoManager = registerMetannoManager;

require("regenerator-runtime/runtime");

var _algorithm = require("@lumino/algorithm");

var _properties = require("@lumino/properties");

var _disposable = require("@lumino/disposable");

var _services = require("@jupyterlab/services");

var _docmanager = require("@jupyterlab/docmanager");

var _mainmenu = require("@jupyterlab/mainmenu");

var _logconsole = require("@jupyterlab/logconsole");

var _rendermime = require("@jupyterlab/rendermime");

var _apputils = require("@jupyterlab/apputils");

var _notebook = require("@jupyterlab/notebook");

var _settingregistry = require("@jupyterlab/settingregistry");

var _application = require("@jupyterlab/application");

var _uiComponents = require("@jupyterlab/ui-components");

var _widgets = require("@lumino/widgets");

var _coreutils = require("@lumino/coreutils");

var _manager = _interopRequireDefault(require("./manager"));

var _renderer = _interopRequireDefault(require("./renderer"));

var _icon = _interopRequireDefault(require("../icon.svg"));

require("./dontDisplayHiddenOutput");

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
exports.default = _default;