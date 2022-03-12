<template>
  <div class="email-authentication">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">Sign up</h1>

        <form @submit.prevent="submitForm">
          <div class="field">
            <label>User Name</label>
            <div class="control">
              <input type="text" class="input" v-model="usernameComputed" />
            </div>
          </div>

          <div class="field">
            <label>Password</label>
            <div class="control">
              <input type="password" class="input" v-model="passwordComputed" />
            </div>
          </div>

          <div class="field">
            <label>Repeat password</label>
            <div class="control">
              <input
                type="password"
                class="input"
                v-model="password2Computed"
              />
            </div>
          </div>

          <div class="notification is-danger" v-if="errors.length">
            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
          </div>

          <div class="field">
            <template v-if="isLoading">
              <div class="control">
                <a class="button is-dark">
                  ユーザー登録
                </a>
              </div>
            </template>
            <template v-else>
              <div class="control">
                <button class="button is-dark">
                  ユーザー登録
                </button>
              </div>
            </template>
          </div>
          Or
          <router-link to="/sign-in/email/send-mail"
            >メールアドレスの再入力</router-link
          >

          <hr />

          <!-- Or <router-link to="/log-in">click here</router-link> to log in! -->
          Or click here to log in!
        </form>
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
    // data
    const router = useRouter();
    const route = useRoute();
    const store = useStore();

    let errors: string[] = [];

    const username = ref("");

    const usernameComputed = computed({
      get: () => username.value,
      set: value => (username.value = value)
    });

    const password = ref("");

    const passwordComputed = computed({
      get: () => password.value,
      set: value => (password.value = value)
    });

    const password2 = ref("");

    const password2Computed = computed({
      get: () => password2.value,
      set: value => (password2.value = value)
    });

    const submitForm = async () => {
      store.commit("setIsLoading", true);
      try {
        errors = [];
        if (password.value !== password2.value) {
          errors.push("パスワードが違います。確認してください");
        }

        if (!errors.length) {
          const formData = {
            title: "sample",
            tags: [],
            content: "sample text",
            category: null,
            publish: true
          };
          // console.log(formData);

          // store.commit("removeToken");
          await axios
            .post("/api/v1/articles/articles/create/", formData)
            .then(response => {
              console.log(response.data);
              store.commit("setIsLoading", false);
            })
            .catch(error => {
              console.log(error.response.data);
              if (error.response.data.data.password) {
                if (
                  error.response.data.data.password[0] ==
                  ["This field may not be blank."]
                ) {
                  toast({
                    message: "パスワードが入力されていません",
                    type: "is-danger",
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 2000,
                    position: "bottom-right"
                  });
                  store.commit("setIsLoading", false);
                }
              } else if (error.response.data.data.username) {
                if (
                  error.response.data.data.username[0] ==
                  ["A user with that username already exists."]
                ) {
                  toast({
                    message: "ユーザーネームは既に使用されています",
                    type: "is-danger",
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 2000,
                    position: "bottom-right"
                  });
                  store.commit("setIsLoading", false);
                } else if (
                  error.response.data.data.username[0] ==
                  ["This field may not be blank."]
                ) {
                  toast({
                    message: "ユーザーネームが入力されていません",
                    type: "is-danger",
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 2000,
                    position: "bottom-right"
                  });
                  store.commit("setIsLoading", false);
                }
              } else if (error.response.data.data.email) {
                if (
                  error.response.data.data.email[0] ==
                  ["user with this email address already exists."]
                ) {
                  toast({
                    message:
                      "このユーザーは既に存在しています。ログインしてください",
                    type: "is-danger",
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 2000,
                    position: "bottom-right"
                  });
                }
              } else {
                toast({
                  message: `${error.response.data.data.error_message}`,
                  type: "is-danger",
                  dismissible: true,
                  pauseOnHover: true,
                  duration: 2000,
                  position: "bottom-right"
                });
              }
              store.commit("setIsLoading", false);
            });
        } else {
          alert(errors);
          store.commit("setIsLoading", false);
        }
      } catch (err) {
        console.log(err);
        store.commit("setIsLoading", false);
      }
    };

    return {
      usernameComputed,
      passwordComputed,
      password2Computed,
      errors,
      isLoading: computed(() => store.state.isLoading),
      submitForm
    };
  }
});
</script>
