<template>
  <div class="page-sign-up">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">ResetPassword</h1>

        <form @submit.prevent="submitForm">
          <div class="field">
            <label>New Password</label>
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
              <button class="button is-dark">リセット</button>
            </div>
          </div>

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
      try {
        errors = [];
        if (password.value !== password2.value) {
          errors.push("パスワードが違います。確認してください");
        }

        if (!errors.length) {
          const formData = {
            uid: uid,
            token: token,
            new_password: password.value
          };
          // console.log(formData);

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
              router.push("/log-in");
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

    return {
      passwordComputed,
      password2Computed,
      errors,
      submitForm
    };
  }
});
</script>
