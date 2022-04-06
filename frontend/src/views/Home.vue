<template>
  <div class="home">
    <div class="columns">
      <ArticleBox
        v-for="article in latestArticleListComputed"
        v-bind:key="article.id"
        v-bind:article="article"
      />
    </div>
    <!-- <MrkdownCompiler /> -->
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, onBeforeMount } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "vuex";
import { toast } from "bulma-toast";
import axios from "axios";

import ArticleBox from "../components/ArticleBox.vue";
// import { values } from "lodash";
export default defineComponent({
  name: "Home",
  components: {
    ArticleBox
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const store = useStore();

    const latestArticleList = ref("");
    const latestArticleListComputed = computed({
      get: () => latestArticleList.value,
      set: value => (latestArticleList.value = value)
    });

    const get_article_list = async () => {
      store.commit("setIsLoading", true);

      await axios
        .get(`api/v1/articles/articles/latest/list/`)
        .then(response => {
          latestArticleList.value = response.data;
        })
        .catch(error => {
          console.log(error.response.data);
          if (error.response.data.data.error == "DoseNotExist") {
            toast({
              message: "この記事は存在していません",
              type: "is-danger",
              dismissible: true,
              pauseOnHover: true,
              duration: 2000,
              position: "bottom-right"
            });
            router.push("/");
          }
        });
      store.commit("setIsLoading", false);
    };

    get_article_list();
    // onBeforeMount(() => {
    // });

    return {
      latestArticleListComputed
    };
  }
});
</script>

<style scoped></style>
