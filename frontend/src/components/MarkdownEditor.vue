<template>
  <div id="MarkdownEditorComponent" class="box">
    <div id="toolkit">
      <nav class="breadcrumb" aria-label="breadcrumbs">
        <ul>
          <li>
            <abbr title="undo">
              <a @click="undo">
                <span class="icon">
                  <i class="kosen-note-icon-undo"></i>
                </span>
              </a>
            </abbr>

            <abbr title="redo">
              <a @click="redo">
                <span class="icon">
                  <i class="kosen-note-icon-redo"></i>
                </span>
              </a>
            </abbr>
          </li>
          <li>
            <abbr title="font-size">
              <div
                class="dropdown"
                v-bind:class="{
                  'is-active': showFontSizeMenuComputed
                }"
              >
                <div class="dropdown-trigger">
                  <a
                    aria-haspopup="true"
                    aria-controls="dropdown-menu"
                    @click="
                      showFontSizeMenuComputed = !showFontSizeMenuComputed
                    "
                  >
                    <span class="icon">
                      <i class="kosen-note-icon-font-size"></i>
                    </span>
                  </a>
                </div>
                <div class="dropdown-menu" id="dropdown-menu" role="menu">
                  <div class="dropdown-content">
                    <a class="dropdown-item" @click="font_size('1')">
                      h1
                    </a>
                    <a class="dropdown-item" @click="font_size('2')">
                      h2
                    </a>
                    <a class="dropdown-item" @click="font_size('3')">
                      h3
                    </a>
                    <a class="dropdown-item" @click="font_size('4')">
                      h4
                    </a>
                  </div>
                </div>
              </div>
            </abbr>
            <abbr title="color">
              <div
                class="dropdown"
                v-bind:class="{ 'is-active': showColorMenuComputed }"
              >
                <div class="dropdown-trigger">
                  <a
                    aria-haspopup="true"
                    aria-controls="dropdown-menu"
                    @click="showColorMenuComputed = !showColorMenuComputed"
                  >
                    <span class="icon">
                      <i class="kosen-note-icon-droplet"></i>
                    </span>
                  </a>
                </div>
                <div class="dropdown-menu" id="dropdown-menu" role="menu">
                  <div class="dropdown-content">
                    <a class="dropdown-item" @click="color('red')">
                      <span style="color: red; ">red</span>
                    </a>
                    <a class="dropdown-item" @click="color('blue')">
                      <span style="color: blue; ">blue</span>
                    </a>
                    <a class="dropdown-item" @click="color('green')">
                      <span style="color: green; ">green</span>
                    </a>
                    <a class="dropdown-item" @click="color('yellow')">
                      <span style="color: yellow; ">yellow</span>
                    </a>
                  </div>
                </div>
              </div>
            </abbr>
            <abbr title="block_quote">
              <a @click="block_quote">
                <span class="icon">
                  <i class="kosen-note-icon-quotes-left"></i>
                </span>
              </a>
            </abbr>
          </li>
          <li>
            <abbr title="bold">
              <a @click="bold">
                <span class="icon">
                  <i class="kosen-note-icon-bold"></i>
                </span>
              </a>
            </abbr>
            <abbr title="underline">
              <a @click="underline">
                <span class="icon">
                  <i class="kosen-note-icon-underline"></i>
                </span>
              </a>
            </abbr>
            <abbr title="italic">
              <a @click="italic">
                <span class="icon">
                  <i class="kosen-note-icon-italic"></i>
                </span>
              </a>
            </abbr>
          </li>
          <li>
            <abbr title="text-align-left">
              <a @click="text_align('left')">
                <span class="icon">
                  <i class="kosen-note-icon-paragraph-left"></i>
                </span>
              </a>
            </abbr>
            <abbr title="text-align-center">
              <a @click="text_align('center')">
                <span class="icon">
                  <i class="kosen-note-icon-paragraph-center"></i>
                </span>
              </a>
            </abbr>
            <abbr title="text-align-right">
              <a @click="text_align('right')">
                <span class="icon">
                  <i class="kosen-note-icon-paragraph-right"></i>
                </span>
              </a>
            </abbr>
          </li>
          <li>
            <abbr title="push_list">
              <a @click="push_list">
                <span class="icon">
                  <i class="kosen-note-icon-list2"></i>
                </span>
              </a>
            </abbr>
            <abbr title="push_table">
              <a @click="push_table">
                <span class="icon">
                  <i class="kosen-note-icon-table2"></i>
                </span>
              </a>
            </abbr>
            <abbr title="insert_link">
              <a @click="insert_link">
                <span class="icon">
                  <i class="kosen-note-icon-section"></i>
                </span>
              </a> </abbr
            ><abbr title="insert_image">
              <div
                class="dropdown"
                v-bind:class="{
                  'is-active': showImageOptionComputed
                }"
              >
                <div class="dropdown-trigger">
                  <a
                    aria-haspopup="true"
                    aria-controls="dropdown-menu"
                    @click="showImageOptionComputed = !showImageOptionComputed"
                  >
                    <span class="icon">
                      <i class="kosen-note-icon-image"></i>
                    </span>
                  </a>
                </div>
                <div class="dropdown-menu" id="dropdown-menu" role="menu">
                  <div class="dropdown-content">
                    <a class="dropdown-item" @click="insert_image_URL">
                      with URL
                    </a>
                    <a
                      class="dropdown-item"
                      @click="insert_image_with_google_drive"
                    >
                      with GoogleDrive
                    </a>
                  </div>
                </div>
              </div>
            </abbr>
            <abbr title="insert_code">
              <a @click="insert_code">
                <span class="icon">
                  <i class="kosen-note-icon-embed2"></i>
                </span>
              </a>
            </abbr>
          </li>
        </ul>
      </nav>
    </div>
    <div id="markdown-editor" class="columns">
      <div class="column">
        <div class="columns is-gapless">
          <div id="editor" class="column">
            <div class="control ">
              <textarea
                id="editor-textarea"
                class="textarea has-fixed-size"
                ref="markdown_textarea"
                v-model="markdownTextComputed"
                @input="input_event"
                @change="update"
                @click="update"
                @paste="update"
                @keydown.tab.prevent
                @keydown.ctrl.z.prevent.exact="undo"
                @keydown.meta.z.prevent.exact="undo"
                @keydown.ctrl.y.prevent.exact="redo"
                @keydown.meta.y.prevent.exact="redo"
                @keydown.ctrl.s.prevent.exact="save_article"
                @keydown.meta.s.prevent.exact="save_article"
                @keyup.shift.up.exact="update"
                @keyup.shift.down.exact="update"
                @keyup.shift.left.exact="update"
                @keyup.shift.right.exact="update"
              ></textarea>
            </div>
          </div>
          <div id="preview" class="column">
            <div class="box" ref="markdown_preview">
              <div class="content break-word">
                <div v-html="compiledMarkdownComputed"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent, ref, computed, onMounted, onBeforeUnmount, onUnmounted  } from "vue";
