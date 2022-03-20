<template>
  <div id="MarkdownEditorComponent" class="box">
    <div class="toolkit">
      <nav class="navbar">
        <div class="navbar-start">
          <table class="table">
            <thead>
              <tr>
                <th>
                  <abbr title="undo">
                    <a @click="undo">
                      <span class="icon">
                        <i class="kosen-note-icon-undo"></i>
                      </span>
                    </a>
                  </abbr>
                </th>
                <th>
                  <abbr title="redo">
                    <a @click="insert_comment">
                      <span class="icon">
                        <i class="kosen-note-icon-redo"></i>
                      </span>
                    </a>
                  </abbr>
                </th>
                <th>|</th>
                <th>
                  <abbr title="redo">
                    <span class="icon">
                      <i class="kosen-note-icon-font-size"></i> </span
                  ></abbr>
                </th>
                <th>
                  <abbr title="redo">
                    <span class="icon">
                      <i class="kosen-note-icon-bold"></i> </span
                  ></abbr>
                </th>
                <th>
                  <abbr title="redo">
                    <span class="icon">
                      <i class="kosen-note-icon-underline"></i> </span
                  ></abbr>
                </th>
                <th>
                  <abbr title="redo">
                    <span class="icon">
                      <i class="kosen-note-icon-italic"></i> </span
                  ></abbr>
                </th>
                <th>
                  <abbr title="redo">
                    <span class="icon">
                      <i class="kosen-note-icon-strikethrough"></i> </span
                  ></abbr>
                </th>
                <th>|</th>
              </tr>
            </thead>
          </table>
        </div>
        <div class="navbar-end">
          <table class="table">
            <thead>
              <tr>
                <th>
                  <abbr title="font-size">
                    <span class="icon">
                      <i class="icon kosen-note-icon-font-size"></i> </span
                  ></abbr>
                </th>
                <th>Team</th>
                <th><abbr title="Played">Pld</abbr></th>
                <th><abbr title="Won">W</abbr></th>
                <th><abbr title="Drawn">D</abbr></th>
                <th><abbr title="Lost">L</abbr></th>
                <th><abbr title="Goals for">GF</abbr></th>
                <th><abbr title="Goals against">GA</abbr></th>
                <th><abbr title="Goal difference">GD</abbr></th>
                <th><abbr title="Points">Pts</abbr></th>
                <th>Qualification or relegation</th>
              </tr>
            </thead>
          </table>
        </div>
      </nav>
    </div>
    <div id="markdown-editor" class="columns is-gapless">
      <div class="column">
        <div class="control ">
          <textarea
            class="textarea has-fixed-size"
            :rows="text_row"
            ref="markdown_textarea"
            v-model="markdownTextComputed"
            @input="update"
          ></textarea>
        </div>
      </div>
      <div class="column">
        <div class="box markdown-preview" :style="stylePreview">
          <div class="content">
            <div v-html="compiledMarkdown"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent, ref, computed, onMounted } from "vue";
import { marked } from "marked";
import _ from "lodash";

interface HistoryStack {
    value: string,
    range: {
      start: number,
      end: number
    },
}

export default defineComponent({
  name: "MarkdownEditorComponent",
  setup() {
    // textareaのelement
    const markdown_textarea = ref<HTMLTextAreaElement>();

    // previewの高さを設定.
    const stylePreview = ref();

    // textareaのtextを保存
    const markdownText = ref("");

    // markdownTextのcomputed
    const markdownTextComputed = computed({
      get: () => markdownText.value,
      set: value => (markdownText.value = value)
    });

    // markdownのコンパイラhtml
    const compiledMarkdown = ref();

    // markdownをcompile
    const update = _.debounce(() => {
      setHistory()
      compiledMarkdown.value = marked.parse(markdownTextComputed.value);
      stylePreview.value = {height: markdown_textarea.value?.clientHeight + 'px'}
      // console.log(stylePreviewComputed);
    }, 300);

    // markdownTextの行数を計算
    const text_row = computed({
      get: () => {
        const row = markdownText.value.split(/\r\n|\r|\n/).length;
        if (row < 20) {
          return 20;
        } else {
          return row;
        }
      },
      set: () => null
    });

    // [insert content append]の文字列を挿入する。contentを選択する。
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

    const insert_comment = () => {
      if (markdown_textarea.value){
        insert('<h1>','message','</h1>',markdown_textarea.value)
      }
    }

    // historyを保存する
    var historyStack:HistoryStack[] = [];
    // 現在のhistoryindex
    var historyIndex:number = 0;

    // 任意のindexのhistoryをmarkdowntextに代入
    const goHistory = (index:number) => {
      const { value, range } = historyStack[index];
      markdownTextComputed.value = value
      markdown_textarea.value?.focus()

      setTimeout(() => markdown_textarea.value?.setSelectionRange(range.start,range.end))
    }

    const setHistory = () => {
      const range = getRange();
      const history:HistoryStack = {
        value: markdownTextComputed.value,
        range,
      };
      historyStack = historyStack.slice(0, historyIndex + 1);
      historyStack.push(history);
      console.log('history:',historyStack);
      historyIndex = historyStack.length - 1;
    }

    const getRange = () => {
        return {

          start: markdown_textarea.value?.selectionStart ?? 0,
          end: markdown_textarea.value?.selectionEnd ?? 0,
        }

    }

    const redo = () => {
      if (historyIndex < historyStack.length - 1) {
        historyIndex++;
        goHistory(historyIndex);
      }

    }
    const undo = () => {
      if (historyIndex > 0) {
        historyIndex--;
        console.log(historyIndex);

        goHistory(historyIndex);
      }
    }

    onMounted(() => {
      stylePreview.value = {height: markdown_textarea.value?.clientHeight + 'px'}
    });

    return {
      markdownTextComputed,
      compiledMarkdown,
      update,
      text_row,
      markdown_textarea,
      stylePreview,
      insert_comment,
      redo,
      undo
    };
  }
});
</script>

<style scoped>
#MarkdownEditorComponent {
  position: relative;
  height: 100%;
}
.markdown-preview {
  overflow: auto;
  line-height: 1.5em;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  font-size: 1em;
}
#markdown-editor {
  padding: 0 0 0 0;
}
.toolkit {
  position: sticky;
  top: 5%;
  z-index: 1;
}
</style>
