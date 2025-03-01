//@ts-check
"use strict"

// Backend
export { CoqWorker } from '../../../dist/backend.js';

// Frontend
import { CoqManager } from './coq-manager-tutorial.js';
export { PackageManager } from './coq-packages.js';
export { FormatPrettyPrint } from './format-pprint.js';
export { CmCoqProvider, Deprettify } from './cm-provider.js';

const scriptDir = import.meta.url.replace(/[^/]*$/, '');

const JsCoq = {
    backend: 'js',  /* 'js' or 'wa' */

    base_path: scriptDir ? `${scriptDir}../../../` : "./",
    node_modules_path: '',
    loaded: undefined,

    is_npm: false,  /* indicates that jsCoq was installed via `npm install` */

    load(...args) {
        let { jscoq_ids, jscoq_opts } = this._getopt('load', ...args);
        return this._load(jscoq_opts.base_path, jscoq_opts.node_modules_path).then(() => jscoq_opts);
    },

    _load(base_path, node_modules_path) {
        this.base_path = base_path;
        this.node_modules_path = node_modules_path;
        window.JsCoq = this; // atm this is still needed by UI addons
        return this.loaded ||
            (this.loaded = loadJsCoq(base_path, node_modules_path));
    },

    async start(...args) {
        let { jscoq_ids, jscoq_opts } = this._getopt('start', ...args);
        await this._load(jscoq_opts.base_path, jscoq_opts.node_modules_path);
        return new CoqManager(jscoq_ids, jscoq_opts);
    },

    /**
     * Parses "command line"-style arguments to `start()` and `load()`.
     * @param method name of method that invoked `_getopt` (for logging).
     * @param  {...any} args a sequence of values including
     *  * (string) base path for jsCoq resources
     *  * (string) node_modules path for library resources
     *  * (string[]) elements ids / CSS selectors designating interactive snippets
     *  * (object) options object passed to `CoqManager` (see `coq-manager.js`)
     * All arguments are optional. Assignment is done according to type.
     * @returns
     */
    _getopt(method, ...args) {

        var base_path = undefined,
            node_modules_path = undefined,
            jscoq_ids = ['ide-wrapper'],
            jscoq_opts = {};

        // Interpret args according to spec, skip missing values
        if (typeof args[0] === 'string') base_path = args.shift();
        if (typeof args[0] === 'string') node_modules_path = args.shift();
        if (Array.isArray(args[0])) jscoq_ids = args.shift();
        if (args[0]) jscoq_opts = args.shift();

        if (args.length > 0) console.warn(`too many arguments to JsCoq.${method}()`);

        // Backend setup
        jscoq_opts.backend = jscoq_opts.backend || this.backend;
        jscoq_opts.is_npm = this.is_npm;

        // Set base and node_modules path from options if not given, use defaults
        jscoq_opts.base_path = base_path || jscoq_opts.base_path || this.base_path;
        jscoq_opts.node_modules_path = node_modules_path
                                    || jscoq_opts.node_modules_path
                                    || jscoq_opts.base_path + (this.is_npm ? "../" : "node_modules/");

        return {jscoq_ids, jscoq_opts}
    },

    globalConfig(v) {
        const defaults = {features: []},
              ls = localStorage['jscoq:config'];
        try { var cfg = ls && JSON.parse(ls); }
        catch (e) { console.warn('(in local config)', ls, e); }
        if (v)
            localStorage['jscoq:config'] = JSON.stringify({...cfg, ...v})
        else return {...defaults, ...cfg};
    }
};

async function loadJsCoq(base_path, node_modules_path) {

    base_path = base_path.replace(/([^/])$/, '$1/');
    node_modules_path = node_modules_path.replace(/([^/])$/, '$1/');

    var files = {
        'css':  [node_modules_path + 'codemirror/lib/codemirror',
                 node_modules_path + 'codemirror/theme/blackboard',
                 node_modules_path + 'codemirror/theme/darcula',
                 node_modules_path + 'codemirror/addon/hint/show-hint',
                 node_modules_path + 'codemirror/addon/dialog/dialog',
                 base_path + 'frontend/classic/css/coq-log',
                 base_path + 'frontend/classic/css/coq-base',
                 base_path + 'frontend/classic/css/coq-light',
                 base_path + 'frontend/classic/css/coq-dark',
                 base_path + 'frontend/classic/css/settings']
    };

    for (let fn of files.css) loadCss(fn)
    // We don't need to load JS modules anymore, they follow from the imports!
    await whenReady();
};


/* boilerplate */
var loadCss = function(fn) {
    var link   = document.createElement("link");
    link.href  = fn + '.css';
    link.type  = "text/css";
    link.rel   = "stylesheet";
    document.head.appendChild(link);
};

var loadJs = function(fn) {
    return new Promise(function (resolve, error) {
        var script    = document.createElement('script');
        script.type   = 'text/javascript';
        script.src    = fn + '.js';
        script.onload = resolve;
        document.head.appendChild(script);
    });
};

/* Some boilerplate (for some reason `$(document).ready(..)` is not quite that) */
function whenReady() {
    return (document.readyState === 'complete') ? Promise.resolve()
        : new Promise(r =>
            document.addEventListener('readystatechange', () =>
                document.readyState === 'complete' && r()));
}

export { JsCoq, CoqManager }

// Local Variables:
// js-indent-level: 4
// End:
