<template>
  <div class="page-sign-up">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">ResetPassword</h1>

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
            <div class="control">
              <button class="button is-dark">メールを送る</button>
            </div>
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
      try {
        errors = [];
        if (email.value === "") {
          errors.push("メールアドレスを入力してください");
        }
        if (!errors.length) {
          const formData = {
            email: email.value
          };
          store.commit("removeToken");
          await axios
            .post("/api/v1/users/users/already_exists/email", formData)
            .then(response => {
              // console.log(error.response);
              toast({
                message: "そのメールアドレスでユーザー登録されていません",
                type: "is-danger",
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: "bottom-right"
              });
            })
            .catch(error => {
              axios
                .post("/api/v1/users/reset_password/", formData)
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
                });
            });
        }
      } catch (err) {
        alert("error");
        console.log(err);
      }
    };

    return {
      emailComputed,
      errors,
      submitForm
    };
  }
});
</script>
