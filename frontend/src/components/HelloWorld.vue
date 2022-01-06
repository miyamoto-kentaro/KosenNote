<template>
  <h1>{{ fullName }} {{ this.user.age }}</h1>
</template>

<script lang="ts">
export interface User {
  firstName: string;
  lastName: string;
  age: number;
}

import { defineComponent, PropType } from "vue";
export default defineComponent({
  name: "HelloWorld",
  props: {
    user: {
      type: Object as PropType<User>,
      required: true,
    },
  },
  computed: {
    fullName(): string {
      return this.user.firstName + " " + this.user.lastName;
    },
  },
});
</script>
