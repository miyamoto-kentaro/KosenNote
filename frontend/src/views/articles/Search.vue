<template>
  <div class="page-search">
    <div class="columns is-multiline">
      <div class="column is-12">
        <h1 class="title">Search</h1>
      </div>

      <ArticleBox
        v-for="article in articleListComputed"
        v-bind:key="article.id"
        v-bind:article="article"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, onBeforeMount } from "vue";
import { useRouter, useRoute, onBeforeRouteUpdate } from "vue-router";
import { useStore } from "vuex";
import { toast } from "bulma-toast";
import axios from "axios";

import ArticleBox from "../../components/ArticleBox.vue";
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

    const articleList = ref<object[]>([]);
    const articleListComputed = computed({
      get: () => articleList.value,
      set: value => (articleList.value = value)
    });

    const errors = ref<string[]>([]);
    const errorsCompute = computed({
      get: () => errors.value,
      set: value => (errors.value = value)
    });

    const get_article_list = async (query: string | string[]) => {
      store.commit("setIsLoading", true);

      console.log(query);
      try {
        // バリデーション

        if (!route.params.query) {
          errorsCompute.value.push("検索ワードが入力されていません");
        }

        if (!errorsCompute.value.length) {
          await axios
            .get(`api/v1/articles/articles/search/${query}`)
            .then(response => {
              console.log(response.data);

              articleListComputed.value = response.data.data;
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
        } else {
          for (var error of errorsCompute.value) {
            toast({
              message: `${error}`,
              type: "is-danger",
              dismissible: true,
              pauseOnHover: true,
              duration: 2000,
              position: "bottom-right"
            });
          }
          errorsCompute.value = [];
        }
      } catch (err) {
        console.log(err);

        toast({
          message: "予期せぬエラー",
          type: "is-danger",
          dismissible: true,
          pauseOnHover: true,
          duration: 2000,
          position: "bottom-right"
        });
        router.push("/");
      }
      store.commit("setIsLoading", false);
    };
    onMounted(() => {
      get_article_list(route.params.query);
    });

    onBeforeRouteUpdate((to, from, next) => {
      get_article_list(to.params.query);

      next();
    });

    return {
      articleListComputed
    };
  }
});
</script>
