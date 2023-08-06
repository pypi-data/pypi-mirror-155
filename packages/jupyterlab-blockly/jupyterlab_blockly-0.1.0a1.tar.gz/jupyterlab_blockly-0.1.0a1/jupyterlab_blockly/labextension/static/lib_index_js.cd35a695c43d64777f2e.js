"use strict";
(self["webpackChunkjupyterlab_blockly"] = self["webpackChunkjupyterlab_blockly"] || []).push([["lib_index_js"],{

/***/ "./lib/factory.js":
/*!************************!*\
  !*** ./lib/factory.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BlocklyEditorFactory": () => (/* binding */ BlocklyEditorFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");
/* harmony import */ var _registry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./registry */ "./lib/registry.js");
/* harmony import */ var _manager__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./manager */ "./lib/manager.js");




/**
 * A widget factory to create new instances of BlocklyEditor.
 */
class BlocklyEditorFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__.ABCWidgetFactory {
    /**
     * Constructor of BlocklyEditorFactory.
     *
     * @param options Constructor options
     */
    constructor(options) {
        super(options);
        this._registry = new _registry__WEBPACK_IMPORTED_MODULE_1__.BlocklyRegistry();
        this._rendermime = options.rendermime;
        this._mimetypeService = options.mimetypeService;
    }
    get registry() {
        return this._registry;
    }
    /**
     * Create a new widget given a context.
     *
     * @param context Contains the information of the file
     * @returns The widget
     */
    createNewWidget(context) {
        const manager = new _manager__WEBPACK_IMPORTED_MODULE_2__.BlocklyManager(this._registry, context.sessionContext, this._mimetypeService);
        const content = new _widget__WEBPACK_IMPORTED_MODULE_3__.BlocklyPanel(context, manager, this._rendermime);
        return new _widget__WEBPACK_IMPORTED_MODULE_3__.BlocklyEditor({ context, content, manager });
    }
}


/***/ }),

/***/ "./lib/icons.js":
/*!**********************!*\
  !*** ./lib/icons.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "blockly_icon": () => (/* binding */ blockly_icon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_icons_blockly_logo_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../../../../style/icons/blockly_logo.svg */ "./style/icons/blockly_logo.svg");


const blockly_icon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'blockly:icon/logo',
    svgstr: _style_icons_blockly_logo_svg__WEBPACK_IMPORTED_MODULE_1__["default"]
});


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _factory__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./factory */ "./lib/factory.js");
/* harmony import */ var _token__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./token */ "./lib/token.js");
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./icons */ "./lib/icons.js");













/**
 * The name of the factory that creates the editor widgets.
 */
const FACTORY = 'Blockly editor';
const PALETTE_CATEGORY = 'Blockly editor';
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.createNew = 'blockly:create-new-blockly-file';
})(CommandIDs || (CommandIDs = {}));
/**
 * The id of the translation plugin.
 */
const PLUGIN_ID = '@jupyterlab/translation-extension:plugin';
/**
 * Initialization data for the jupyterlab-blocky extension.
 */
