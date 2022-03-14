<template>
  <div id="editor" class="columns">
    <div class="column">
      <textarea
        class="textarea"
        rows="10"
        v-model="markdownTextComputed"
        @input="update"
      ></textarea>
    </div>
    <div class="column">
      <div class="card">
        <div class="card-content">
          <div v-html="compiledMarkdown" class="content"></div>
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
