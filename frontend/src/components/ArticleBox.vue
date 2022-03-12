<template>
  <div class="column is-3 is-narrow">
    <div class="card">
      <header class="card-header">
        <p class="card-header-title">
          {{ article.title }}
        </p>
        <button
          class="card-header-icon"
          aria-label="more options"
          v-on:click="contant_activate"
        >
          <span class="icon">
            <i class="icon v-md-icon-arrow-down" aria-hidden="true"></i>
          </span>
        </button>
      </header>
      <div class="card-content">
        <div class="content">
          <p v-if="article.author" class="is-size-6 lineClamp subtitle">
            作者：{{ article.get_author_name }}
          </p>
          <p v-else class="is-size-6 lineClamp subtitle">
            作者はアカウントを削除しました
          </p>
          <p class="is-size-6 has-text-grey lineClamp">
            タグ：<span
              class="tag is-light"
              v-for="tag in article.tags"
              v-bind:key="tag.id"
              v-bind:article="article"
            >
              <router-link
                v-bind:to="{ path: 'search', query: { query: tag } }"
                style="color:black"
              >
                {{ tag }}
              </router-link></span
            >
          </p>
        </div>
      </div>
      <footer class="card-footer">
        <router-link
          v-bind:to="`/article/${article.id}/`"
          class="button is-light mt-4"
          style="margin-left: auto;"
          >記事を見る</router-link
        >
      </footer>
    </div>

    <div class="modal " v-bind:class="{ 'is-active': contant_active }">
      <div @click="contant_activate" class="modal-background"></div>
      <div class="modal-content">
        <article class="message">
          <div class="message-header">
            <p>{{ article.title }}</p>
          </div>
          <div class="message-body">
            <v-md-preview
              class="article-content"
              :text="article.content"
            ></v-md-preview>
          </div>
        </article>
        <button
          @click="contant_activate"
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

export default defineComponent({
  setup() {
    const router = useRouter();
    const route = useRoute();
    const store = useStore();
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
</style>
