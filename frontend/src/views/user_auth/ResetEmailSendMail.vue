<template>
  <div class="reset-email-send-mail">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">ResetEmail</h1>

        <form @submit.prevent="submitForm">
          <div class="field">
            <label>Email Address</label>
            <div class="control">
              <input type="text" class="input" v-model="emailComputed" />
            </div>
          </div>

          <div class="notification is-danger" v-if="errors.length">
            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
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

          <hr />

          Or <router-link to="/log-in">ログイン</router-link>
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
      } catch (err) {
        alert("error");
        console.log(err);
        store.commit("setIsLoading", false);
      }
    };

    return {
      emailComputed,
      errors,
      isLoading: computed(() => store.state.isLoading),
      submitForm
    };
  }
});
</script>
