<template>
  <div class="page-my-account">
    <div class="tabs is-left">
      <h1 class="title">{{ usernameComputed }}のプロフィール</h1>
    </div>
    <div class="tabs is-right">
      <ul>
        <li :class="{ 'is-active': showPanelComputed == 0 }">
          <a class="has-text-info" @click="showPanelComputed = 0"
            >投稿した記事</a
          >
        </li>
        <!-- <li><a>Music</a></li>
        <li><a>Videos</a></li> -->
        <li :class="{ 'is-active': showPanelComputed == 1 }">
          <a class="has-text-info" @click="showPanelComputed = 1">
            いいねした記事
          </a>
        </li>

        <li>
          <a
            class="show-modal has-text-info"
            data-target="my-modal"
            @click="showPanelComputed = 2"
            >アカウント設定</a
          >
        </li>
      </ul>
    </div>

    <div
      class="columns is-multiline panel-1"
      :class="{ 'dont-show': showPanelComputed != 0 }"
    >
      <ArticleBox
        v-for="article in articlesComputed"
        v-bind:key="article.id"
        v-bind:article="article"
      />
    </div>

    <div
      class="columns is-multiline panel-1"
      :class="{ 'dont-show': showPanelComputed != 1 }"
    >
      <ArticleBox
        v-for="article in goodsComputed"
        v-bind:key="article.id"
        v-bind:article="article"
      />
    </div>

    <div class="panel-1" :class="{ 'dont-show': showPanelComputed != 2 }">
      <nav class="panel">
        <p class="panel-heading">
          アカウント設定
        </p>
        <p class="panel-tabs">
          <a class="is-active">All</a>
        </p>
        <a class="panel-block" @click="showUserConfPanelComputed = 1">
          ユーザー名の変更
        </a>
        <a class="panel-block">
          メールアドレスの変更
        </a>
        <router-link to="/reset-password/send-mail/" class="panel-block"
          >パスワードの変更</router-link
        >
        <a
          class="panel-block has-text-danger"
          @click="showUserConfPanelComputed = 3"
        >
          ログアウト
        </a>
      </nav>
    </div>

    <div class="modal" :class="{ 'is-active': showUserConfPanelComputed == 1 }">
      <div
        @click="showUserConfPanelComputed = 0"
        class="modal-background"
      ></div>
      <div class="modal-content">
        <div class="card">
          <div class="card-content">
            <form @submit.prevent="update_username">
              <div class="field">
                <p class="control">
                  <input
                    class="input"
                    type="text"
                    placeholder="新しいユーザー名"
                    v-model="next_usernameComputed"
                  />
                </p>
              </div>
              <div class="field">
                <p class="control">
                  <button class="button is-success">
                    変更
                  </button>
                </p>
              </div>
            </form>
          </div>
        </div>
      </div>
      <button
        @click="showUserConfPanelComputed = 0"
        class="modal-close is-large"
        aria-label="close"
      ></button>
    </div>
    <div class="modal" :class="{ 'is-active': showUserConfPanelComputed == 3 }">
      <div
        @click="showUserConfPanelComputed = 0"
        class="modal-background"
      ></div>
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
        @click="showUserConfPanelComputed = 0"
        class="modal-close is-large"
        aria-label="close"
      ></button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, computed, onMounted } from "vue";
import {
  useRoute,
  useRouter,
  onBeforeRouteLeave,
  onBeforeRouteUpdate
} from "vue-router";
import { useStore } from "vuex";
import { toast } from "bulma-toast";
import axios from "axios";

import ArticleBox from "../../components/ArticleBox.vue";

export default defineComponent({
  name: "Profile",
  components: {
    ArticleBox
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const store = useStore();

    const showPanel = ref<number>(0);
    const showPanelComputed = computed({
      get: () => showPanel.value,
      set: value => (showPanel.value = value)
    });

    const showUserConfPanel = ref<number>(0);
    const showUserConfPanelComputed = computed({
      get: () => showUserConfPanel.value,
      set: value => (showUserConfPanel.value = value)
    });

    // const SwitchshowPanel = (num: number) => {
    //   showPanelComputed.value = num;
    // };

    const articles = ref([]);
    const articlesComputed = computed({
      get: () => articles.value,
      set: value => (articles.value = value)
    });

    const goods = ref([]);
    const goodsComputed = computed({
      get: () => goods.value,
      set: value => (goods.value = value)
    });

    const username = ref<string>("");
    const usernameComputed = computed({
      get: () => username.value,
      set: value => (username.value = value)
    });

    const next_username = ref<string>("");
    const next_usernameComputed = computed({
      get: () => next_username.value,
      set: value => (next_username.value = value)
    });

    const search_user = async (username: string | string[]) => {
      store.commit("setIsLoading", true);
      const FormData = {
        username: username
      };
      console.log(route.params.username);

      await axios
        .post(`api/v1/articles/profile/`, FormData)
        .then(response => {
          console.log(response.data);
          usernameComputed.value = response.data.data.profile.username;
          articlesComputed.value = response.data.data.article_list;
          goodsComputed.value = response.data.data.goods;

          // username.value = response.data;
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

    const update_username = async () => {
      store.commit("setIsLoading", true);
      console.log(next_usernameComputed);

      const FormData = {
        username: next_usernameComputed.value
      };

      await axios
        .put(`api/v1/users/users/update/`, FormData)
        .then(response => {
          console.log(response.data);

          store.commit("setUser", response.data.data);
          showUserConfPanelComputed.value = 0;
          toast({
            message: `ユーザー名を変更しました\nNew ${store.state.user.username}`,
            type: "is-success",
            dismissible: true,
            pauseOnHover: true,
            duration: 2000,
            position: "bottom-right"
          });
          router.push(`/profile/${store.state.user.username}`);
        })
        .catch(error => {
          console.log(error.response.data);
          if (error.response.data.data.error == "DoseNotExist") {
            toast({
              message: "このユーザーは存在していません",
              type: "is-danger",
              dismissible: true,
              pauseOnHover: true,
              duration: 2000,
              position: "bottom-right"
            });
            router.push("/");
          } else if (error.response.data.data.username) {
            if (
              error.response.data.data.username[0] ==
              ["A user with that username already exists."]
            ) {
              toast({
                message: "このユーザー名は既に使用されています",
                type: "is-danger",
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: "bottom-right"
              });
            }
          }
        });
      store.commit("setIsLoading", false);
    };

    const logout = () => {
      store.commit("setIsLoading", true);
      store.commit("removeToken");
      store.commit("removeUser");
      store.commit("setIsLoading", false);
      router.push("/");
    };

    onBeforeRouteUpdate((to, from, next) => {
      console.log(to.params.username);

      search_user(to.params.username);
      next();
    });

    onMounted(() => {
      console.log("mounted");

      search_user(route.params.username);
      console.log(showPanelComputed.value);
    });

    return {
      usernameComputed,
      articlesComputed,
      goodsComputed,
      showPanelComputed,
      showUserConfPanelComputed,
      logout,
      next_usernameComputed,
      update_username
    };
  }
});
</script>

<style scoped>
.dont-show {
  display: none;
  height: 0;
  width: 0;
}
</style>
