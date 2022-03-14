<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <MarkdownEditor />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import MarkdownEditor from "@/components/MarkdownEditor.vue"; // @ is an alias to /src
export default defineComponent({
  name: "Home",
  components: {
    MarkdownEditor
  }
});
</script>