const plugin = {
    id: 'jupyterlab-blocky:plugin',
    autoStart: true,
    requires: [
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__.IRenderMimeRegistry,
        _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_4__.IEditorServices,
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5__.IFileBrowserFactory,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_8__.ISettingRegistry,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator
    ],
    optional: [_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_6__.ILauncher, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ICommandPalette],
    provides: _token__WEBPACK_IMPORTED_MODULE_9__.IBlocklyRegisty,
    activate: (app, restorer, rendermime, editorServices, browserFactory, settings, translator, launcher, palette) => {
        console.log('JupyterLab extension jupyterlab-blocky is activated!');
        // Namespace for the tracker
        const namespace = 'jupyterlab-blocky';
        // Creating the tracker for the document
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.WidgetTracker({ namespace });
        // Handle state restoration.
        if (restorer) {
            // When restoring the app, if the document was open, reopen it
            restorer.restore(tracker, {
                command: 'docmanager:open',
                args: widget => ({ path: widget.context.path, factory: FACTORY }),
                name: widget => widget.context.path
            });
        }
        const { commands } = app;
        const command = CommandIDs.createNew;
        // Creating the widget factory to register it so the document manager knows about
        // our new DocumentWidget
        const widgetFactory = new _factory__WEBPACK_IMPORTED_MODULE_10__.BlocklyEditorFactory({
            name: FACTORY,
            modelName: 'text',
            fileTypes: ['blockly'],
            defaultFor: ['blockly'],
            // Kernel options, in this case we need to execute the code generated
            // in the blockly editor. The best way would be to use kernels, for
            // that reason, we tell the widget factory to start a kernel session
            // when opening the editor, and close the session when closing the editor.
            canStartKernel: true,
            preferKernel: true,
            shutdownOnClose: true,
            // The rendermime instance, necessary to render the outputs
            // after a code execution. And the mimeType service to get the
            // mimeType from the kernel language
            rendermime: rendermime,
            mimetypeService: editorServices.mimeTypeService,
            // The translator instance, used for the internalization of the plugin.
            translator: translator
        });
        // Add the widget to the tracker when it's created
        widgetFactory.widgetCreated.connect((sender, widget) => {
            // Adding the Blockly icon for the widget so it appears next to the file name.
            widget.title.icon = _icons__WEBPACK_IMPORTED_MODULE_11__.blockly_icon;
            // Notify the instance tracker if restore data needs to update.
            widget.context.pathChanged.connect(() => {
                tracker.save(widget);
            });
            tracker.add(widget);
        });
        // Registering the file type
        app.docRegistry.addFileType({
            name: 'blockly',
            displayName: 'Blockly',
            contentType: 'file',
            fileFormat: 'json',
            extensions: ['.jpblockly'],
            mimeTypes: ['application/json'],
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.jsonIcon,
            iconLabel: 'JupyterLab-Blockly'
        });
        // Registering the widget factory
        app.docRegistry.addWidgetFactory(widgetFactory);
        function getSetting(setting) {
            // Read the settings and convert to the correct type
            const currentLocale = setting.get('locale').composite;
            return currentLocale;
        }
        // Wait for the application to be restored and
        // for the settings for this plugin to be loaded
        settings.load(PLUGIN_ID).then(setting => {
            // Read the settings
            const currentLocale = getSetting(setting);
            // Listen for our plugin setting changes using Signal
            setting.changed.connect(getSetting);
            // Get new language and call the function that modifies the language name accordingly.
            // Also, make the transformation to have the name of the language package as in Blockly.
            const language = currentLocale[currentLocale.length - 2].toUpperCase() +
                currentLocale[currentLocale.length - 1].toLowerCase();
            console.log(`Current Language : '${language}'`);
            // Transmitting the current language to the manager.
            widgetFactory.registry.setlanguage(language);
        });
        commands.addCommand(command, {
            label: args => args['isPalette'] ? 'New Blockly Editor' : 'Blockly Editor',
            caption: 'Create a new Blockly Editor',
            icon: args => (args['isPalette'] ? null : _icons__WEBPACK_IMPORTED_MODULE_11__.blockly_icon),
            execute: async (args) => {
                // Get the directory in which the Blockly file must be created;
                // otherwise take the current filebrowser directory
                const cwd = args['cwd'] || browserFactory.tracker.currentWidget.model.path;
                // Create a new untitled Blockly file
                const model = await commands.execute('docmanager:new-untitled', {
                    path: cwd,
                    type: 'file',
                    ext: '.json'
                });
                // Open the newly created file with the 'Editor'
                return commands.execute('docmanager:open', {
                    path: model.path,
                    factory: FACTORY
                });
            }
        });
        // Add the command to the launcher
        if (launcher) {
            launcher.add({
                command,
                category: 'Other',
                rank: 1
            });
        }
        // Add the command to the palette
        if (palette) {
            palette.addItem({
                command,
                args: { isPalette: true },
                category: PALETTE_CATEGORY
            });
        }
        return widgetFactory.registry;
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/layout.js":
/*!***********************!*\
  !*** ./lib/layout.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BlocklyLayout": () => (/* binding */ BlocklyLayout)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! blockly */ "webpack/sharing/consume/default/blockly/blockly");
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(blockly__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");







/**
 * A blockly layout to host the Blockly editor.
 */
class BlocklyLayout extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.PanelLayout {
    /**
     * Construct a `BlocklyLayout`.
     *
     */
    constructor(manager, sessionContext, rendermime) {
        super();
        this._manager = manager;
        this._sessionContext = sessionContext;
        // Creating the container for the Blockly editor
        // and the output area to render the execution replies.
        this._host = document.createElement('div');
        // Creating a CodeCell widget to render the code and
        // outputs from the execution reply.
        this._cell = new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.CodeCell({
            model: new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.CodeCellModel({}),
            rendermime
        });
        // Trust the outputs and set the mimeType for the code
        this._cell.readOnly = true;
        this._cell.model.trusted = true;
        this._cell.model.mimeType = this._manager.mimeType;
        this._manager.changed.connect(this._onManagerChanged, this);
    }
    get workspace() {
        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
        // @ts-ignore
        return blockly__WEBPACK_IMPORTED_MODULE_5__.serialization.workspaces.save(this._workspace);
    }
    set workspace(workspace) {
        const data = workspace === null ? { variables: [] } : workspace;
        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
        // @ts-ignore
        blockly__WEBPACK_IMPORTED_MODULE_5__.serialization.workspaces.load(data, this._workspace);
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        this._manager.changed.disconnect(this._resizeWorkspace, this);
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal.clearData(this);
        this._workspace.dispose();
        super.dispose();
    }
    /**
     * Init the blockly layout
     */
    init() {
        super.init();
        // Add the blockly container into the DOM
        this.addWidget(new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget({ node: this._host }));
    }
    /**
     * Create an iterator over the widgets in the layout.
     */
    iter() {
        return new _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.ArrayIterator([]);
    }
    /**
     * Remove a widget from the layout.
     *
     * @param widget - The `widget` to remove.
     */
    removeWidget(widget) {
        return;
    }
    run() {
        // Serializing our workspace into the chosen language generator.
        const code = this._manager.generator.workspaceToCode(this._workspace);
        this._cell.model.sharedModel.setSource(code);
        this.addWidget(this._cell);
        this._resizeWorkspace();
        // Execute the code using the kernel, by using a static method from the
        // same class to make an execution request.
        if (this._sessionContext.hasNoKernel) {
            // Check whether there is a kernel
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)('Select a valid kernel', `There is not a valid kernel selected, select one from the dropdown menu in the toolbar.
        If there isn't a valid kernel please install 'xeus-python' from Pypi.org or using mamba.
        `);
        }
        else {
            _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.CodeCell.execute(this._cell, this._sessionContext)
                .then(() => this._resizeWorkspace())
                .catch(e => console.error(e));
        }
    }
    /**
     * Handle `update-request` messages sent to the widget.
     */
    onUpdateRequest(msg) {
        this._resizeWorkspace();
    }
    /**
     * Handle `resize-request` messages sent to the widget.
     */
    onResize(msg) {
        this._resizeWorkspace();
    }
    /**
     * Handle `fit-request` messages sent to the widget.
     */
    onFitRequest(msg) {
        this._resizeWorkspace();
    }
    /**
     * Handle `after-attach` messages sent to the widget.
     */
    onAfterAttach(msg) {
        //inject Blockly with appropiate JupyterLab theme.
        this._workspace = blockly__WEBPACK_IMPORTED_MODULE_5__.inject(this._host, {
            toolbox: this._manager.toolbox,
            theme: _utils__WEBPACK_IMPORTED_MODULE_6__.THEME
        });
    }
    _resizeWorkspace() {
        //Resize logic.
        const rect = this.parent.node.getBoundingClientRect();
        const { height } = this._cell.node.getBoundingClientRect();
        const margin = rect.height / 3;
        if (height > margin) {
            this._host.style.height = rect.height - margin + 'px';
            this._cell.node.style.height = margin + 'px';
            this._cell.node.style.overflowY = 'scroll';
        }
        else {
            this._host.style.height = rect.height - height + 'px';
            this._cell.node.style.overflowY = 'scroll';
        }
        blockly__WEBPACK_IMPORTED_MODULE_5__.svgResize(this._workspace);
    }
    _onManagerChanged(sender, change) {
        if (change === 'kernel') {
            // Serializing our workspace into the chosen language generator.
            const code = this._manager.generator.workspaceToCode(this._workspace);
            this._cell.model.sharedModel.setSource(code);
            this._cell.model.mimeType = this._manager.mimeType;
        }
    }
}


