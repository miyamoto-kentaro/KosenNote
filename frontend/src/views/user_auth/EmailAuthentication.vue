<template>
  <div class="page-sign-up">
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
            <div class="control">
              <button class="button is-dark">ユーザー登録</button>
            </div>
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

    const email = route.params.email;
    const code = route.params.code;

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
      try {
        errors = [];
        if (password.value !== password2.value) {
          errors.push("パスワードが違います。確認してください");
        }

        if (!errors.length) {
          const formData = {
            email: email,
            username: username.value,
            password: password.value,
            code: code
          };
          // console.log(formData);

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
              const user = {
                username: response.data.data.username,
                email: response.data.data.email
              };
              store.commit("setUser", user);
              // console.log(store.state.user);
              // console.log(response.data)
              Login();
              router.push("/sign-in/email/waiting-email");
            })
            .catch(error => {
              // console.log(error.response.data);
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
              }
            });
        } else {
          alert(errors);
        }
      } catch (err) {
        console.log(err);
      }
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
          axios.defaults.headers.common["Authorization"] = "token " + token;
          localStorage.setItem("token", token);
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
      submitForm
    };
  }
});
</script>
