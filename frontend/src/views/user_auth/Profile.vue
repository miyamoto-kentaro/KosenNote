<template>
  <div class="page-my-account">
    <div class="tabs is-left">
      <h1 class="title">{{ username }}のアカウントページ</h1>
    </div>
    <div class="tabs is-right">
      <ul>
        <li v-bind:class="{ 'is-active': myArticle }">
          <a class="has-text-info" @click="getMyArticles">投稿した記事</a>
        </li>
        <!-- <li><a>Music</a></li>
        <li><a>Videos</a></li> -->
        <li v-bind:class="{ 'is-active': myGoods }">
          <a @click="getMyGoods" class="has-text-info">
            いいねした記事
          </a>
        </li>
        <li>
          <a
            class="show-modal has-text-danger"
            data-target="my-modal"
            @click="showModalEdit"
            >アカウント設定</a
          >
        </li>
      </ul>
    </div>

    <div class="modal" v-bind:class="{ 'is-active': showModal }">
      <div @click="showModalEdit" class="modal-background"></div>
      <div class="modal-content">
        <div class="card">
          <div class="card-content">
            <div class="content">
              本当にログアウトしますか？
              <p class="has-text-grey">
                一時保存していた記事のデータが消失します。はじめに、記事を保存しておくことをおすすめします。
                ログインページから再度ログインできます
              </p>
              <br />
              <p></p>
            </div>
            <div class="button is-danger" @click="logout">ログアウト</div>
          </div>
        </div>
      </div>
      <button
        @click="showModalEdit"
        class="modal-close is-large"
        aria-label="close"
      ></button>
    </div>

    <div class="columns is-multiline">
      <ArticleBox
        v-for="article in articles"
        v-bind:key="article.id"
        v-bind:article="article"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import { toast } from "bulma-toast";
import axios from "axios";

import ArticleBox from "@/components/ArticleBox.vue";

export default defineComponent({
  components: {
    ArticleBox
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const store = useStore();

    const myself = store.state.user;
    const username = route.params.username;

    const search_user = async () => {};

    return {
      username: username
    };
  }
});
</script>