/***/ }),

/***/ "./lib/manager.js":
/*!************************!*\
  !*** ./lib/manager.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BlocklyManager": () => (/* binding */ BlocklyManager)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);

/**
 * BlocklyManager the manager for each document
 * to select the toolbox and the generator that the
 * user wants to use on a specific document.
 */
class BlocklyManager {
    /**
     * Constructor of BlocklyManager.
     */
    constructor(registry, sessionContext, mimetypeService) {
        this._registry = registry;
        this._sessionContext = sessionContext;
        this._mimetypeService = mimetypeService;
        this._toolbox = this._registry.toolboxes.get('default');
        this._generator = this._registry.generators.get('python');
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._sessionContext.kernelChanged.connect(this._onKernelChanged, this);
    }
    /**
     * Returns the selected toolbox.
     */
    get toolbox() {
        return this._toolbox;
    }
    /**
     * Returns the mimeType for the selected kernel.
     *
     * Note: We need the mimeType for the syntax highlighting
     * when rendering the code.
     */
    get mimeType() {
        if (this._selectedKernel) {
            return this._mimetypeService.getMimeTypeByLanguage({
                name: this._selectedKernel.language
            });
        }
        else {
            return 'text/plain';
        }
    }
    /**
     * Returns the name of the selected kernel.
     */
    get kernel() {
        var _a;
        return ((_a = this._selectedKernel) === null || _a === void 0 ? void 0 : _a.name) || 'No kernel';
    }
    /**
     * Returns the selected generator.
     */
    get generator() {
        return this._generator;
    }
    /**
     * Signal triggered when the manager changes.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Dispose.
     */
    dispose() {
        this._sessionContext.kernelChanged.disconnect(this._onKernelChanged, this);
    }
    /**
     * Set the selected toolbox.
     *
     * @argument name The name of the toolbox.
     */
    setToolbox(name) {
        this._toolbox = this._registry.toolboxes.get(name);
    }
    /**
     * Set the selected kernel.
     *
     * @argument name The name of the kernel.
     */
    selectKernel(name) {
        this._sessionContext.changeKernel({ name });
    }
    /**
     * Set the selected toolbox.
     *
     * @returns the list of available kernels for Blockly
     */
    listKernels() {
        const specs = this._sessionContext.specsManager.specs.kernelspecs;
        const list = [];
        Object.keys(specs).forEach(key => {
            const language = specs[key].language;
            if (this._registry.generators.has(language)) {
                list.push({ label: specs[key].display_name, value: specs[key].name });
            }
        });
        return list;
    }
    _onKernelChanged(sender, args) {
        const specs = this._sessionContext.specsManager.specs.kernelspecs;
        if (args.newValue && specs[args.newValue.name] !== undefined) {
            this._selectedKernel = specs[args.newValue.name];
            const language = specs[args.newValue.name].language;
            this._generator = this._registry.generators.get(language);
            this._changed.emit('kernel');
        }
    }
}