import { marked } from "marked";
import _, { values } from "lodash";

interface HistoryStack {
    value: string,
    range: {
      start: number,
      end: number
    },
}


export default defineComponent({
  name: "MarkdownEditorComponent",
  props: {
    value: String
  },
  setup(props, { emit }) {

    onMounted(() => {
      window.addEventListener('resize', init_style);
      update()
      init_style()
    });

    // Elementの取得
    const markdown_textarea = ref<HTMLTextAreaElement>();
    const markdown_preview = ref<HTMLElement>()

    // styleの初期化
    const init_style = () => {
      if(markdown_textarea.value && markdown_preview.value){
        // textareaの高さを初期化
        markdown_textarea.value.style.height = "0px"
        markdown_textarea.value.style.height = [markdown_textarea.value.scrollHeight, "px"].join("")

        markdown_textarea.value.style.minHeight = markdown_preview.value.clientHeight + "px"
        // previewのmax-widthを初期化
        markdown_preview.value.style.maxWidth = markdown_textarea.value.clientWidth + "px"

      }
    }

    // textareaのtextを保存
    const markdownText = ref("");
    // markdownTextのcomputed
    const markdownTextComputed = computed({
      get: () => markdownText.value,
      set: value => {
          return markdownText.value = value
        }
    });
    // props.valueを代入
    markdownTextComputed.value = props.value ?? ""

    // previewのHTMLElement
    const compiledMarkdown = ref();
    // previewのHTMLElementのcomputed
    const compiledMarkdownComputed = computed({
      get: () => compiledMarkdown.value,
      set: value => compiledMarkdown.value = value
    })

    // markdownTextComputedからcompiledMarkdownを生成
    const compile_markdown = () => {
      compiledMarkdownComputed.value = marked.parse(markdownTextComputed.value);
    }


    // 編集履歴系
    // 編集履歴を格納するlist
    var historyStack:HistoryStack[] = [];
    // 現在のhistoryindex
    var historyIndex:number = 0;

    // 選択範囲をget
    const getRange = () => {
      return {
        start: markdown_textarea.value?.selectionStart ?? 0,
          end: markdown_textarea.value?.selectionEnd ?? 0,
        }
    }
    // historyを保存する
    const setHistory = () => {
      const range = getRange();
      const history:HistoryStack = {
        value: markdownTextComputed.value,
        range,
      };
      historyStack = historyStack.slice(0, historyIndex + 1);
      historyStack.push(history);
      // console.log('history:',historyStack);
      historyIndex = historyStack.length - 1;
    }

    // 任意のindexのhistoryをmarkdowntextに代入
    const goHistory = (index:number) => {
      const { value, range } = historyStack[index];
      markdownTextComputed.value = value
      markdown_textarea.value?.focus()

      setTimeout(() => markdown_textarea.value?.setSelectionRange(range.start,range.end))
    }


    // textareaが変更したときの処理
    const update = _.debounce(() => {
      compile_markdown()
      setHistory()
      update_props()
    }, 300);

    // textareaにinputされた時のイベント
    const input_event = () =>{
      update()
      init_style()
    }

    // propsをparentに送る
    const update_props = () => {
      emit('update_props',  String(markdownText.value))
      // console.log(markdownText.value);
    }

    // ctrl + sのイベント
    const save_article = () => {
      emit('save_article')
    }

    // Toolkit
    const redo = () => {
      if (historyIndex < historyStack.length - 1) {
        historyIndex++;
        goHistory(historyIndex);

        compile_markdown()
      }

    }
    const undo = () => {
      if (historyIndex > 0) {
        historyIndex--;
        // console.log(historyIndex);

        goHistory(historyIndex);

        compile_markdown()
      }
    }

    const insert = (insert_text:string,content:string,append_text:string,target_textarea:HTMLTextAreaElement)  => {
      const selectionStart = target_textarea.selectionStart;
      const selectionEnd = target_textarea.selectionEnd;
      const startText = target_textarea.value.slice(0, selectionStart);
      const endText = target_textarea.value.slice(selectionEnd);
      // target_textarea.value = startText + insert_text + endText;
      markdownTextComputed.value = startText + insert_text + content + append_text + endText;
      update()
      // 挿入文字列の末尾にカーソルを移動させる
      target_textarea.focus();
      // target_textarea.setSelectionRange(0,1)
      const cursor = selectionStart + insert_text.length
      setTimeout(() => target_textarea.setSelectionRange(cursor, cursor+content.length))
    }

    const font_size = (size:string) => {
      if (markdown_textarea.value){
        insert('<h'+size+'>','message','</h'+size+'>',markdown_textarea.value)
        showFontSizeMenuComputed.value = false
      }
    }
    const showFontSizeMenu = ref(false)
    const showFontSizeMenuComputed = computed({
      get: () => showFontSizeMenu.value,
      set: value => (showFontSizeMenu.value = value)
    })

    const color = (color:string) => {
      if (markdown_textarea.value){
        insert(`<span style='color: ${color}; '>`,'message','</span>',markdown_textarea.value)
        showColorMenuComputed.value = false
      }
    }
    const showColorMenu = ref(false)
    const showColorMenuComputed = computed({
      get: () => showColorMenu.value,
      set: value => (showColorMenu.value = value)
    })

    const bold = () => {
      if (markdown_textarea.value){
        insert("<b>",'message',"</b>",markdown_textarea.value)
      }

    }

    const underline = () => {

      if (markdown_textarea.value){
        insert("<ins>",'message',"</ins>",markdown_textarea.value)
      }
    }
    const italic = () => {

      if (markdown_textarea.value){
        insert("<i>",'message',"</i>",markdown_textarea.value)
      }
    }
    const block_quote = () => {

      if (markdown_textarea.value){
        insert("> ",'message',"",markdown_textarea.value)
      }
    }


    const text_align = (direction:string) => {

      if (markdown_textarea.value){
        insert(`<div style='text-align: ${direction}; '>\n`,'message','\n</div>',markdown_textarea.value)
      }
    }
    const push_list = () => {

      if (markdown_textarea.value){
        insert("- ",'message',"",markdown_textarea.value)
      }
    }
    const push_table = () => {

      if (markdown_textarea.value){
        insert("|","column1","|column2|column3|\n|-|-|-|\n|content1|content2|content3|",markdown_textarea.value)
      }
    }
    const insert_link = () => {

      if (markdown_textarea.value){
        insert("<a href='https://' target='_blank'>","content","</a>",markdown_textarea.value)
      }
    }
    const insert_image_URL = () => {

      if (markdown_textarea.value){
        insert("<img src='","content","'></img>",markdown_textarea.value)
      }
      showImageOptionComputed.value = false
    }
    const insert_image_with_google_drive = () => {

      if (markdown_textarea.value){
        insert("<img src='https://drive.google.com/uc?id=","imageID", "'>",markdown_textarea.value)
      }
      showImageOptionComputed.value = false
    }
    const showImageOption = ref(false)
    const showImageOptionComputed = computed({
      get: () => showImageOption.value,
      set: value => (showImageOption.value = value)
    })
    const insert_code = () => {
      if (markdown_textarea.value){
        insert("``` language\n","content", "\n```",markdown_textarea.value)
      }
      showImageOptionComputed.value = false
    }


    return {
      markdownTextComputed,
      compiledMarkdownComputed,
      update,
      input_event,
      markdown_textarea,
      markdown_preview,
      redo,
      undo,
      font_size,
      showFontSizeMenuComputed,
      color,
      showColorMenuComputed,
      bold,
      underline,
      italic,
      text_align,
      block_quote,
      push_list,
      push_table,
      insert_link,
      insert_image_URL,
      insert_image_with_google_drive,
      showImageOptionComputed,
      insert_code,
      save_article,
    };
  }
});
</script>

<style scoped>
#MarkdownEditorComponent {
  position: relative;
  height: 100%;
}
#editor-textarea {
  max-height: 100%;
  min-height: 440px;
  /*上下方向にはみ出した要素ををスクロールさせる*/
  overflow-y: hidden;
}

#preview {
  min-height: 440px;
}

#preview >>> table {
  display: block;
  overflow-x: scroll;
}
#preview >>> .box {
  height: 100%;
}

.break-word {
  overflow-wrap: break-word;
}

#toolkit {
  overflow-wrap: break-word;
  position: sticky;
  top: 5%;
  z-index: 1;
}
</style>
