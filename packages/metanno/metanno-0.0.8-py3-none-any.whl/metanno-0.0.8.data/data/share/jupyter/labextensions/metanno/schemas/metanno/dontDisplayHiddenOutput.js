"use strict";

var _outputarea = require("@jupyterlab/outputarea");

var _cells = require("@jupyterlab/cells");

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