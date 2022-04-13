<template>
  <div class="sign-in-with-email">
    <section class="hero is-fullheight">
      <div class="hero-body">
        <div class="container has-text-centered">
          <div class="column is-4 is-offset-4">
            <h3 class="title has-text-black">SignIn</h3>
            <hr class="sign-in-hr" />
            <p class="subtitle has-text-black">認証メールを送ります</p>
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
                <template v-if="isLoading">
                  <a class="button is-block is-info is-large is-fullwidth">
                    メールを送る
                    <i class="fa fa-sign-in" aria-hidden="true"></i>
                  </a>
                </template>
                <template v-else>
                  <button class="button is-block is-info is-large is-fullwidth">
                    メールを送る
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
  name: "SignInWithEmail",
  setup() {
    document.title = "SignInWithEmail | KosenNote";
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

    // async function submitForm() {
    //   alert('called submit')
    // }

    const submitForm = async () => {
      store.commit("setIsLoading", true);
      errorsCompute.value = [];
      try {
        if (!email.value) {
          errorsCompute.value.push("メールアドレスを入力してください");
        }
        if (!errorsCompute.value.length) {
          const formData = {
            email: email.value
          };
          store.dispatch("InitializationStore");

          await axios
            .post("/api/v1/users/users/email/pre_register/create", formData)
            .then(response => {
              toast({
                message:
                  "入力したメールアドレスにメールを送りました。確認して、認証URLにアクセスしてください",
                type: "is-success",
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: "bottom-right"
              });
              const user = {
                username: "",
                email: response.data.data.email
              };
              store.commit("setUser", user);
              // console.log(store.state.user);
              // console.log(response.data)
              // router.push("/sign-in/email/waiting-email");
            })
            .catch(error => {
              toast({
                message: `${error.response.data.data.error_message}`,
                type: "is-danger",
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: "bottom-right"
              });
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

    return {
      emailComputed,
      isLoading: computed(() => store.state.isLoading),
      submitForm
    };
  }
});
</script>
