<template>
  <div class="page-profile">
    <div class="is-left">
      <h1 class="title">{{ usernameComputed }}</h1>
    </div>
    <div class="tag is-left">
      <a class="tag" @click="showPanelComputed = 3">
        フォロー {{ follow_toComputed.length }}
      </a>
      <a class="tag" @click="showPanelComputed = 4">
        フォロワー {{ followerComputed.length }}
      </a>
    </div>
    <div class="tabs is-right">
      <ul>
        <li :class="{ 'is-active': showPanelComputed == 0 }">
          <a class="has-text-info" @click="showPanelComputed = 0">
            <span class="icon"> <i class="icon kosen-note-icon-book"></i> </span
            >記事</a
          >
        </li>
        <!-- <li><a>Music</a></li>
        <li><a>Videos</a></li> -->
        <li :class="{ 'is-active': showPanelComputed == 1 }">
          <a class="has-text-info" @click="showPanelComputed = 1"
            ><span class="icon">
              <i class="icon kosen-note-icon-heart"></i>
            </span>

            いいね
          </a>
        </li>

        <li v-if="ItmeComputed == true">
          <a
            class="show-modal has-text-info"
            data-target="my-modal"
            @click="showPanelComputed = 2"
            >アカウント設定</a
          >
        </li>
        <li v-else>
          <a
            class="show-modal has-text-info"
            data-target="my-modal"
            @click="follow"
            v-if="onfollowComputed == false"
            >フォロー</a
          >
          <a
            class="show-modal has-text-danger"
            data-target="my-modal"
            @click="follow"
            v-if="onfollowComputed == true"
            >フォローを外す</a
          >
        </li>
      </ul>
    </div>

    <div
      class="columns is-multiline panel-0"
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

    <div class="panel-2" :class="{ 'dont-show': showPanelComputed != 2 }">
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
        <router-link to="/reset-email/send-mail/" class="panel-block"
          >メールアドレスの変更</router-link
        >
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
    <div
      class="columns is-multiline panel-3"
      :class="{ 'dont-show': showPanelComputed != 3 }"
    >
      <nav class="panel">
        <p class="panel-heading">フォロー {{ follow_toComputed.length }}</p>
        <!-- <div class="panel-block">
          <p class="control has-icons-left">
            <input class="input" type="text" placeholder="Search" />
            <span class="icon is-left">
              <i class="fas kosen-note-icon-search" aria-hidden="true"></i>
            </span>
          </p>
        </div> -->
        <a
          class="panel-block"
          v-for="follow_to_user in follow_toComputed"
          v-bind:key="follow_to_user.id"
          v-bind:follow_to_user="follow_to_user"
          @click="push_to_profile(follow_to_user.get_followed_user_name)"
        >
          {{ follow_to_user.get_followed_user_name }}
        </a>
      </nav>
    </div>
    <div
      class="columns is-multiline panel-1"
      :class="{ 'dont-show': showPanelComputed != 4 }"
    >
      <nav class="panel">
        <p class="panel-heading">フォロワー {{ followerComputed.length }}</p>
        <!-- <div class="panel-block">
          <p class="control has-icons-left">
            <input class="input" type="text" placeholder="Search" />
            <span class="icon is-left">
              <i class="fas kosen-note-icon-search" aria-hidden="true"></i>
            </span>
          </p>
        </div> -->
        <a
          class="panel-block"
          v-for="follower in followerComputed"
          v-bind:key="follower.id"
          v-bind:follower="follower"
          @click="push_to_profile(follower.get_follower_name)"
        >
          {{ follower.get_follower_name }}
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

    const errors = ref<string[]>([]);
    const errorsCompute = computed({
      get: () => errors.value,
      set: value => (errors.value = value)
    });

    const showUserConfPanel = ref<number>(0);
    const showUserConfPanelComputed = computed({
      get: () => showUserConfPanel.value,
      set: value => (showUserConfPanel.value = value)
    });

    const Itme = ref<boolean>(false);
    const ItmeComputed = computed({
      get: () => Itme.value,
      set: value => (Itme.value = value)
    });

    // const SwitchshowPanel = (num: number) => {
    //   showPanelComputed.value = num;
    // };

    const articles = ref<object[]>([]);
    const articlesComputed = computed({
      get: () => articles.value,
      set: value => (articles.value = value)
    });

    const goods = ref<object[]>([]);
    const goodsComputed = computed({
      get: () => goods.value,
      set: value => (goods.value = value)
    });

    const username = ref<string>("");
    const usernameComputed = computed({
      get: () => username.value,
      set: value => (username.value = value)
    });

    const onfollow = ref<boolean>(false);
    const onfollowComputed = computed({
      get: () => onfollow.value,
      set: value => (onfollow.value = value)
    });

    const follower = ref<object[]>([]);
    const followerComputed = computed({
      get: () => follower.value,
      set: value => (follower.value = value)
    });
    const follow_to = ref<object[]>([]);
    const follow_toComputed = computed({
      get: () => follow_to.value,
      set: value => (follow_to.value = value)
    });

    const next_username = ref<string>("");
    const next_usernameComputed = computed({
      get: () => next_username.value,
      set: value => (next_username.value = value)
    });

    const search_user = async (username: string | string[]) => {
      store.commit("setIsLoading", true);
      // console.log("arg_username", username);
      try {
        if (!username) {
          errorsCompute.value.push("ユーザーが存在しません");
        }
        if (!errorsCompute.value.length) {
          await axios
            .get(`api/v1/articles/profile/${username}`)
            .then(response => {
              // console.log(response.data);
              // console.log("reloading");

              usernameComputed.value = response.data.data.profile.username;
              // console.log(response.data.data.profile.username);

              articlesComputed.value = response.data.data.article_list;
              goodsComputed.value = response.data.data.goods;
              onfollowComputed.value = response.data.data.profile.follow;
              followerComputed.value = response.data.data.profile.follower;
              follow_toComputed.value = response.data.data.profile.follow_to;

              // console.log("usernameComputed:", usernameComputed.value);

              if (usernameComputed.value == store.state.user.username) {
                // console.log("yse");

                ItmeComputed.value = true;
              } else {
                ItmeComputed.value = false;
              }
            })
            .catch(error => {
              // console.log(error.response.data);
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
          await axios
            .get(`api/v1/users/users/${usernameComputed.value}/following/`)
            .then(response => {
              // console.log(response.data);
              // username.value = response.data;
            })
            .catch(error => {
              // console.log(error.response.data);
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
              store.commit("setIsLoading", false);
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
        alert("error");
      }
      store.commit("setIsLoading", false);
    };

    const update_username = async () => {
      store.commit("setIsLoading", true);
      // console.log(next_usernameComputed);

      try {
        if (!next_usernameComputed.value) {
          errorsCompute.value.push("新しいユーザー名を入力してください");
        }
        if (!errorsCompute.value.length) {
          const FormData = {
            username: next_usernameComputed.value
          };

          await axios
            .put(`api/v1/users/users/update/`, FormData)
            .then(response => {
              // console.log(response.data);

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
              // console.log(error.response.data);
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
        alert("error");
      }
      store.commit("setIsLoading", false);
    };

    const follow = async () => {
      try {
        if (!errorsCompute.value.length) {
          if (onfollowComputed.value == true) {
            await axios
              .delete(`api/v1/users/users/${usernameComputed.value}/following/`)
              .then(response => {
                // console.log(response.data);
                onfollowComputed.value = false;
                toast({
                  message: `フォローを外しました`,
                  type: "is-danger",
                  dismissible: true,
                  pauseOnHover: true,
                  duration: 2000,
                  position: "bottom-right"
                });
              })
              .catch(error => {
                // console.log(error.response.data);
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
          } else {
            await axios
              .post(`api/v1/users/users/${usernameComputed.value}/following/`)
              .then(response => {
                // console.log(response.data);
                onfollowComputed.value = true;

                toast({
                  message: `フォローしました`,
                  type: "is-success",
                  dismissible: true,
                  pauseOnHover: true,
                  duration: 2000,
                  position: "bottom-right"
                });
              })
              .catch(error => {
                // console.log(error.response.data);
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
          }
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
        alert("error");
      }

      store.commit("setIsLoading", false);
    };

    const logout = () => {
      store.dispatch("InitializationStore");
      router.push("/");
    };

    const push_to_profile = (username: string) => {
      router.push(`/profile/${username}/`);
    };

    onBeforeRouteUpdate((to, from, next) => {
      // console.log("param:", to.params.username);
      // console.log("router update");

      showPanelComputed.value = 0;
      search_user(to.params.username);
      // console.log("user:", usernameComputed.value);

      next();
    });

    search_user(route.params.username);
    onMounted(() => {
      // console.log("mounted");
      // console.log(showPanelComputed.value);
      // console.log(route.params.username);
    });

    return {
      usernameComputed,
      articlesComputed,
      goodsComputed,
      showPanelComputed,
      showUserConfPanelComputed,
      logout,
      follow,
      next_usernameComputed,
      update_username,
      ItmeComputed,
      onfollowComputed,
      follow_toComputed,
      followerComputed,
      push_to_profile
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
