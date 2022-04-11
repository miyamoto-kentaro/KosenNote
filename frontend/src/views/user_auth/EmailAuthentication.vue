<template>
  <div class="email-authentication">
    <section class="hero is-fullheight">
      <div class="hero-body">
        <div class="container has-text-centered">
          <div class="column is-4 is-offset-4">
            <h3 class="title has-text-black">SignIn</h3>
            <hr class="sign-in-hr" />
            <p class="subtitle has-text-black">ユーザー登録</p>
            <div class="box">
              <form @submit.prevent="submitForm">
                <div class="field">
                  <div class="control">
                    <input
                      class="input is-large"
                      type="text"
                      placeholder="User Name"
                      autofocus=""
                      v-model="usernameComputed"
                    />
                  </div>
                </div>

                <div class="field">
                  <div class="control">
                    <input
                      class="input is-large"
                      type="password"
                      placeholder="Password"
                      autofocus=""
                      v-model="passwordComputed"
                    />
                  </div>
                </div>

                <div class="field">
                  <div class="control">
                    <input
                      class="input is-large"
                      type="password"
                      placeholder="Repeat password"
                      autofocus=""
                      v-model="password2Computed"
                    />
                  </div>
                </div>
                <template v-if="isLoading">
                  <a class="button is-block is-info is-large is-fullwidth">
                    登録
                    <i class="fa fa-sign-in" aria-hidden="true"></i>
                  </a>
                </template>
                <template v-else>
                  <button class="button is-block is-info is-large is-fullwidth">
                    登録
                    <i class="fa fa-sign-in" aria-hidden="true"></i>
                  </button>
                </template>
              </form>
            </div>
            <p class="has-text-grey">
              <router-link to="/log-in">ログイン</router-link>
              &nbsp;·&nbsp;
              <router-link to="/reset-password/send-mail"
                >パスワードの変更</router-link
              >
              &nbsp;·&nbsp;
              <router-link to="/sign-in/email/send-mail"
                >メールアドレスの再入力</router-link
              >
            </p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import { toast } from "bulma-toast";
import axios from "axios";

export default defineComponent({
  name: "EmailAuth",
  setup() {
    document.title = "EmailAuth | KosenNote";
    // data
    const router = useRouter();
    const route = useRoute();
    const store = useStore();

    const errors = ref<string[]>([]);
    const errorsCompute = computed({
      get: () => errors.value,
      set: value => (errors.value = value)
    });

    const email = route.params.email;
    const code = route.params.code;

    const username = ref<string>("");

    const usernameComputed = computed({
      get: () => username.value,
      set: value => (username.value = value)
    });

    const password = ref<string>("");
    const passwordComputed = computed({
      get: () => password.value,
      set: value => (password.value = value)
    });

    const password2 = ref<string>("");
    const password2Computed = computed({
      get: () => password2.value,
      set: value => (password2.value = value)
    });

    const submitForm = async () => {
      store.commit("setIsLoading", true);
      errorsCompute.value = [];
      try {
        if (passwordComputed.value !== password2Computed.value) {
          errorsCompute.value.push("パスワードが違います。確認してください");
        }
        if (!usernameComputed.value) {
          errorsCompute.value.push("ユーザー名を入力してください");
        }

        if (!errorsCompute.value.length) {
          const formData = {
            email: email,
            username: username.value,
            password: password.value,
            code: code
          };

          store.dispatch("InitializationStore");
          await axios
            .post(
              "/api/v1/users/users/email/pre_register/certification",
              formData
            )
            .then(response => {
              toast({
                message: "ユーザー登録が完了しました",
                type: "is-success",
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: "bottom-right"
              });
              console.log(response);

              const user = {
                username: response.data.data.username,
                email: response.data.data.email
              };
              store.commit("setUser", user);
              // console.log(store.state.user);
              // console.log(response.data)
              store.commit("setIsLoading", false);
              Login();
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
        }
      } catch (err) {
        console.log(err);
      }
      store.commit("setIsLoading", false);
    };

    const Login = async () => {
      const formData = {
        email: email,
        password: password.value
      };
      // console.log(formData);
      await axios
        .post("/api/v1/token/login/", formData)
        .then(response => {
          // console.log("form", formData);
          // console.log("response :", response);
          const token = response.data.auth_token;
          store.commit("setToken", token);

          router.push(`/profile/${store.state.user.username}`);
        })
        .catch(error => {
          // console.log(error);
          toast({
            message: "ユーザー名かパスワードが間違っています。",
            type: "is-danger",
            dismissible: true,
            pauseOnHover: true,
            duration: 2000,
            position: "bottom-right"
          });
        });
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