/***/ }),

/***/ "./lib/registry.js":
/*!*************************!*\
  !*** ./lib/registry.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BlocklyRegistry": () => (/* binding */ BlocklyRegistry)
/* harmony export */ });
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! blockly */ "webpack/sharing/consume/default/blockly/blockly");
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(blockly__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var blockly_python__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! blockly/python */ "./node_modules/blockly/python.js");
/* harmony import */ var blockly_python__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(blockly_python__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var blockly_javascript__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! blockly/javascript */ "./node_modules/blockly/javascript.js");
/* harmony import */ var blockly_javascript__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(blockly_javascript__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var blockly_lua__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! blockly/lua */ "./node_modules/blockly/lua.js");
/* harmony import */ var blockly_lua__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(blockly_lua__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var blockly_msg_en__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! blockly/msg/en */ "./node_modules/blockly/msg/en.js");
/* harmony import */ var blockly_msg_en__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(blockly_msg_en__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");






/**
 * BlocklyRegistry is the class that JupyterLab-Blockly exposes
 * to other plugins. This registry allows other plugins to register
 * new Toolboxes, Blocks and Generators that users can use in the
 * Blockly editor.
 */
class BlocklyRegistry {
    /**
     * Constructor of BlocklyRegistry.
     */
    constructor() {
        this._toolboxes = new Map();
        this._toolboxes.set('default', _utils__WEBPACK_IMPORTED_MODULE_5__.TOOLBOX);
        this._generators = new Map();
        this._generators.set('python', (blockly_python__WEBPACK_IMPORTED_MODULE_1___default()));
        this._generators.set('javascript', (blockly_javascript__WEBPACK_IMPORTED_MODULE_2___default()));
        this._generators.set('lua', (blockly_lua__WEBPACK_IMPORTED_MODULE_3___default()));
    }
    /**
     * Returns a map with all the toolboxes.
     */
    get toolboxes() {
        return this._toolboxes;
    }
    /**
     * Returns a map with all the generators.
     */
    get generators() {
        return this._generators;
    }
    /**
     * Register a toolbox for the editor.
     *
     * @argument name Name of the toolbox.
     *
     * @argument value Toolbox to register.
     */
    registerToolbox(name, value) {
        this._toolboxes.set(name, value);
    }
    /**
     * Register new blocks.
     *
     * @argument name Name of the toolbox.
     *
     * @argument value Toolbox to register.
     */
    registerBlocks(blocks) {
        blockly__WEBPACK_IMPORTED_MODULE_0__.defineBlocksWithJsonArray(blocks);
    }
    /**
     * Register new generators.
     *
     * @argument name Name of the toolbox.
     *
     * @argument value Toolbox to register.
     *
     * #### Notes
     * When registering a generator, the name should correspond to the language
     * used by a kernel.
     *
     * If you register a generator for an existing language this will be overwritten.
     */
    registerGenerator(name, generator) {
        this._generators.set(name, generator);
    }
    setlanguage(language) {
        Private.importLanguageModule(language);
    }
}
var Private;
(function (Private) {
    // Dynamically importing the language modules needed for each respective
    // user, in order to change the Blockly language in accordance to the
    // JL one.
    async function importLanguageModule(language) {
        let module;
        switch (language) {
            case 'En':
                module = Promise.resolve(/*! import() */).then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/en */ "./node_modules/blockly/msg/en.js", 23));
                break;
            case 'Es':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_es_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/es */ "./node_modules/blockly/msg/es.js", 23));
                break;
            case 'Fr':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_fr_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/fr */ "./node_modules/blockly/msg/fr.js", 23));
                break;
            case 'Sa' || 0:
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_ar_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/ar */ "./node_modules/blockly/msg/ar.js", 23));
                break;
            case 'Cz':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_cs_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/cs */ "./node_modules/blockly/msg/cs.js", 23));
                break;
            case 'Dk':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_da_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/da */ "./node_modules/blockly/msg/da.js", 23));
                break;
            case 'De':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_de_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/de */ "./node_modules/blockly/msg/de.js", 23));
                break;
            case 'Gr':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_el_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/el */ "./node_modules/blockly/msg/el.js", 23));
                break;
            case 'Ee':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_et_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/et */ "./node_modules/blockly/msg/et.js", 23));
                break;
            case 'Fi':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_fi_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/fi */ "./node_modules/blockly/msg/fi.js", 23));
                break;
            case 'Il':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_he_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/he */ "./node_modules/blockly/msg/he.js", 23));
                break;
            case 'Hu':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_hu_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/hu */ "./node_modules/blockly/msg/hu.js", 23));
                break;
            case 'Am':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_hy_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/hy */ "./node_modules/blockly/msg/hy.js", 23));
                break;
            case 'Id':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_id_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/id */ "./node_modules/blockly/msg/id.js", 23));
                break;
            case 'It':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_it_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/it */ "./node_modules/blockly/msg/it.js", 23));
                break;
            case 'Jp':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_ja_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/ja */ "./node_modules/blockly/msg/ja.js", 23));
                break;
            case 'Kr':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_ko_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/ko */ "./node_modules/blockly/msg/ko.js", 23));
                break;
            case 'Lt':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_lt_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/lt */ "./node_modules/blockly/msg/lt.js", 23));
                break;
            case 'Nl':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_nl_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/nl */ "./node_modules/blockly/msg/nl.js", 23));
                break;
            case 'Pl':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_pl_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/pl */ "./node_modules/blockly/msg/pl.js", 23));
                break;
            case 'Br':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_pt_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/pt */ "./node_modules/blockly/msg/pt.js", 23));
                break;
            case 'Ro':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_ro_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/ro */ "./node_modules/blockly/msg/ro.js", 23));
                break;
            case 'Ru':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_ru_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/ru */ "./node_modules/blockly/msg/ru.js", 23));
                break;
            case 'Lk':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_si_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/si */ "./node_modules/blockly/msg/si.js", 23));
                break;
            case 'Tr':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_tr_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/tr */ "./node_modules/blockly/msg/tr.js", 23));
                break;
            case 'Ua':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_uk_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/uk */ "./node_modules/blockly/msg/uk.js", 23));
                break;
            case 'Vn':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_vi_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/vi */ "./node_modules/blockly/msg/vi.js", 23));
                break;
            case 'Tw':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_zh-hant_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/zh-hant */ "./node_modules/blockly/msg/zh-hant.js", 23));
                break;
            case 'Cn':
                module = __webpack_require__.e(/*! import() */ "vendors-node_modules_blockly_msg_zh-hans_js").then(__webpack_require__.t.bind(__webpack_require__, /*! blockly/msg/zh-hans */ "./node_modules/blockly/msg/zh-hans.js", 23));
                break;
            default:
                // Complete with all the cases taken from: (last updates June 2022)
                // List of languages in blockly: https://github.com/google/blockly/tree/master/msg/js
                // List of languages in Lab: https://github.com/jupyterlab/language-packs/tree/master/language-packs
                console.warn('Language not found. Loading english');
                module = Promise.resolve((blockly_msg_en__WEBPACK_IMPORTED_MODULE_4___default()));
                break;
        }
        // Setting the current language in Blockly.
        module.then(lang => {
            // eslint-disable-next-line @typescript-eslint/ban-ts-comment
            // @ts-ignore
            blockly__WEBPACK_IMPORTED_MODULE_0__.setLocale(lang);
        });
    }
    Private.importLanguageModule = importLanguageModule;
})(Private || (Private = {}));


