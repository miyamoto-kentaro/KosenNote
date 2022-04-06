<template>
  <div id="MrkdownCompilerComponent">
    <div id="preview">
      <div class="content break-word">
        <!-- {{ props.text }} -->
        <div v-html="compiledMarkdownComputed"></div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent, computed } from "vue";
import { marked } from "marked";

export default defineComponent({
  name: "MrkdownCompilerComponent",
  props: {
    text: {
      type: String,
      required: true
    }
  },
  setup(props) {
    // markdownのコンパイラhtml
    const compiledMarkdownComputed = computed(() => marked.parse(props.text));

    return {
      compiledMarkdownComputed
    };
  }
});
</script>

<style scoped>
#preview {
  overflow: auto;
  line-height: 1.5em;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  font-size: 1em;
}

#preview >>> table {
  display: block;
  overflow-x: scroll;
}

.break-word {
  overflow-wrap: break-word;
}
</style>
