<template>
  <div class="page-create-report">
    <div class="columns">
      <div class="column title is-10 is-offset-1">ノートの作成</div>
    </div>
    <div class="columns">
      <div class="column box is-10 is-offset-1">
        <nav class="level">
          <!-- Left side -->
          <div class="level-left">
            <div class="level-item">
              <div class="field has-addons">
                <p class="control">
                  <!-- <input
                    class="input"
                    type="text"
                    placeholder="タイトル"
                    v-model="report.title"
                  /> -->
                </p>
              </div>
            </div>
            <div class="level-item">
              <!-- <TagInput v-model="report.tags" /> -->
            </div>
            <div class="level-item">
              <label class="checkbox">
                <input type="checkbox" v-model="unpublish" />
                非公開
              </label>
            </div>
          </div>

          <!-- Right side -->
          <div class="level-right">
            <p class="level-item">
              <a class="" v-on:click="downloadButton()">
                <span class="icon v-md-custom-icon-folder-download"></span>
                保存
              </a>
            </p>

            <p class="level-item">
              <a>
                <span class="icon v-md-custom-icon-folder-download"></span>
                PDFにエクスポート
              </a>
              <!-- <a v-on:click="submitForm()"> PDFにエクスポート </a> -->
            </p>
            <p class="level-item">
              <a class="button is-success" v-on:click="submitForm()"> 作成 </a>
            </p>
          </div>
        </nav>
      </div>
    </div>

    <!-- <div class="notification is-danger" v-if="errors.length">
      <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
    </div> -->
    <div style="text-align: left">
      <!-- v-model="report.content" -->
      <v-md-editor
        left-toolbar="undo redo | h changecolor bold italic strikethrough quote textalignleft textaligncenter textalignright | ul ol table hr | link image code | tip todo-list"
        height="500px"
        :include-level="[1, 2]"
        :toolbar="toolbar"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { toast } from "bulma-toast";
