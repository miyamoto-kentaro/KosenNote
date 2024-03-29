<template>
  <div class="waiting-email">
    <section class="hero is-fullheight">
      <div class="hero-body">
        <div class="container has-text-centered">
          <div class="column is-4 is-offset-4">
            <h3 class="title has-text-black">SignIn</h3>
            <hr class="sign-in-hr" />
            <p class="subtitle has-text-black">Waiting Email</p>
            <div class="box">
              <form @submit.prevent="submitForm">
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

    const email = ref("");

    const emailComputed = computed({
      get: () => email.value,
      set: value => (email.value = value)
    });

    const submitForm = async () => {
      store.commit("setIsLoading", true);
      try {
        errorsCompute.value = [];

        if (store.state.user) {
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

      store.commit("setIsLoading", false);
    };

    return {
      emailComputed,
      submitForm,
      isLoading: computed(() => store.state.isLoading)
    };
  }
});
</script>