/***/ }),

/***/ "./lib/token.js":
/*!**********************!*\
  !*** ./lib/token.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IBlocklyRegisty": () => (/* binding */ IBlocklyRegisty)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);

/**
 * The registry token.
 */
const IBlocklyRegisty = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('jupyterlab-blockly/registry');


/***/ }),

/***/ "./lib/toolbar/selector.js":
/*!*********************************!*\
  !*** ./lib/toolbar/selector.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SelectGenerator": () => (/* binding */ SelectGenerator)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./utils */ "./lib/toolbar/utils.js");



class SelectGenerator extends _utils__WEBPACK_IMPORTED_MODULE_2__.BlocklyButton {
    constructor(props) {
        super(props);
        this.handleChange = (event) => {
            this._manager.selectKernel(event.target.value);
            this.update();
        };
        this._manager = props.manager;
        this._manager.changed.connect(this.update, this);
    }
    dispose() {
        super.dispose();
        this._manager.changed.disconnect(this.update, this);
    }
    render() {
        const kernels = this._manager.listKernels();
        if (this._manager.kernel === 'No kernel') {
            kernels.push({ label: 'No kernel', value: 'No kernel' });
        }
        return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.HTMLSelect, { onChange: this.handleChange, value: this._manager.kernel, options: kernels }));
    }
}


/***/ }),

/***/ "./lib/toolbar/utils.js":
/*!******************************!*\
  !*** ./lib/toolbar/utils.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BlocklyButton": () => (/* binding */ BlocklyButton),
