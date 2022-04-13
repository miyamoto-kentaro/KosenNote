<template>
  <div class="column is-3 is-narrow">
    <div class="card">
      <header class="card-header">
        <p class="card-header-title article-title">
          {{ props.article.title }}
        </p>
        <button
          class="card-header-icon"
          aria-label="more options"
          @click="showArticleComputed = !showArticleComputed"
        >
          <span class="icon">
            <i class="kosen-note-icon-circle-down"></i>
          </span>
        </button>
      </header>
      <div class="card-content">
        <div class="content">
          <p v-if="props.article.author" class="is-size-6 lineClamp subtitle">
            作者：<router-link :to="author_profile">{{
              props.article.get_author_name
            }}</router-link>
          </p>
          <p v-else class="is-size-6 lineClamp subtitle">
            作者はアカウントを削除しました
          </p>
          <p class="is-size-6 has-text-grey lineClamp">
            タグ：<span
              class="tag is-light"
              v-for="tag in props.article.tags"
              v-bind:key="tag.id"
              v-bind:article="article"
            >
              <a @click="push_search(tag)">
                {{ tag }}
              </a></span
            >
          </p>
        </div>
      </div>
      <footer class="card-footer">
        <router-link
          v-bind:to="`/article-detail/${props.article.id}/`"
          class="button is-light mt-4"
          style="margin-left: auto;"
          >記事を見る</router-link
        >
      </footer>
    </div>

    <div class="modal " v-bind:class="{ 'is-active': showArticleComputed }">
      <div
        @click="showArticleComputed = !showArticleComputed"
        class="modal-background"
      ></div>
      <div class="modal-content">
        <article class="message">
          <div class="message-header article-title">
            <p>{{ props.article.title }}</p>
          </div>
          <div class="message-body">
            <MrkdownCompiler :text="article.content" />
          </div>
        </article>
        <button
          @click="showArticleComputed = !showArticleComputed"
          class="modal-close is-large"
          aria-label="close"
        ></button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import { toast } from "bulma-toast";
import axios from "axios";

import MrkdownCompiler from "../components/MrkdownCompiler.vue";

export default defineComponent({
  name: "ArticleBox",
  components: {
    MrkdownCompiler
  },
  props: {
    article: Object
  },
  setup(props) {
    const router = useRouter();
    const route = useRoute();
    const store = useStore();

    const showArticle = ref(false);
    const showArticleComputed = computed({
      get: () => showArticle.value,
      set: value => (showArticle.value = value)
    });

    const author_profile = computed(() => {
      if (props.article) {
        return "/profile/" + props.article.get_author_name + "/";
      } else {
        return "/";
      }
    });

    const push_search = (tag: string) => {
      router.push(`/search-article/${tag}`);
    };

    return {
      props,
      showArticleComputed,
      author_profile,
      push_search
    };
  }
});
</script>

<style scoped>
.image {
  margin-top: -1.25rem;
  margin-left: -1.25rem;
  margin-right: -1.25rem;
}
.lineClamp {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;

  /*IE対策*/
  line-height: 1.5em;
  max-height: 4.5em;
}
.article-title {
  /*上下方向にはみ出した要素ををスクロールさせる*/
  overflow-x: scroll;
  /*スクロールバー非表示（IE・Edge）*/
  -ms-overflow-style: none;
  /*スクロールバー非表示（Firefox）*/
  scrollbar-width: none;
}
.article-title::-webkit-scrollbar {
  display: none;
}
</style>
