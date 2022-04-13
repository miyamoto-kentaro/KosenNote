<template>
  <div class="article-detail">
    <div class="columns">
      <div class="column is-offset-1 is-10">
        <article class="message is-dark is-medium">
          <div class="message-header">
            <div
              class="dropdown"
              v-bind:class="{
                'is-active': showTagsMenuComputed
              }"
            >
              <div class="dropdown-trigger">
                <button
                  class="button"
                  aria-haspopup="true"
                  aria-controls="dropdown-menu"
                  @click="showTagsMenuComputed = !showTagsMenuComputed"
                >
                  <span>tags</span>
                  <span class="icon">
                    <i class="kosen-note-icon-circle-down"></i>
                  </span>
                </button>
              </div>
              <div class="dropdown-menu" id="dropdown-menu" role="menu">
                <div class="dropdown-content">
                  <a
                    class="dropdown-item"
                    v-for="tag in articleComputed.tags"
                    v-bind:key="tag.id"
                  >
                    <span>
                      <a @click="push_search(tag)">
                        {{ tag }}
                      </a></span
                    >
                  </a>
                </div>
              </div>
            </div>
            <p class="article-title">&nbsp;Title:{{ articleComputed.title }}</p>
            <p>&nbsp;By:{{ articleComputed.get_author_name }}</p>
          </div>

          <div class="message-body">
            <div class="tabs is-right">
              <ul>
                <li v-if="isGoodComputed == true">
                  <a @click="goodToArticle" class="has-text-danger">
                    ブックマークから削除
                  </a>
                </li>
                <li v-else>
                  <a @click="goodToArticle" class="has-text-info">
                    ブックマークに追加
                  </a>
                </li>
                <li v-if="ItmeComputed">
                  <router-link
                    v-bind:to="`/edit-article/${articleComputed.id}/`"
                    class="has-text-info"
                  >
                    編集
                  </router-link>
                </li>
                <li v-if="ItmeComputed">
                  <a
                    class="show-modal has-text-danger"
                    data-target="my-modal"
                    @click="showDeleteMenuComputed = !showDeleteMenuComputed"
                    >記事の削除</a
                  >
                </li>
                <li v-if="ItmeComputed">
                  <a
                    class="show-modal"
                    data-target="my-modal"
                    @click="downloadButton"
                  >
                    <span class="icon v-md-custom-icon-folder-download"></span>
                  </a>
                </li>
              </ul>
            </div>
            <div style="color:gray; font-size:5px; text-align: right; ">
              {{ articleComputed.create_at }}
            </div>
            <MrkdownCompiler :text="articleComputed.content" />
          </div>

          <div
            class="modal"
            v-bind:class="{ 'is-active': showDeleteMenuComputed }"
          >
            <div
              @click="showDeleteMenuComputed = !showDeleteMenuComputed"
              class="modal-background"
            ></div>
            <div class="modal-content">
              <div class="card">
                <div class="card-content">
                  <div class="content">
                    本当に記事を削除しますか？
                    <p class="has-text-grey">
                      データは完全に消滅します。
                    </p>
                    <br />
                    <!-- <p>{{ currentDateTime() }}</p> -->
                  </div>
                  <div class="button is-danger" @click="deleteArticle">
                    削除
                  </div>
                </div>
              </div>
            </div>
            <button
              @click="showDeleteMenuComputed = !showDeleteMenuComputed"
              class="modal-close is-large"
              aria-label="close"
            ></button>
          </div>
        </article>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "vuex";
import { toast } from "bulma-toast";
import axios from "axios";