/* harmony export */   "Spacer": () => (/* binding */ Spacer)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);


class BlocklyButton extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton {
    constructor(props) {
        super(props);
        this.addClass('jp-blockly-button');
    }
}
class Spacer extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget {
    constructor() {
        super();
        this.addClass('jp-Toolbar-spacer');
    }
}


/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "THEME": () => (/* binding */ THEME),
/* harmony export */   "TOOLBOX": () => (/* binding */ TOOLBOX)
/* harmony export */ });
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! blockly */ "webpack/sharing/consume/default/blockly/blockly");
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(blockly__WEBPACK_IMPORTED_MODULE_0__);

// Creating a toolbox containing all the main (default) blocks.
const TOOLBOX = {
    kind: 'categoryToolbox',
    contents: [
        {
            kind: 'category',
            name: 'Logic',
            colour: '210',
            contents: [
                {
                    kind: 'block',
                    type: 'controls_if'
                },
                {
                    kind: 'BLOCK',
                    type: 'logic_compare'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="logic_operation"></block>',
                    type: 'logic_operation'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="logic_negate"></block>',
                    type: 'logic_negate'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="logic_boolean"></block>',
                    type: 'logic_boolean'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="logic_null"></block>',
                    type: 'logic_null'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="logic_ternary"></block>',
                    type: 'logic_ternary'
                }
            ]
        },
        {
            kind: 'category',
            name: 'Loops',
            colour: '120',
            contents: [
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="controls_repeat_ext">\n          <value name="TIMES">\n            <shadow type="math_number">\n              <field name="NUM">10</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'controls_repeat_ext'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="controls_whileUntil"></block>',
                    type: 'controls_whileUntil'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="controls_for">\n          <value name="FROM">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="TO">\n            <shadow type="math_number">\n              <field name="NUM">10</field>\n            </shadow>\n          </value>\n          <value name="BY">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'controls_for'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="controls_forEach"></block>',
                    type: 'controls_forEach'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="controls_flow_statements"></block>',
                    type: 'controls_flow_statements'
                }
            ]
        },
        {
            kind: 'CATEGORY',
            name: 'Math',
            colour: '230',
            contents: [
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_number"></block>',
                    type: 'math_number'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_arithmetic">\n          <value name="A">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="B">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_arithmetic'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_single">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">9</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_single'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_trig">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">45</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_trig'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_constant"></block>',
                    type: 'math_constant'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_number_property">\n          <value name="NUMBER_TO_CHECK">\n            <shadow type="math_number">\n              <field name="NUM">0</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_number_property'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_change">\n          <value name="DELTA">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_change'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_round">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">3.1</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_round'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_on_list"></block>',
                    type: 'math_on_list'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_modulo">\n          <value name="DIVIDEND">\n            <shadow type="math_number">\n              <field name="NUM">64</field>\n            </shadow>\n          </value>\n          <value name="DIVISOR">\n            <shadow type="math_number">\n              <field name="NUM">10</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_modulo'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_constrain">\n          <value name="VALUE">\n            <shadow type="math_number">\n              <field name="NUM">50</field>\n            </shadow>\n          </value>\n          <value name="LOW">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="HIGH">\n            <shadow type="math_number">\n              <field name="NUM">100</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_constrain'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_random_int">\n          <value name="FROM">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="TO">\n            <shadow type="math_number">\n              <field name="NUM">100</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_random_int'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_random_float"></block>',
                    type: 'math_random_float'
                }
            ]
        },
        {
            kind: 'CATEGORY',
            name: 'Text',
            colour: '160',
            contents: [
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text"></block>',
                    type: 'text'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_join"></block>',
                    type: 'text_join'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_append">\n          <value name="TEXT">\n            <shadow type="text"></shadow>\n          </value>\n        </block>',
                    type: 'text_append'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_length">\n          <value name="VALUE">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_length'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_isEmpty">\n          <value name="VALUE">\n            <shadow type="text">\n              <field name="TEXT"></field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_isEmpty'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_indexOf">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">text</field>\n            </block>\n          </value>\n          <value name="FIND">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_indexOf'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_charAt">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">text</field>\n            </block>\n          </value>\n        </block>',
                    type: 'text_charAt'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_getSubstring">\n          <value name="STRING">\n            <block type="variables_get">\n              <field name="VAR">text</field>\n            </block>\n          </value>\n        </block>',
                    type: 'text_getSubstring'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_changeCase">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_changeCase'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_trim">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_trim'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_print">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_print'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_prompt_ext">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_prompt_ext'
                }
            ]
        },
        {
            kind: 'CATEGORY',
            name: 'Lists',
            colour: '260',
            contents: [
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_create_with">\n          <mutation items="0"></mutation>\n        </block>',
                    type: 'lists_create_with'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_create_with"></block>',
                    type: 'lists_create_with'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_repeat">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">5</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'lists_repeat'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_length"></block>',
                    type: 'lists_length'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_isEmpty"></block>',
                    type: 'lists_isEmpty'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_indexOf">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
                    type: 'lists_indexOf'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_getIndex">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
                    type: 'lists_getIndex'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_setIndex">\n          <value name="LIST">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
                    type: 'lists_setIndex'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_getSublist">\n          <value name="LIST">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
                    type: 'lists_getSublist'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_split">\n          <value name="DELIM">\n            <shadow type="text">\n              <field name="TEXT">,</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'lists_split'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_sort"></block>',
                    type: 'lists_sort'
                }
            ]
        },
        {
            kind: 'CATEGORY',
            name: 'Color',
            colour: '20',
            contents: [
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="colour_picker"></block>',
                    type: 'colour_picker'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="colour_random"></block>',
                    type: 'colour_random'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="colour_rgb">\n          <value name="RED">\n            <shadow type="math_number">\n              <field name="NUM">100</field>\n            </shadow>\n          </value>\n          <value name="GREEN">\n            <shadow type="math_number">\n              <field name="NUM">50</field>\n            </shadow>\n          </value>\n          <value name="BLUE">\n            <shadow type="math_number">\n              <field name="NUM">0</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'colour_rgb'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="colour_blend">\n          <value name="COLOUR1">\n            <shadow type="colour_picker">\n              <field name="COLOUR">#ff0000</field>\n            </shadow>\n          </value>\n          <value name="COLOUR2">\n            <shadow type="colour_picker">\n              <field name="COLOUR">#3333ff</field>\n            </shadow>\n          </value>\n          <value name="RATIO">\n            <shadow type="math_number">\n              <field name="NUM">0.5</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'colour_blend'
                }
            ]
        },
        {
            kind: 'SEP'
        },
        {
            kind: 'CATEGORY',
            colour: '330',
            custom: 'VARIABLE',
            name: 'Variables'
        },
        {
            kind: 'CATEGORY',
            colour: '290',
            custom: 'PROCEDURE',
            name: 'Functions'
        }
    ]
};
// Defining a Blockly Theme in accordance with the current JupyterLab Theme.
const jupyterlab_theme = blockly__WEBPACK_IMPORTED_MODULE_0__.Theme.defineTheme('jupyterlab', {
    base: blockly__WEBPACK_IMPORTED_MODULE_0__.Themes.Classic,
    componentStyles: {
        workspaceBackgroundColour: 'var(--jp-layout-color0)',
        toolboxBackgroundColour: 'var(--jp-layout-color2)',
        toolboxForegroundColour: 'var(--jp-ui-font-color0)',
        flyoutBackgroundColour: 'var(--jp-border-color2)',
        flyoutForegroundColour: 'var(--jp-layout-color3)',
        flyoutOpacity: 1,
        scrollbarColour: 'var(--jp-border-color0)',
        insertionMarkerOpacity: 0.3,
        scrollbarOpacity: 0.4,
        cursorColour: 'var(--jp-scrollbar-background-color)'
    }
});
const THEME = jupyterlab_theme;


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BlocklyEditor": () => (/* binding */ BlocklyEditor),
/* harmony export */   "BlocklyPanel": () => (/* binding */ BlocklyPanel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _layout__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./layout */ "./lib/layout.js");
/* harmony import */ var _toolbar__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./toolbar */ "./lib/toolbar/utils.js");
/* harmony import */ var _toolbar__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./toolbar */ "./lib/toolbar/selector.js");






