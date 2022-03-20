<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <MarkdownEditor />
    <p>{{ articleComputed }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from "vue";
import MarkdownEditor from "@/components/MarkdownEditor.vue"; // @ is an alias to /src
export default defineComponent({
  name: "Home",
  components: {
    MarkdownEditor
  },
  setup() {
    const article = ref("");
    const articleComputed = computed({
      get: () => article.value,
      set: value => (article.value = value)
    });
    return {
      articleComputed
    };
  }
});
</script>
