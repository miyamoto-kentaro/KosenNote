<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <h1>{{ book.title }}/{{ book.author }}/{{ book.year }}</h1>
  </div>
</template>

<script lang="ts">
interface Book {
  title: string;
  author: string;
  year: number;
}

import { defineComponent } from "vue";

export default defineComponent({
  name: "Home",
  data() {
    return {
      msg: "Hello TypeScript",
      book: {
        title: "Vue 3 Guide",
        author: "Vue Team",
        year: 2020,
      } as Book,
    };
  },
  computed: {
    getLength(): number {
      return this.msg.length;
    },
  },
  methods: {
    changeMsg(msg: string): string {
      return (this.msg = msg);
    },
  },
});
</script>