import TagInput from "@/components/TagInput.vue";
export default {
  name: "CreateReport",
  components: {
    TagInput,
  },
  data() {
    this.toolbar = {
      changecolor: {
        title: "change color",
        icon: "v-md-custom-icon-color",
        menus: {
          mode: "panel",
          itemWidth: "56px",
          rowNum: 5,
          items: [
            {
              text: "red",
              action(editor) {
                editor.insert(function (selected) {
                  const prefix = "<span style='color: red; '>";
                  const suffix = "</span>";
                  const placeholder = "placeholder";
                  const content = selected || placeholder;
                  return {
                    text: `${prefix}${content}${suffix}`,
                    selected: content,
                  };
                });
              },
            },
            {
              text: "blue",
              action(editor) {
                editor.insert(function (selected) {
                  const prefix = "<span style='color: blue; '>";
                  const suffix = "</span>";
                  const placeholder = "placeholder";
                  const content = selected || placeholder;
                  return {
                    text: `${prefix}${content}${suffix}`,
                    selected: content,
                  };
                });
              },
            },
            {
              text: "green",
              action(editor) {
                editor.insert(function (selected) {
                  const prefix = "<span style='color: green; '>";
                  const suffix = "</span>";
                  const placeholder = "placeholder";
                  const content = selected || placeholder;
                  return {
                    text: `${prefix}${content}${suffix}`,
                    selected: content,
                  };
                });
              },
            },
            {
              text: "yellow",
              action(editor) {
                editor.insert(function (selected) {
                  const prefix = "<span style='color: yellow; '>";
                  const suffix = "</span>";
                  const placeholder = "placeholder";
                  const content = selected || placeholder;
                  return {
                    text: `${prefix}${content}${suffix}`,
                    selected: content,
                  };
                });
              },
            },
          ],
        },
      },
      textalignleft: {
        title: "text align left",
        icon: "v-md-custom-icon-align-left",
        action(editor) {
          editor.insert(function (selected) {
            const prefix = ":::align-left\n";
            const suffix = "\n:::";
            const placeholder = "placeholder";
            const content = selected || placeholder;
            return {
              text: `${prefix}${content}${suffix}`,
              selected: content,
            };
          });
        },
      },
      textaligncenter: {
        title: "text align center",
        icon: "v-md-custom-icon-align-center",
        action(editor) {
          editor.insert(function (selected) {
            const prefix = ":::align-center\n";
            const suffix = "\n:::";
            const placeholder = "placeholder";
            const content = selected || placeholder;
            return {
              text: `${prefix}${content}${suffix}`,
              selected: content,
            };
          });
        },
      },
      textalignright: {
        title: "text align right",
        icon: "v-md-custom-icon-align-right",
        action(editor) {
          editor.insert(function (selected) {
            const prefix = ":::align-right\n";
            const suffix = "\n:::";
            const placeholder = "placeholder";
            const content = selected || placeholder;
            return {
              text: `${prefix}${content}${suffix}`,
              selected: content,
            };
          });
        },
      },
    };
    return {
      user: {
        username: "",
        id: null,
        email: "",
      },
      report: {
        title: "",
        tags: [],
        content: "",
        author: null,
        category: null,
        publish: true,
      },
      unpublish: false,
      errors: [],
    };
  },
  created() {
    this.user = this.$store.state.user;
    this.report = this.$store.state.report;
  },
  mounted() {
    document.title = "CreateReport | KosenNote";
  },
  methods: {
    async temporarilySaved() {
      this.report.author = this.user.id;
      this.$store.commit("setReport", this.report);
    },
    async submitForm() {
      this.$store.commit("setIsLoading", true);
      this.errors = [];
      if (this.report.title === "") {
        this.errors.push("タイトルが設定されていません");
        toast({
          message: "タイトルが設定されていません",
          type: "is-danger",
          dismissible: true,
          pauseOnHover: true,
          duration: 2000,
          position: "bottom-right",
        });
      }
      if (this.report.content === "") {
        this.errors.push("コンテンツが必要です");
        toast({
          message: "コンテンツが必要です",
          type: "is-danger",
          dismissible: true,
          pauseOnHover: true,
          duration: 2000,
          position: "bottom-right",
        });
      }
      if (!this.errors.length) {
        if (this.user.id) {
          console.log(this.report.publish);
          if (this.unpublish) {
            this.report.publish = false;
          }
          this.report.author = this.user.id;
          this.$store.commit("setReport", this.report);
          const formData = this.report;
          await axios
            .post("api/v1/reports/create", formData)
            .then((response) => {
              toast({
                message: "記事が保存されました",
                type: "is-success",
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: "bottom-right",
              });
              this.$store.commit("removeReport", this.report);
              this.$router.push(`/report/${response.data.id}`);
            })
            .catch((error) => {
              if (error.response) {
                for (const property in error.response.data) {
                  this.errors.push(
                    `${property}: ${error.response.data[property]}`
                  );
                }
                console.log(JSON.stringify(error.response.data));
              } else if (error.message) {
                this.errors.push("Something went wrong. Please try again");
                console.log(JSON.stringify(error));
              }
            });
        } else {
          toast({
            message: "ログインできていません",
            type: "is-danger",
            dismissible: true,
            pauseOnHover: true,
            duration: 2000,
            position: "bottom-right",
          });
          this.$router.push("/log-in");
        }
      }
      this.$store.commit("setIsLoading", false);
    },
    downloadButton() {
      if (this.report.title === "") {
        this.errors.push("タイトルが設定されていません");
        toast({
          message: "タイトルが設定されていません",
          type: "is-danger",
          dismissible: true,
          pauseOnHover: true,
          duration: 2000,
          position: "bottom-right",
        });
      } else if (this.report.content === "") {
        this.errors.push("コンテンツが必要です");
        toast({
          message: "コンテンツが必要です",
          type: "is-danger",
          dismissible: true,
          pauseOnHover: true,
          duration: 2000,
          position: "bottom-right",
        });
      } else {
        const blob = new Blob([this.report.content], { type: "text/plain" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = `${this.report.title}.md`;
        link.click();
      }
    },
  },
};
</script>