/**
 * DocumentWidget: widget that represents the view or editor for a file type.
 */
class BlocklyEditor extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__.DocumentWidget {
    constructor(options) {
        super(options);
        // Loading the ITranslator
        // const trans = this.translator.load('jupyterlab');
        // Create and add a button to the toolbar to execute
        // the code.
        const button = new _toolbar__WEBPACK_IMPORTED_MODULE_4__.BlocklyButton({
            label: '',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.runIcon,
            className: 'jp-blockly-runButton',
            onClick: () => this.content.layout.run(),
            tooltip: 'Run Code'
        });
        this.toolbar.addItem('run', button);
        this.toolbar.addItem('spacer', new _toolbar__WEBPACK_IMPORTED_MODULE_4__.Spacer());
        this.toolbar.addItem('select', new _toolbar__WEBPACK_IMPORTED_MODULE_5__.SelectGenerator({
            label: 'Select',
            tooltip: 'Select kernel',
            manager: options.manager
        }));
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        this.content.dispose();
        super.dispose();
    }
}
/**
 * Widget that contains the main view of the DocumentWidget.
 */
class BlocklyPanel extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Panel {
    /**
     * Construct a `ExamplePanel`.
     *
     * @param context - The documents context.
     */
    constructor(context, manager, rendermime) {
        super({
            layout: new _layout__WEBPACK_IMPORTED_MODULE_6__.BlocklyLayout(manager, context.sessionContext, rendermime)
        });
        this.addClass('jp-BlocklyPanel');
        this._context = context;
        // Load the content of the file when the context is ready
        this._context.ready.then(() => this._load());
        // Connect to the save signal
        this._context.saveState.connect(this._onSave, this);
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal.clearData(this);
        super.dispose();
    }
    _load() {
        // Loading the content of the document into the workspace
        const content = this._context.model.toJSON();
        this.layout.workspace = content;
    }
    _onSave(sender, state) {
        if (state === 'started') {
            const workspace = this.layout.workspace;
            this._context.model.fromJSON(workspace);
        }
    }
}


