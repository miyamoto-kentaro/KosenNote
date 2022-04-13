<template>
  <div class="create-article">
    <div class="columns">
      <div class="column title is-10 is-offset-1">記事の作成</div>
    </div>
    <div class="columns">
      <div class="column">
        <div class="columns">
          <div class="column is-3">
            <div class="field has-addons">
              <p class="control">
                <input
                  class="input"
                  type="text"
                  placeholder="タイトル"
                  v-model="articleComputed.title"
                />
              </p>
            </div>
          </div>
          <div class="column is-3">
            <TagInput v-model="articleComputed.tags" />
          </div>
          <div class="column">
            <label
              class="checkbox"
              @click="articleComputed.publish = !articleComputed.publish"
            >
              <!-- <input type="checkbox" v-model="articleComputed.publish" /> -->
              <span class="icon">
                <i
                  class="icon"
                  :class="[
                    articleComputed.publish
                      ? 'kosen-note-icon-unlocked'
                      : 'kosen-note-icon-lock'
                  ]"
                ></i>
              </span>
            </label>
            <a @click="downloadButton()">
              <span class="icon">
                <i class="kosen-note-icon-folder-download"></i>
              </span>
            </a>
          </div>
          <div class="column">
            <a class="button is-success" @click="submitForm()">
              投稿
            </a>
          </div>
        </div>
      </div>
    </div>
    <MarkdownEditor
      :value="articleComputed.content"
      @update_props="newVal => (articleComputed.content = newVal)"
      @save_article="save_article"
    />
  </div>
</template>

<script lang="ts">
import {
  defineComponent,
  ref,
  computed,
  onMounted,
  onActivated,
  onBeforeUpdate
} from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "vuex";
import { toast } from "bulma-toast";
import axios from "axios";

import MarkdownEditor from "../../components/MarkdownEditor.vue";
import TagInput from "../../components/TagInput.vue";

interface Article {
  title: string;
  tags: string[];
  content: string;
  category: string;
  publish: boolean;
}

export default defineComponent({
  name: "CreateArticle",
  components: {
    MarkdownEditor,
    TagInput
  },

  setup() {
    const router = useRouter();
    const route = useRoute();
    const store = useStore();
    // const article_content = ref("");

    const errors = ref<string[]>([]);
    const errorsCompute = computed({
      get: () => errors.value,
      set: value => (errors.value = value)
    });

    const article = ref<Article>({
      title: "",
      tags: [],
      content: "",
      category: "",
      publish: false
    });

    const articleComputed = computed({
      get: () => article.value,
      set: value => (article.value = value)
    });

    const downloadButton = () => {
      const blob = new Blob([articleComputed.value.content], {
        type: "text/plain"
      });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      if (articleComputed.value.title) {
        link.download = `${articleComputed.value.title}.md`;
      } else {
        link.download = "article.md";
      }
      link.click();
    };

    const submitForm = async () => {
      store.commit("setIsLoading", true);
      try {
        // バリデーション

        if (!articleComputed.value.title) {
          errorsCompute.value.push("タイトルを入力してください");
        }
        if (!articleComputed.value.content) {
          errorsCompute.value.push("記事にはコンテンツが必要です");
        }

        if (!errorsCompute.value.length) {
          await axios
            .post("api/v1/articles/articles/create/", articleComputed.value)
            .then(response => {
              toast({
                message: "記事が保存されました",
                type: "is-success",
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: "bottom-right"
              });
              store.commit("removeSavedArticle");

              // store.commit("removeArticle", article.value);
              console.log(response.data.data);

              router.push(`/article-detail/${response.data.data.id}`);
            })
            .catch(error => {
              console.log(error.response.data);
              if (error.response.data.data.title) {
                if (
                  error.response.data.data.title[0] ==
                  ["This field may not be blank."]
                ) {
                  toast({
                    message: "タイトルが入力されていません",
                    type: "is-danger",
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 2000,
                    position: "bottom-right"
                  });
                }
              } else if (error.response.data.data.content) {
                if (
                  error.response.data.data.content[0] ==
                  ["This field may not be blank."]
                ) {
                  toast({
                    message: "コンテンツが必要です",
                    type: "is-danger",
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 2000,
                    position: "bottom-right"
                  });
                }
              } else if (error.response.data.data.error == "DoseNotExist") {
                toast({
                  message:
                    "ユーザーが存在していません。正しくログインしてください",
                  type: "is-danger",
                  dismissible: true,
                  pauseOnHover: true,
                  duration: 2000,
                  position: "bottom-right"
                });
              } else if (error.response.data.data.detail) {
                if (error.response.data.data.detail == ["Invalid token."]) {
                  toast({
                    message:
                      "URLに間違いがあります。再度メールを送ってください。",
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

    const save_article = () => {
      // console.log("yes");
      store.commit("setSavedArticle", articleComputed.value);
    };

    onMounted(() => {
      if (store.state.saved_article) {
        articleComputed.value = store.state.saved_article;
      }
    });

    return {
      articleComputed,
      downloadButton,
      submitForm,
      save_article
    };
  }
});
</script>
