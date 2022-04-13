<template>
  <div class="log-in">
    <section class="hero is-fullheight">
      <div class="hero-body">
        <div class="container has-text-centered">
          <div class="column is-4 is-offset-4">
            <h3 class="title has-text-black">Login</h3>
            <hr class="login-hr" />
            <p class="subtitle has-text-black">ログインしてください</p>
            <div class="box">
              <form @submit.prevent="submitForm">
                <div class="field">
                  <div class="control">
                    <input
                      class="input is-large"
                      type="email"
                      placeholder="Your Email"
                      autofocus=""
                      v-model="emailComputed"
                    />
                  </div>
                </div>

                <div class="field">
                  <div class="control">
                    <input
                      class="input is-large"
                      type="password"
                      placeholder="Your Password"
                      v-model="passwordComputed"
                    />
                  </div>
                </div>

                <template v-if="isLoading">
                  <a class="button is-block is-info is-large is-fullwidth">
                    Login <i class="fa fa-sign-in" aria-hidden="true"></i>
                  </a>
                </template>
                <template v-else>
                  <button class="button is-block is-info is-large is-fullwidth">
                    Login <i class="fa fa-sign-in" aria-hidden="true"></i>
                  </button>
                </template>
              </form>
            </div>
            <p class="has-text-grey">
              <router-link to="/sign-in/email/send-mail"
                >サインイン</router-link
              >
              &nbsp;·&nbsp;
              <router-link to="/reset-password/send-mail"
                >パスワードの変更</router-link
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

interface User {
  username: string;
  email: string;
}

export default defineComponent({
  name: "LogIn",
  setup() {
    document.title = "LogIn | KosenNote";
    // data
    const router = useRouter();
    const route = useRoute();
    const store = useStore();

    const errors = ref<string[]>([]);
    const errorsCompute = computed({
      get: () => errors.value,
      set: value => (errors.value = value)
    });

    const email = ref<string>("");
    const emailComputed = computed({
      get: () => email.value,
      set: value => (email.value = value)
    });

    const password = ref<string>("");
    const passwordComputed = computed({
      get: () => password.value,
      set: value => (password.value = value)
    });

    const submitForm = async () => {
      store.commit("setIsLoading", true);
      console.log(store.state.isLoading);
      errorsCompute.value = [];
      try {
        // バリデーション
        if (!emailComputed.value) {
          errorsCompute.value.push("メールアドレスを入力してください");
        }
        if (!passwordComputed.value) {
          errorsCompute.value.push("パスワードを入力してください");
        }

        if (!errorsCompute.value.length) {
          const formData = {
            email: email.value,
            password: password.value
          };

          store.dispatch("InitializationStore");
          await axios
            .post("/api/v1/token/login", formData)
            .then(response => {
              console.log(response.data.auth_token);

              store.commit("setToken", response.data.auth_token);
              console.log("yes");

              GetUser();
            })
            .catch(error => {
              // console.log(error.response);

              if (error.response.data.email) {
                if (
                  error.response.data.email[0] ==
                  ["This field may not be blank."]
                ) {
                  toast({
                    message: "メールアドレスを入力してください",
                    type: "is-danger",
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 2000,
                    position: "bottom-right"
                  });
                }
              } else if (error.response.data.password) {
                if (
                  error.response.data.password[0] ==
                  ["This field may not be blank."]
                ) {
                  toast({
                    message: "パスワードを入力してください",
                    type: "is-danger",
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 2000,
                    position: "bottom-right"
                  });
                }
              } else if (error.response.data.non_field_errors) {
                if (
                  error.response.data.non_field_errors[0] ==
                  ["Unable to log in with provided credentials."]
                ) {
                  toast({
                    message: "パスワードかメールアドレスが間違っています",
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

    const GetUser = async () => {
      console.log("get user");
      await axios
        .get("/api/v1/users/me")
        .then(response => {
          console.log(response);

          const user: User = {
            username: response.data.username,
            email: response.data.email
          };

          store.commit("setUser", user);

          toast({
            message: "ログインできました",
            type: "is-success",
            dismissible: true,
            pauseOnHover: true,
            duration: 2000,
            position: "bottom-right"
          });

          router.push(`/profile/${user.username}`);
        })
        .catch(error => {
          toast({
            message: "予期せぬエラー",
            type: "is-danger",
            dismissible: true,
            pauseOnHover: true,
            duration: 2000,
            position: "bottom-right"
          });
          router.push("/");
        });
    };

    return {
      emailComputed,
      passwordComputed,
      errors,
      isLoading: computed(() => store.state.isLoading),
      submitForm
    };
  }
});
</script>
