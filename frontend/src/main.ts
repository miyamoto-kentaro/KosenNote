import { createApp } from 'vue'
import axios from 'axios'
import App from './App.vue'
import router from './router'
import { store } from './store'

import VMdEditor from "@kangc/v-md-editor"
import "@kangc/v-md-editor/lib/style/base-editor.css"
import VMdPreview from "@kangc/v-md-editor/lib/preview"
import "@kangc/v-md-editor/lib/style/preview.css"
import githubTheme from "@kangc/v-md-editor/lib/theme/github.js"
import "@kangc/v-md-editor/lib/theme/style/github.css"
import enUS from "@kangc/v-md-editor/lib/lang/en-US"
import hljs from "highlight.js"

import createTipPlugin from "@kangc/v-md-editor/lib/plugins/tip/index"
import "@kangc/v-md-editor/lib/plugins/tip/tip.css"

import Codemirror from "codemirror"
import "codemirror/mode/markdown/markdown"
import "codemirror/mode/javascript/javascript"
import "codemirror/mode/css/css"
import "codemirror/mode/htmlmixed/htmlmixed"
import "codemirror/mode/vue/vue"
import "codemirror/mode/d/d"
import "codemirror/mode/django/django"
import "codemirror/mode/dockerfile/dockerfile"
import "codemirror/mode/elm/elm"
import "codemirror/mode/go/go"
import "codemirror/mode/groovy/groovy"
import "codemirror/mode/jinja2/jinja2"
import "codemirror/mode/nginx/nginx"
import "codemirror/mode/perl/perl"
import "codemirror/mode/php/php"
import "codemirror/mode/powershell/powershell"
import "codemirror/mode/python/python"
import "codemirror/mode/ruby/ruby"
import "codemirror/mode/sass/sass"
import "codemirror/mode/scheme/scheme"
import "codemirror/mode/sql/sql"
import "codemirror/mode/xml/xml"
import "codemirror/mode/yaml/yaml"
import "codemirror/mode/yaml-frontmatter/yaml-frontmatter"

import "codemirror/addon/edit/closebrackets"
import "codemirror/addon/edit/closetag"
import "codemirror/addon/edit/matchbrackets"
import "codemirror/addon/display/placeholder"
import "codemirror/addon/selection/active-line"
import "codemirror/addon/scroll/simplescrollbars"
import "codemirror/addon/scroll/simplescrollbars.css"
import "codemirror/lib/codemirror.css"

import createKatexPlugin from "@kangc/v-md-editor/lib/plugins/katex/cdn"
import createMermaidPlugin from "@kangc/v-md-editor/lib/plugins/mermaid/cdn"
import "@kangc/v-md-editor/lib/plugins/mermaid/mermaid.css"
import createTodoListPlugin from "@kangc/v-md-editor/lib/plugins/todo-list/index"
import "@kangc/v-md-editor/lib/plugins/todo-list/todo-list.css"
import createLineNumbertPlugin from "@kangc/v-md-editor/lib/plugins/line-number/index"
import createCopyCodePlugin from "@kangc/v-md-editor/lib/plugins/copy-code/index"
import "@kangc/v-md-editor/lib/plugins/copy-code/copy-code.css"
import createAlignPlugin from "@kangc/v-md-editor/lib/plugins/align"

// // Font Awesome
// import { library } from "@fortawesome/fontawesome-svg-core"
// import { faLeaf } from "@fortawesome/free-solid-svg-icons"
// import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"

// import "@/assets/css/font.css"

// library.add(faLeaf)

VMdEditor.Codemirror = Codemirror

VMdEditor.use(githubTheme, {
    Hljs: hljs,
    config: {
        toc: {
            includeLevel: [1, 2],
        },
    },
})
    .use(createTipPlugin())
    .use(createKatexPlugin())
    .use(createMermaidPlugin())
    .use(createTodoListPlugin())
    .use(createLineNumbertPlugin())
    .use(createCopyCodePlugin())
    .use(createAlignPlugin())

VMdEditor.lang.use("en-US", enUS)

VMdPreview.Codemirror = Codemirror
VMdPreview.use(githubTheme, {
    Hljs: hljs,
})
    .use(createTipPlugin())
    .use(createKatexPlugin())
    .use(createMermaidPlugin())
    .use(createTodoListPlugin())
    .use(createLineNumbertPlugin())
    .use(createCopyCodePlugin())
    .use(createAlignPlugin())

axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL

createApp(App)
    .use(store)
    .use(router)
    .use(VMdEditor)
    .use(VMdPreview)
    .mount('#app')