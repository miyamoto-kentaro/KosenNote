<template>
  <div id="editor" class="columns is-gapless markdown-editor">
    <div class="column">
      <div class="control editor-box">
        <textarea
          class="textarea has-fixed-size"
          rows="10"
          v-model="markdownTextComputed"
          @input="update"
        ></textarea>
      </div>
    </div>
    <div class="column">
      <div class="box markdown-preview">
        <div class="content">
          <div v-html="compiledMarkdown"></div>
        </div>
      </div>
    </div>
    <!-- <div v-html="compiledMarkdown"></div> -->
  </div>
</template>
<script lang="ts">
import { defineComponent, ref, computed } from "vue";
import { marked } from "marked";
import _ from "lodash";

export default defineComponent({
  name: "MarkdownEditor",
  setup() {
    const markdownText = ref("");

    const markdownTextComputed = computed({
      get: () => markdownText.value,
      set: value => (markdownText.value = value)
    });

    const compiledMarkdown = ref("");

    const update = _.debounce(() => {
      console.log("debug");

      compiledMarkdown.value = marked.parse(markdownTextComputed.value);
    }, 300);

    return {
      markdownTextComputed,
      compiledMarkdown,
      update
    };
  }
});
</script>

<style scoped>
.markdown-preview {
  overflow: auto;
  line-height: 1.5em;
  border: 2px solid #0a0;
  border-radius: 0.67em;
  padding: 0.5em;
  background-color: snow;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  font-size: 1em;
}
.markdown-editor {
  height: 100%;
}
</style>
