<template>
  <div class="reset-email-send-mail">
    <section class="hero is-fullheight">
      <div class="hero-body">
        <div class="container has-text-centered">
          <div class="column is-4 is-offset-4">
            <h3 class="title has-text-black">ResetEmail</h3>
            <hr class="login-hr" />
            <p class="subtitle has-text-black">Emailをリセットします</p>
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
                  <template v-if="isLoading">
                    <div class="control">
                      <a class="button is-dark">
                        メールを送る
                      </a>
                    </div>
                  </template>
                  <template v-else>
                    <div class="control">
                      <button class="button is-dark">
                        メールを送る
                      </button>
                    </div>
                  </template>
                </div>
              </form>
            </div>
            <p class="has-text-grey">
              <router-link to="/log-in">ログイン</router-link>
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

    const email = ref("");

    const emailComputed = computed({
      get: () => email.value,
      set: value => (email.value = value)
    });

    // async function submitForm() {
    //   alert('called submit')
    // }

    const submitForm = async () => {
      store.commit("setIsLoading", true);
      try {
        // バリデーション
        if (!emailComputed.value) {
          errorsCompute.value.push("メールアドレスを入力してください");
        }

        if (!errorsCompute.value.length) {
          const formData = {
            previous_email: store.state.user.email,
            email: emailComputed.value
          };
          await axios
            .post(
              "/api/v1/users/users/email/change_email_ticket/create",
              formData
            )
            .then(response => {
              console.log(response);

              toast({
                message:
                  "入力したメールアドレスにメールを送りました。確認して、認証URLにアクセスしてください",
                type: "is-success",
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: "bottom-right"
              });
              store.commit("setIsLoading", false);
              // console.log(store.state.user);
              // console.log(response.data)
              //   router.push("/sign-in/email/waiting-email");
            })
            .catch(error => {
              console.log(error.response.data);
              toast({
                message: `${error.response.data.data.error_message}`,
                type: "is-danger",
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: "bottom-right"
              });
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
        console.log(err);
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
