<template>
  <div class="reset-password">
    <section class="hero is-fullheight">
      <div class="hero-body">
        <div class="container has-text-centered">
          <div class="column is-4 is-offset-4">
            <h3 class="title has-text-black">ResetPassword</h3>
            <hr class="sign-in-hr" />
            <p class="subtitle has-text-black">パスワードを入力してください</p>
            <div class="box">
              <form @submit.prevent="submitForm">
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
                    リセット
                    <i class="fa fa-sign-in" aria-hidden="true"></i>
                  </a>
                </template>
                <template v-else>
                  <button class="button is-block is-info is-large is-fullwidth">
                    リセット
                    <i class="fa fa-sign-in" aria-hidden="true"></i>
                  </button>
                </template>
              </form>
            </div>
            <p class="has-text-grey">
              <router-link to="/log-in">ログイン</router-link>
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
  setup() {
    // data
    const router = useRouter();
    const route = useRoute();
    const store = useStore();

    const errors = ref<string[]>([]);
    const errorsCompute = computed({
      get: () => errors.value,
      set: value => (errors.value = value)
    });

    const uid = route.params.uid;
    const token = route.params.token;

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
        if (passwordComputed.value !== password2Computed.value) {
          errorsCompute.value.push("パスワードが違います。確認してください");
        }

        if (!errorsCompute.value.length) {
          const formData = {
            uid: uid,
            token: token,
            new_password: password.value
          };

          store.dispatch("InitializationStore");
          console.log(formData);

          await axios
            .post("/api/v1/users/reset_password_confirm/", formData)
            .then(response => {
              toast({
                message: "パスワードのリセットが完了しました",
                type: "is-success",
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: "bottom-right"
              });
              // console.log(store.state.user);
              // console.log(response.data)
              store.commit("setIsLoading", false);
              router.push("/log-in");
            })
            .catch(error => {
              console.log(error.response);
              if (error.response.data.new_password) {
                if (
                  error.response.data.new_password[0] ==
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
                } else if (
                  error.response.data.new_password[0] ==
                  "This password is too short. It must contain at least 8 characters."
                ) {
                  toast({
                    message: "パスワードが短すぎます",
                    type: "is-danger",
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 2000,
                    position: "bottom-right"
                  });
                  store.commit("setIsLoading", false);
                }
              } else if (error.response.data.detail) {
                console.log("detail");

                if (error.response.data.detail == ["Invalid token."]) {
                  toast({
                    message:
                      "URLに間違いがあります。再度メールを送ってください。",
                    type: "is-danger",
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 2000,
                    position: "bottom-right"
                  });
                  store.commit("setIsLoading", false);
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
        store.commit("setIsLoading", false);
      }
      store.commit("setIsLoading", false);
    };

    return {
      passwordComputed,
      password2Computed,
      isLoading: computed(() => store.state.isLoading),
      submitForm
    };
  }
});
</script>