import MrkdownCompiler from "../../components/MrkdownCompiler.vue";
export default defineComponent({
  name: "ArticleDetail",
  components: {
    MrkdownCompiler
  },

  setup() {
    const router = useRouter();
    const route = useRoute();
    const store = useStore();

    const errors = ref<string[]>([]);
    const errorsCompute = computed({
      get: () => errors.value,
      set: value => (errors.value = value)
    });

    const article_id = route.params.article_id;
    const article = ref({
      title: "",
      tags: [],
      content: "",
      create_at: "",
      update_at: "",
      author: null,
      category: null,
      get_author_name: ""
    });
    const articleComputed = computed({
      get: () => article.value,
      set: value => (article.value = value)
    });

    const showTagsMenu = ref(false);
    const showTagsMenuComputed = computed({
      get: () => showTagsMenu.value,
      set: value => (showTagsMenu.value = value)
    });

    const showDeleteMenu = ref(false);
    const showDeleteMenuComputed = computed({
      get: () => showDeleteMenu.value,
      set: value => (showDeleteMenu.value = value)
    });

    const Itme = ref(false);
    const ItmeComputed = computed({
      get: () => Itme.value,
      set: value => (Itme.value = value)
    });

    const isGood = ref<boolean>(false);
    const isGoodComputed = computed({
      get: () => isGood.value,
      set: value => (isGood.value = value)
    });

    const getArticleDetail = async () => {
      store.commit("setIsLoading", true);
      try {
        // バリデーション
        console.log("article_id", article_id);

        if (article_id == "") {
          errorsCompute.value.push("記事のidが入力されていません");
        }

        if (!errorsCompute.value.length) {
          await axios
            .get(`api/v1/articles/articles/detail/${article_id}`)
            .then(response => {
              articleComputed.value = response.data.data;
              if (
                articleComputed.value.get_author_name ==
                store.state.user.username
              ) {
                ItmeComputed.value = true;
              }
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
          const FormData = {
            article_id: article_id
          };
          if (store.state.isAuthenticated) {
            await axios
              .post("api/v1/articles/goods/already_exists/", FormData)
              .then(response => {
                console.log(response.data.data.already_good);

                isGoodComputed.value = response.data.data.already_good;
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
          }
          store.commit("setIsLoading", false);
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

    const deleteArticle = async () => {
      store.commit("setIsLoading", true);
      await axios
        .delete(
          `api/v1/articles/articles/authenticated/detail/${route.params.article_id}`
        )
        .then(response => {
          console.log(response.data.data);
          console.log(articleComputed);

          // store.commit("removeArticle", article.value?);

          router.push(`/profile/${store.state.user.username}`);
        })
        .catch(error => {
          console.log(error.response.data);
          if (error.response.data.data.error == "DoseNotExist") {
            toast({
              message: error.response.data.data.error_message,
              type: "is-danger",
              dismissible: true,
              pauseOnHover: true,
              duration: 2000,
              position: "bottom-right"
            });
          }
        });
      store.commit("setIsLoading", false);
    };

    const goodToArticle = async () => {
      store.commit("setIsLoading", true);
      if (isGoodComputed.value == true) {
        const config = {
          data: {
            article_id: article_id
          }
        };
        await axios
          .delete(`api/v1/articles/goods/destroy/`, config)
          .then(response => {
            isGoodComputed.value = false;
            console.log("degood");

            store.commit("setIsLoading", false);
          })
          .catch(error => {
            console.log(error.response.data);
            if (error.response.data.data.error == "DoseNotExist") {
              toast({
                message: `${error.response.data.data.error_message}`,
                type: "is-danger",
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: "bottom-right"
              });
              store.commit("setIsLoading", false);
              router.push("/");
            }
          });
      } else if (isGoodComputed.value == false) {
        const FormData = {
          article_id: article_id
        };
        await axios
          .put(`api/v1/articles/goods/create/`, FormData)
          .then(response => {
            isGoodComputed.value = true;
            store.commit("setIsLoading", false);
          })
          .catch(error => {
            console.log(error.response.data);
            if (error.response.data.data.error == "DoseNotExist") {
              toast({
                message: `${error.response.data.data.error_message}`,
                type: "is-danger",
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: "bottom-right"
              });
              store.commit("setIsLoading", false);
            } else if ((error.response.data.data.error = "AlreadyExists")) {
              isGoodComputed.value = true;
            }
          });
      }
      store.commit("setIsLoading", false);
    };
    const push_search = (tag: string) => {
      router.push(`/search-article/${tag}`);
    };

    getArticleDetail();

    return {
      articleComputed,
      deleteArticle,
      showTagsMenuComputed,
      showDeleteMenuComputed,
      ItmeComputed,
      isGoodComputed,
      goodToArticle,
      push_search
    };
  }
});
</script>

<style scoped>
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
