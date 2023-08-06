'use strict';
(self['webpackChunkjupyterlab_voice_control'] =
  self['webpackChunkjupyterlab_voice_control'] || []).push([
  ['lib_index_js'],
  {
    /***/ './lib/commands.js':
      /*!*************************!*\
  !*** ./lib/commands.js ***!
  \*************************/
      /***/ (
        __unused_webpack_module,
        __webpack_exports__,
        __webpack_require__
      ) => {
        __webpack_require__.r(__webpack_exports__);
        /* harmony export */ __webpack_require__.d(__webpack_exports__, {
          /* harmony export */ deleteText: () => /* binding */ deleteText,
          /* harmony export */ moveCursor: () => /* binding */ moveCursor,
          /* harmony export */ scrollBy: () => /* binding */ scrollBy,
          /* harmony export */ typeText: () => /* binding */ typeText
          /* harmony export */
        });
        function moveCursor(options) {
          const focused = document.activeElement;
          if (!focused) {
            return 'Cannot move cursor: no element is focused';
          }
          if (typeof focused.value !== 'undefined') {
            const input = focused;
            if (options.to === 'start') {
              input.setSelectionRange(0, 0);
              input.focus();
            }
            if (options.to === 'end') {
              const end = input.value.length;
              input.setSelectionRange(end, end);
              input.focus();
            }
          }
        }
        function typeText(options) {
          if (typeof options.text === 'undefined') {
            return 'No text provided';
          }
          const focused = document.activeElement;
          if (!focused) {
            return 'Cannot type: no element is focused';
          }
          if (typeof focused.value !== 'undefined') {
            focused.value += options.text;
          } else {
            for (const key of options.text) {
              console.log(key.charCodeAt(0), key);
              focused.dispatchEvent(
                new KeyboardEvent('keydown', {
                  key: key,
                  keyCode: key.charCodeAt(0),
                  code: key,
                  shiftKey: false,
                  ctrlKey: false,
                  metaKey: false,
                  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
                  // @ts-ignore
                  which: key.charCodeAt(0)
                })
              );
            }
          }
        }
        function deleteText(options) {
          if (typeof options.what === 'undefined') {
            return 'No "what" argument provided';
          }
          const focused = document.activeElement;
          if (!focused) {
            return 'Cannot delete: no element is focused';
          }
          if (typeof focused.value !== 'undefined') {
            const value = focused.value;
            const lastSpace = value.lastIndexOf(' ');
            focused.value = value.substring(0, lastSpace);
          }
        }
        function scrollBy(options) {
          const focused = document.activeElement;
          if (!focused) {
            return 'Cannot scroll: no element is focused';
          }
          if (options.behavior == null) {
            options.behavior = 'smooth';
          }
          focused.scrollBy({
            top: ((options.topPercent || 0) / 100) * window.innerHeight,
            left: ((options.leftPercent || 0) / 100) * window.innerWidth,
            behavior: options.behavior
          });
        }

        /***/
      },

    /***/ './lib/components/status.js':
      /*!**********************************!*\
  !*** ./lib/components/status.js ***!
  \**********************************/
      /***/ (
        __unused_webpack_module,
        __webpack_exports__,
        __webpack_require__
      ) => {
        __webpack_require__.r(__webpack_exports__);
        /* harmony export */ __webpack_require__.d(__webpack_exports__, {
          /* harmony export */ VoiceControlStatusIndicator: () =>
            /* binding */ VoiceControlStatusIndicator
          /* harmony export */
        });
        /* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ =
          __webpack_require__(
            /*! react */ 'webpack/sharing/consume/default/react'
          );
        /* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default =
          /*#__PURE__*/ __webpack_require__.n(
            react__WEBPACK_IMPORTED_MODULE_0__
          );
        /* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ =
          __webpack_require__(
            /*! @jupyterlab/apputils */ 'webpack/sharing/consume/default/@jupyterlab/apputils'
          );
        /* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default =
          /*#__PURE__*/ __webpack_require__.n(
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__
          );
        /* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_2__ =
          __webpack_require__(
            /*! @jupyterlab/statusbar */ 'webpack/sharing/consume/default/@jupyterlab/statusbar'
          );
        /* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_2___default =
          /*#__PURE__*/ __webpack_require__.n(
            _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_2__
          );
        /* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_3__ =
          __webpack_require__(/*! ../icons */ './lib/icons.js');

        class VoiceControlStatusIndicator extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
          constructor(signal, trans, controller) {
            super();
            this.signal = signal;
            this.trans = trans;
            this.controller = controller;
          }
          render() {
            return react__WEBPACK_IMPORTED_MODULE_0__.createElement(
              _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.UseSignal,
              { signal: this.signal },
              (sender, status) => {
                if (!status) {
                  status = {
                    enabled: false
                  };
                }
                const icon = status.enabled
                  ? _icons__WEBPACK_IMPORTED_MODULE_3__.recognitionEnabledIcon
                  : _icons__WEBPACK_IMPORTED_MODULE_3__.recognitionDisabledIcon;
                const text = this.trans.__(
                  'Last voice recognition result: %1 with confidence %2',
                  status.lastResult,
                  status.lastConfidence
                );
                const shortText = this.trans.__(
                  '%1 (%2%)',
                  status.lastResult,
                  status.lastConfidence
                    ? Math.round(status.lastConfidence * 100)
                    : '?'
                );
                const controller = this.controller;
                return react__WEBPACK_IMPORTED_MODULE_0__.createElement(
                  _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_2__.GroupItem,
                  {
                    spacing: 0,
                    title: text,
                    onClick: () => {
                      controller.isEnabled
                        ? controller.disable()
                        : controller.enable();
                    }
                  },
                  react__WEBPACK_IMPORTED_MODULE_0__.createElement(icon.react, {
                    top: '2px',
                    kind: 'statusBar'
                  }),
                  status.error || status.lastResult
                    ? react__WEBPACK_IMPORTED_MODULE_0__.createElement(
                        _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_2__.TextItem,
                        {
                          className: 'status-message',
                          source: status.error ? status.error : shortText
                        }
                      )
                    : react__WEBPACK_IMPORTED_MODULE_0__.createElement(
                        'div',
                        null
                      )
                );
              }
            );
          }
        }

        /***/
      },

    /***/ './lib/controller.js':
      /*!***************************!*\
  !*** ./lib/controller.js ***!
  \***************************/
      /***/ (
        __unused_webpack_module,
        __webpack_exports__,
        __webpack_require__
      ) => {
        __webpack_require__.r(__webpack_exports__);
        /* harmony export */ __webpack_require__.d(__webpack_exports__, {
          /* harmony export */ VoiceController: () =>
            /* binding */ VoiceController
          /* harmony export */
        });
        /* harmony import */ var fastest_levenshtein__WEBPACK_IMPORTED_MODULE_0__ =
          __webpack_require__(
            /*! fastest-levenshtein */ 'webpack/sharing/consume/default/fastest-levenshtein/fastest-levenshtein'
          );
        /* harmony import */ var fastest_levenshtein__WEBPACK_IMPORTED_MODULE_0___default =
          /*#__PURE__*/ __webpack_require__.n(
            fastest_levenshtein__WEBPACK_IMPORTED_MODULE_0__
          );
        /* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__ =
          __webpack_require__(
            /*! @lumino/signaling */ 'webpack/sharing/consume/default/@lumino/signaling'
          );
        /* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1___default =
          /*#__PURE__*/ __webpack_require__.n(
            _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__
          );
        /* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ =
          __webpack_require__(
            /*! @jupyterlab/apputils */ 'webpack/sharing/consume/default/@jupyterlab/apputils'
          );
        /* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default =
          /*#__PURE__*/ __webpack_require__.n(
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__
          );

        function normalise(text) {
          return text.toLowerCase().trim();
        }
        const ordinals = {
          first: 1,
          second: 2,
          third: 3,
          fourth: 4,
          fifth: 5
        };
        class VoiceController {
          constructor(commandRegistry, trans, palette) {
            this.commandRegistry = commandRegistry;
            this.trans = trans;
            this.speak = false;
            this.commands = [];
            this.suggestionThreshold = 1;
            this.counter = 0;
            this._currentSuggestions = [];
            this.statusChanged =
              new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
            const SpeechRecognition =
              window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {
              (0,
              _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showErrorMessage)(
                trans.__('Speach recognition not supported'),
                trans.__('Your browser does not support speech recognition.')
              );
              throw Error('Not supported');
            }
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = true;
            this.recognition.interimResults = false;
            this.recognition.maxAlternatives = 1;
            this.confidenceThreshold = 0;
            this._status = {
              enabled: false
            };
            // TODO: interim results, synonyms, translations, docs
            // TODO: undo runs "filebrowser:undo" in notebook - need to update the prefered based on context!
            this.jupyterCommands = new Map();
            this.recognition.onresult = this.handleSpeechResult.bind(this);
            this.recognition.onspeechend = event => {
              console.log('speech end');
              this.disable();
            };
            this.recognition.onerror = event => {
              const title = 'Speech recognition not available';
              switch (event.error) {
                case 'audio-capture':
                  (0,
                  _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showErrorMessage)(
                    title,
                    'Microphone not detected'
                  );
                  break;
                case 'not-allowed':
                  (0,
                  _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showErrorMessage)(
                    title,
                    'Access to microphone was denied or blocked'
                  );
                  break;
                case 'no-speech':
                  this._status.error = this.trans.__('No speech was detected');
                  break;
              }
            };
            commandRegistry.commandChanged.connect(() => {
              this.updateGrammar();
            });
            this.updateGrammar();
          }
          matchPhrase(phrase) {
            // First try to match against our voice commands which get a higher priority
            for (const command of this.commands) {
              const match = phrase.match(new RegExp(command.phrase, 'i'));
              if (match != null) {
                if (!this.commandRegistry.hasCommand(command.command)) {
                  this.communicate(
                    this.trans.__(
                      'Matched "%1" phrase but command "%2" is not in the registry',
                      command.phrase,
                      command.command
                    )
                  );
                  return [];
                }
                const args = Object.assign({}, command.arguments);
                if (match.groups) {
                  Object.assign(args, match.groups);
                }
                this.commandRegistry.execute(command.command, args);
                return [];
              }
            }
            // If it did not succeed, match against all JupyterLab commands
            const command = this.jupyterCommands.get(phrase);
            if (command) {
              this.commandRegistry.execute(command.id);
              return [];
            } else {
              let best = 999;
              let bestCandidates = [];
              for (const [
                candidateLabel,
                command
              ] of this.jupyterCommands.entries()) {
                const matchScore = Math.min(
                  (0,
                  fastest_levenshtein__WEBPACK_IMPORTED_MODULE_0__.distance)(
                    candidateLabel,
                    phrase
                  ),
                  (0,
                  fastest_levenshtein__WEBPACK_IMPORTED_MODULE_0__.distance)(
                    normalise(command.caption),
                    phrase
                  )
                );
                if (matchScore < best) {
                  best = matchScore;
                  bestCandidates = [command];
                } else if (matchScore === best) {
                  bestCandidates.push(command);
                }
              }
              if (
                bestCandidates.length != 0 &&
                best <= this.suggestionThreshold
              ) {
                const suggestionText = this.trans.__(
                  'Did you mean %1?',
                  bestCandidates.length === 1
                    ? bestCandidates[0].label
                    : bestCandidates
                        .map(
                          (candidate, index) =>
                            `${index + 1}) ${candidate.label}`
                        )
                        .join(' or ')
                );
                this.communicate(suggestionText);
                return bestCandidates.map(candidate => {
                  return {
                    id: candidate.id,
                    label: candidate.label,
                    score: best
                  };
                });
              }
            }
            return [];
          }
          communicate(message) {
            this._status.error = message;
            if (this.speak) {
              speechSynthesis.speak(new SpeechSynthesisUtterance(message));
            }
          }
          handleSpeechResult(event) {
            const result = event.results[this.counter][0];
            const speech = normalise(result.transcript);
            this._status.lastResult = speech;
            this._status.lastConfidence = result.confidence;
            this.counter += 1;
            if (result.confidence < this.confidenceThreshold) {
              this.communicate(this.trans.__('Too low confidence. Speak up?'));
              this.statusChanged.emit(this._status);
              console.log('Discarding the result due to too low confidence');
              return;
            }
            this._status.error = undefined;
            this._currentSuggestions = this.matchPhrase(speech);
            console.log(this._currentSuggestions);
            this.statusChanged.emit(this._status);
          }
          acceptSuggestion(options) {
            const option =
              options.option != null ? ordinals[options.option] - 1 : 0;
            if (typeof option !== 'undefined') {
              if (this._currentSuggestions.length > option) {
                this.commandRegistry.execute(
                  this._currentSuggestions[option].id
                );
                this._currentSuggestions = [];
              } else {
                this.communicate(
                  this.trans.__('Suggestion %1 not available.', option + 1)
                );
              }
            } else {
              console.warn(
                'Could not resolve option to accept suggestion',
                options
              );
            }
          }
          set language(value) {
            this.recognition.lang = value;
          }
          updateGrammar() {
            this.jupyterCommands.clear();
            this.commandRegistry
              .listCommands()
              .filter(commandID => this.commandRegistry.isVisible(commandID))
              .map(commandID => {
                try {
                  const label = this.commandRegistry.label(commandID);
                  const caption = this.commandRegistry.caption(commandID);
                  if (label) {
                    this.jupyterCommands.set(normalise(label), {
                      id: commandID,
                      caption: caption,
                      label: label
                    });
                  }
                  return label;
                } catch (e) {
                  return null;
                }
              })
              .filter(commandID => !!commandID);
          }
          get isEnabled() {
            return this._status.enabled;
          }
          configure(settings) {
            // TODO
            this.language = 'en-US';
            this.speak = settings.composite.speak;
            this.confidenceThreshold = settings.composite.confidenceThreshold;
            this.suggestionThreshold = settings.composite.suggestionThreshold;
            this.commands = settings.composite.commands;
          }
          enable() {
            this._status.enabled = true;
            this.recognition.start();
            this.counter = 0;
            this.statusChanged.emit(this._status);
          }
          disable() {
            this._status.enabled = false;
            this.recognition.stop();
            this.statusChanged.emit(this._status);
          }
        }

        /***/
      },

    /***/ './lib/icons.js':
      /*!**********************!*\
  !*** ./lib/icons.js ***!
  \**********************/
      /***/ (
        __unused_webpack_module,
        __webpack_exports__,
        __webpack_require__
      ) => {
        __webpack_require__.r(__webpack_exports__);
        /* harmony export */ __webpack_require__.d(__webpack_exports__, {
          /* harmony export */ recognitionDisabledIcon: () =>
            /* binding */ recognitionDisabledIcon,
          /* harmony export */ recognitionEnabledIcon: () =>
            /* binding */ recognitionEnabledIcon
          /* harmony export */
        });
        /* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ =
          __webpack_require__(
            /*! @jupyterlab/ui-components */ 'webpack/sharing/consume/default/@jupyterlab/ui-components'
          );
        /* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default =
          /*#__PURE__*/ __webpack_require__.n(
            _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__
          );
        /* harmony import */ var _style_icons_microphone_svg__WEBPACK_IMPORTED_MODULE_1__ =
          __webpack_require__(
            /*! ../style/icons/microphone.svg */ './style/icons/microphone.svg'
          );
        /* harmony import */ var _style_icons_microphone_off_svg__WEBPACK_IMPORTED_MODULE_2__ =
          __webpack_require__(
            /*! ../style/icons/microphone-off.svg */ './style/icons/microphone-off.svg'
          );

        const recognitionEnabledIcon =
          new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
            name: 'voice:enabled',
            svgstr:
              _style_icons_microphone_svg__WEBPACK_IMPORTED_MODULE_1__[
                'default'
              ]
          });
        const recognitionDisabledIcon =
          new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
            name: 'voice:disabled',
            svgstr:
              _style_icons_microphone_off_svg__WEBPACK_IMPORTED_MODULE_2__[
                'default'
              ]
          });

        /***/
      },

    /***/ './lib/index.js':
      /*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
      /***/ (
        __unused_webpack_module,
        __webpack_exports__,
        __webpack_require__
      ) => {
        __webpack_require__.r(__webpack_exports__);
        /* harmony export */ __webpack_require__.d(__webpack_exports__, {
          /* harmony export */ default: () => __WEBPACK_DEFAULT_EXPORT__
          /* harmony export */
        });
        /* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ =
          __webpack_require__(
            /*! @lumino/coreutils */ 'webpack/sharing/consume/default/@lumino/coreutils'
          );
        /* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default =
          /*#__PURE__*/ __webpack_require__.n(
            _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__
          );
        /* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ =
          __webpack_require__(
            /*! @jupyterlab/apputils */ 'webpack/sharing/consume/default/@jupyterlab/apputils'
          );
        /* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default =
          /*#__PURE__*/ __webpack_require__.n(
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__
          );
        /* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_2__ =
          __webpack_require__(
            /*! @jupyterlab/statusbar */ 'webpack/sharing/consume/default/@jupyterlab/statusbar'
          );
        /* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_2___default =
          /*#__PURE__*/ __webpack_require__.n(
            _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_2__
          );
        /* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ =
          __webpack_require__(
            /*! @jupyterlab/translation */ 'webpack/sharing/consume/default/@jupyterlab/translation'
          );
        /* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default =
          /*#__PURE__*/ __webpack_require__.n(
            _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__
          );
        /* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__ =
          __webpack_require__(
            /*! @jupyterlab/settingregistry */ 'webpack/sharing/consume/default/@jupyterlab/settingregistry'
          );
        /* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4___default =
          /*#__PURE__*/ __webpack_require__.n(
            _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__
          );
        /* harmony import */ var _components_status__WEBPACK_IMPORTED_MODULE_6__ =
          __webpack_require__(
            /*! ./components/status */ './lib/components/status.js'
          );
        /* harmony import */ var _controller__WEBPACK_IMPORTED_MODULE_5__ =
          __webpack_require__(/*! ./controller */ './lib/controller.js');
        /* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_7__ =
          __webpack_require__(/*! ./commands */ './lib/commands.js');

        const PLUGIN_ID = 'jupyterlab-voice-control:plugin';
        /**
         * Initialization data for the jupyterlab-voice-control extension.
         */
        const plugin = {
          id: PLUGIN_ID,
          autoStart: true,
          requires: [
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette
          ],
          optional: [
            _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry,
            _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_2__.IStatusBar,
            _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator
          ],
          activate: (app, palette, settingRegistry, statusBar, translator) => {
            console.log(
              'JupyterLab extension jupyterlab-voice-control is activated!'
            );
            translator =
              translator ||
              _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator;
            const trans = translator.load('jupyterlab-voice-control');
            const controller =
              new _controller__WEBPACK_IMPORTED_MODULE_5__.VoiceController(
                app.commands,
                trans,
                palette
              );
            let canonical;
            /**
             * Populate the plugin's schema defaults.
             */
            const populate = schema => {
              schema.properties.commands.items.properties.command.enum =
                app.commands.listCommands();
            };
            if (settingRegistry) {
              settingRegistry
                .load(plugin.id)
                .then(settings => {
                  settings.changed.connect(
                    controller.configure.bind(controller)
                  );
                  controller.configure(settings);
                })
                .catch(reason => {
                  console.error(
                    'Failed to load settings for jupyterlab-voice-control.',
                    reason
                  );
                });
              settingRegistry.transform(plugin.id, {
                fetch: plugin => {
                  // Only override the canonical schema the first time.
                  if (!canonical) {
                    canonical =
                      _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.JSONExt.deepCopy(
                        plugin.schema
                      );
                    populate(canonical);
                  }
                  return {
                    data: plugin.data,
                    id: plugin.id,
                    raw: plugin.raw,
                    schema: canonical,
                    version: plugin.version
                  };
                }
              });
            }
            console.log(controller.statusChanged);
            if (statusBar) {
              statusBar.registerStatusItem(PLUGIN_ID, {
                item: new _components_status__WEBPACK_IMPORTED_MODULE_6__.VoiceControlStatusIndicator(
                  controller.statusChanged,
                  trans,
                  controller
                ),
                rank: 900
              });
            }
            app.commands.addCommand('vc:start-listening', {
              label: trans.__('Enable voice control'),
              execute: () => controller.enable(),
              isVisible: () => !controller.isEnabled
            });
            app.commands.addCommand('vc:stop-listening', {
              label: trans.__('Enable voice control'),
              execute: () => controller.enable(),
              isVisible: () => !controller.isEnabled
            });
            app.commands.addCommand('vc:scroll-by', {
              label: trans.__('Scroll Focused Element By'),
              execute: args =>
                (0, _commands__WEBPACK_IMPORTED_MODULE_7__.scrollBy)(args)
            });
            app.commands.addCommand('vc:type-text', {
              label: trans.__('Type Text Into Focused Element'),
              execute: args =>
                (0, _commands__WEBPACK_IMPORTED_MODULE_7__.typeText)(args)
            });
            app.commands.addCommand('vc:delete-text', {
              label: trans.__('Delete Text From Focused Element'),
              execute: args =>
                (0, _commands__WEBPACK_IMPORTED_MODULE_7__.deleteText)(args)
            });
            app.commands.addCommand('vc:accept-suggestion', {
              label: trans.__('Accept Voice Control Suggestion'),
              execute: args => controller.acceptSuggestion(args)
            });
            app.commands.addCommand('vc:open-notebook', {
              label: trans.__('Open Notebook By Name'),
              execute: args =>
                app.commands.execute('filebrowser:open-path', {
                  path: args.path + '.ipynb'
                })
            });
            app.commands.addCommand('vc:move-cursor', {
              label: trans.__('Move Cursor In Editor'),
              execute: args =>
                (0, _commands__WEBPACK_IMPORTED_MODULE_7__.moveCursor)(args)
            });
          }
        };
        /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = plugin;

        /***/
      },

    /***/ './style/icons/microphone-off.svg':
      /*!****************************************!*\
  !*** ./style/icons/microphone-off.svg ***!
  \****************************************/
      /***/ (
        __unused_webpack_module,
        __webpack_exports__,
        __webpack_require__
      ) => {
        __webpack_require__.r(__webpack_exports__);
        /* harmony export */ __webpack_require__.d(__webpack_exports__, {
          /* harmony export */ default: () => __WEBPACK_DEFAULT_EXPORT__
          /* harmony export */
        });
        /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ =
          '<svg width="16" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">\n  <g class="jp-icon3 jp-icon-selectable" fill="#4F4F4F">\n    <path d="M19,11C19,12.19 18.66,13.3 18.1,14.28L16.87,13.05C17.14,12.43 17.3,11.74 17.3,11H19M15,11.16L9,5.18V5A3,3 0 0,1 12,2A3,3 0 0,1 15,5V11L15,11.16M4.27,3L21,19.73L19.73,21L15.54,16.81C14.77,17.27 13.91,17.58 13,17.72V21H11V17.72C7.72,17.23 5,14.41 5,11H6.7C6.7,14 9.24,16.1 12,16.1C12.81,16.1 13.6,15.91 14.31,15.58L12.65,13.92L12,14A3,3 0 0,1 9,11V10.28L3,4.27L4.27,3Z" />\n  </g>\n</svg>';

        /***/
      },

    /***/ './style/icons/microphone.svg':
      /*!************************************!*\
  !*** ./style/icons/microphone.svg ***!
  \************************************/
      /***/ (
        __unused_webpack_module,
        __webpack_exports__,
        __webpack_require__
      ) => {
        __webpack_require__.r(__webpack_exports__);
        /* harmony export */ __webpack_require__.d(__webpack_exports__, {
          /* harmony export */ default: () => __WEBPACK_DEFAULT_EXPORT__
          /* harmony export */
        });
        /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ =
          '<svg width="16" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">\n  <g class="jp-icon3 jp-icon-selectable" fill="#4F4F4F">\n    <path d="M12,2A3,3 0 0,1 15,5V11A3,3 0 0,1 12,14A3,3 0 0,1 9,11V5A3,3 0 0,1 12,2M19,11C19,14.53 16.39,17.44 13,17.93V21H11V17.93C7.61,17.44 5,14.53 5,11H7A5,5 0 0,0 12,16A5,5 0 0,0 17,11H19Z" />\n  </g>\n</svg>';

        /***/
      }
  }
]);
//# sourceMappingURL=lib_index_js.f7b76e5ba262d6079bf7.js.map
