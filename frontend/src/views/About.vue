<template>
  <div class="About">
    <HelloWorld :user="user" />
  </div>
</template>

<script lang="ts">
import {
  computed,
  defineComponent,
  reactive,
  watchEffect,
  onMounted,
} from "vue";

import HelloWorld, { User } from "../components/HelloWorld.vue";

export default defineComponent({
  name: "About",
  components: {
    HelloWorld,
  },
  setup() {
    const state = reactive<User>({
      firstName: "john",
      lastName: "doe",
      age: 30,
    });
    return {};
  },
  data() {
    return {
      person: {
        firstName: "John",
        lastName: "doe",
        age: 30,
      } as User,
    };
  },
  computed: {
    user(): User {
      return this.person;
    },
  },
});
</script>