/***/ }),

/***/ "./style/icons/blockly_logo.svg":
/*!**************************************!*\
  !*** ./style/icons/blockly_logo.svg ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<svg\n   xmlns:dc=\"http://purl.org/dc/elements/1.1/\"\n   xmlns:cc=\"http://creativecommons.org/ns#\"\n   xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n   xmlns:svg=\"http://www.w3.org/2000/svg\"\n   xmlns=\"http://www.w3.org/2000/svg\"\n   xmlns:sodipodi=\"http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd\"\n   xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\"\n   id=\"Layer_6\"\n   data-name=\"Layer 6\"\n   viewBox=\"0 0 192 192\"\n   version=\"1.1\"\n   sodipodi:docname=\"logo-only.svg\"\n   inkscape:version=\"0.92.2pre0 (973e216, 2017-07-25)\"\n   inkscape:export-filename=\"/usr/local/google/home/epastern/Documents/Blockly Logos/Square/logo-only.png\"\n   inkscape:export-xdpi=\"96\"\n   inkscape:export-ydpi=\"96\">\n  <metadata\n     id=\"metadata913\">\n    <rdf:RDF>\n      <cc:Work\n         rdf:about=\"\">\n        <dc:format>image/svg+xml</dc:format>\n        <dc:type\n           rdf:resource=\"http://purl.org/dc/dcmitype/StillImage\" />\n        <dc:title>blockly-logo</dc:title>\n      </cc:Work>\n    </rdf:RDF>\n  </metadata>\n  <sodipodi:namedview\n     pagecolor=\"#ffffff\"\n     bordercolor=\"#666666\"\n     borderopacity=\"1\"\n     objecttolerance=\"10\"\n     gridtolerance=\"10\"\n     guidetolerance=\"10\"\n     inkscape:pageopacity=\"0\"\n     inkscape:pageshadow=\"2\"\n     inkscape:window-width=\"2560\"\n     inkscape:window-height=\"1379\"\n     id=\"namedview911\"\n     showgrid=\"false\"\n     inkscape:zoom=\"2\"\n     inkscape:cx=\"239.87642\"\n     inkscape:cy=\"59.742687\"\n     inkscape:window-x=\"0\"\n     inkscape:window-y=\"0\"\n     inkscape:window-maximized=\"1\"\n     inkscape:current-layer=\"g1013\" />\n  <defs\n     id=\"defs902\">\n    <style\n       id=\"style900\">.cls-1{fill:#4285f4;}.cls-2{fill:#c8d1db;}</style>\n  </defs>\n  <title\n     id=\"title904\">blockly-logo</title>\n  <g\n     id=\"g1013\"\n     transform=\"translate(23.500002,-7.9121105)\"\n     inkscape:export-xdpi=\"96\"\n     inkscape:export-ydpi=\"96\">\n    <path\n       id=\"path906\"\n       d=\"M 20.140625,32 C 13.433598,31.994468 7.9944684,37.433598 8,44.140625 V 148.85938 C 7.99447,155.56641 13.433598,161.00553 20.140625,161 h 4.726563 c 2.330826,8.74182 10.245751,14.82585 19.292968,14.83008 C 53.201562,175.81878 61.108176,169.73621 63.4375,161 h 4.841797 15.726562 c 4.418278,0 8,-3.58172 8,-8 V 40 l -8,-8 z\"\n       style=\"fill:#4285f4\"\n       inkscape:connector-curvature=\"0\"\n       sodipodi:nodetypes=\"ccccccccssccc\" />\n    <path\n       sodipodi:nodetypes=\"ccccccccccccccccc\"\n       inkscape:connector-curvature=\"0\"\n       id=\"path908\"\n       d=\"M 80.007812,31.994141 C 79.997147,49.696887 80,67.396525 80,85.109375 L 63.369141,75.710938 C 60.971784,74.358189 58.004891,76.087168 58,78.839844 v 40.621096 c 0.0049,2.75267 2.971786,4.48165 5.369141,3.1289 L 80,113.18945 v 37.5918 2.21875 8 h 8 1.425781 36.054689 c 6.36195,-2.6e-4 11.51927,-5.15758 11.51953,-11.51953 V 43.480469 C 136.97822,37.133775 131.8272,32.000222 125.48047,32 Z\"\n       style=\"fill:#c8d1db\" />\n  </g>\n</svg>\n");

/***/ })

}]);
//# sourceMappingURL=lib_index_js.cd35a695c43d64777f2e.js.map