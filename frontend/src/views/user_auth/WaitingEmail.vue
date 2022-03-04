<template>
  <div class="waiting-email">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <h1 class="title">Waiting Email</h1>

        <form @submit.prevent="submitForm">
          <div class="field">
            <div class="control">
              <button class="button is-dark">メールの再送</button>
            </div>
          </div>

          <hr />

          Or
          <router-link to="/sign-in/email/send-mail"
            >メールアドレスの再入力</router-link
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

export default defineComponent({
  setup() {
    // data
    const router = useRouter();
    const route = useRoute();
    const store = useStore();

    let errors: string[] = [];

    const email = ref("example@gmail.com");

    const emailComputed = computed({
      get: () => email.value,
      set: value => (email.value = value)
    });

    // async function submitForm() {
    //   alert('called submit')
    // }

    // const push_send_email = () => {
    //   if (store.state.user.email == "") {
    //     router.push("/sign-in/email/send-mail");
    //   }
    // };
    // push_send_email();

    const submitForm = async () => {
      try {
        errors = [];
        if (store.state.user.email) {
          const formData = {
            email: store.state.user.email
          };
          // console.log(formData);

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
              // console.log(response.data);
              router.push("/sign-in/email/waiting-email");
            })
            .catch(error => {
              toast({
                message: `${error.response.data.status}: ${error.response.data.data.error_message}`,
                type: "is-danger",
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: "bottom-right"
              });
            });
        } else {
          router.push("/sign-in/email/send-mail");
        }
      } catch (err) {
        alert("error");
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
