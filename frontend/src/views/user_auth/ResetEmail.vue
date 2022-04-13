<template>
  <div class="reset-email"></div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, computed, onMounted } from "vue";
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

    const email = route.params.email;
    const code = route.params.code;

    let errors: string[] = [];

    const ChangeEmail = async () => {
      store.commit("setIsLoading", true);
      try {
        if (!errors.length) {
          const formData = {
            email: email,
            code: code
          };

          store.dispatch("InitializationStore");
          console.log(formData);

          await axios
            .post("/api/v1/users/users/email/update/certification", formData)
            .then(response => {
              store.commit("removeToken");
              toast({
                message: "メールアドレスのリセットが完了しました",
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
          alert(errors);
          store.commit("setIsLoading", false);
        }
      } catch (err) {
        console.log(err);
        store.commit("setIsLoading", false);
      }
      store.commit("setIsLoading", false);
    };

    onMounted(() => {
      ChangeEmail();
    });

    return {
      isLoading: computed(() => store.state.isLoading)
    };
  }
});
</script>
