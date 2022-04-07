<template>
  <div class="log-in">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">Log in</h1>

        <form @submit.prevent="submitForm">
          <div class="field">
            <label>Email Address</label>
            <div class="control">
              <input type="text" class="input" v-model="emailComputed" />
            </div>
          </div>

          <div class="field">
            <label>Password</label>
            <div class="control">
              <input type="password" class="input" v-model="passwordComputed" />
            </div>
          </div>

          <div class="notification is-danger" v-if="errors.length">
            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
          </div>

          <div class="field">
            <template v-if="isLoading">
              <div class="control">
                <a class="button is-dark">
                  ログイン
                </a>
              </div>
            </template>
            <template v-else>
              <div class="control">
                <button class="button is-dark">
                  ログイン
                </button>
              </div>
            </template>
          </div>

          <hr />

          Or <router-link to="/sign-in/email/send-mail">サインイン</router-link>

          <hr />

          Or
          <router-link to="/reset-password/send-mail"
            >パスワードの変更</router-link
          >
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

interface User {
  username: string;
  email: string;
}

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

    const password = ref("");

    const passwordComputed = computed({
      get: () => password.value,
      set: value => (password.value = value)
    });
    // async function submitForm() {
    //   alert('called submit')
    // }

    const submitForm = async () => {
      store.commit("setIsLoading", true);
      console.log(store.state.isLoading);
      try {
        errors = [];
        // if (email.value === "") {
        //   toast({
        //     message: "メールアドレスを入力してください",
        //     type: "is-danger",
        //     dismissible: true,
        //     pauseOnHover: true,
        //     duration: 2000,
        //     position: "bottom-right"
        //   });
        // }
        if (!errors.length) {
          const formData = {
            email: email.value,
            password: password.value
          };

          store.commit("removeToken");
          await axios
            .post("/api/v1/token/login", formData)
            .then(response => {
              // console.log(response.data);
              toast({
                message: "ログインできました",
                type: "is-success",
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: "bottom-right"
              });
              store.commit("setToken", response.data.auth_token);
              // console.log(store.state.user);
              // console.log(response.data);
              GetUser();
              router.push(`/`);
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
                    message: "パスワードが間違っています",
                    type: "is-danger",
                    dismissible: true,
                    pauseOnHover: true,
                    duration: 2000,
                    position: "bottom-right"
                  });
                }
              }
            });
        }
      } catch (err) {
        alert("error");
      }
      store.commit("setIsLoading", false);
    };

    const GetUser = async () => {
      // console.log(axios.defaults.headers.common["Authorization"]);
      await axios
        .get("/api/v1/users/me")
        .then(response => {
          const user: User = {
            username: response.data.username,
            email: response.data.email
          };
          store.commit("setUser", user);
          // console.log(response.data);
          // console.log("user:", store.state.user);
        })
        .catch(error => {
          // console.log(JSON.stringify(error));
          console.log(error.data);
        });
      // store.commit("setIsLoading", false);
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
